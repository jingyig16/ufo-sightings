import os, re, glob, json, argparse
from dataclasses import dataclass
from typing import Optional, List, Tuple
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import rowcol

class Config:
    city_csv: str
    worldclim_bio_dir: Optional[str]
    elev_tif: Optional[str]
    viirs_annual_tif: Optional[str]
    viirs_monthly_tiles: Optional[str]
    viirs_monthly_tag: Optional[str]
    output_csv: Optional[str]

def read_config(args):
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        return Config(**cfg)
    else:
        return Config(
            city_csv=args.city_csv,
            worldclim_bio_dir=args.worldclim_bio_dir,
            elev_tif=args.elev_tif,
            viirs_annual_tif=args.viirs_annual_tif,
            viirs_monthly_tiles=args.viirs_monthly_tiles,
            viirs_monthly_tag=args.viirs_monthly_tag,
            output_csv=args.output_csv
        )

def require_cols(df: pd.DataFrame, cols: List[str]):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in city CSV: {missing}")

def to_points(df: pd.DataFrame) -> List[Tuple[float,float]]:
    return list(zip(df['lng'].astype(float), df['lat'].astype(float)))

def sample_raster(points: List[Tuple[float,float]], tif: str, band: int=1) -> np.ndarray:
    values = np.full(len(points), np.nan, dtype=np.float64)
    with rasterio.open(tif) as src:
        arr = src.read(band)
        T = src.transform
        H, W = src.height, src.width
        for i, (x,y) in enumerate(points):
            try:
                r, c = rowcol(T, x, y)
                if 0 <= r < H and 0 <= c < W:
                    v = arr[r, c]
                    if (src.nodata is not None) and np.isclose(v, src.nodata):
                        values[i] = np.nan
                    else:
                        values[i] = float(v)
            except Exception:
                values[i] = np.nan
    return values

def parse_tiles_arg(arg: str) -> List[str]:
    if not arg:
        return []
    if any(ch in arg for ch in "*?[]"):
        return sorted(glob.glob(arg))
    return [p.strip() for p in arg.split(",") if p.strip()]

def sample_rasters_multi(points: List[Tuple[float,float]], tifs: List[str], band: int=1) -> np.ndarray:
    out = np.full(len(points), np.nan, dtype=np.float64)
    cnt = np.zeros(len(points), dtype=np.int32)
    sm = np.zeros(len(points), dtype=np.float64)
    for tif in tifs:
        try:
            with rasterio.open(tif) as src:
                arr = src.read(band); T = src.transform
                H, W = src.height, src.width; nodata = src.nodata
                for i, (x,y) in enumerate(points):
                    try:
                        r, c = rowcol(T, x, y)
                        if 0 <= r < H and 0 <= c < W:
                            v = arr[r, c]
                            if nodata is None or not np.isclose(v, nodata):
                                if not np.isnan(v):
                                    sm[i] += float(v); cnt[i] += 1
                    except Exception:
                        continue
        except Exception:
            continue
    mask = cnt > 0
    out[mask] = sm[mask] / cnt[mask]
    return out

def attach_worldclim(df: pd.DataFrame, bio_dir: str, biovars=(1,4,12)) -> pd.DataFrame:
    pts = to_points(df)
    for vid in biovars:
        path = os.path.join(bio_dir, f"wc2.1_30s_bio_{vid}.tif")
        vals = sample_raster(pts, path, 1)
        df[f"wc_bio{vid}"] = vals
    return df

def attach_elevation(df: pd.DataFrame, elev_tif: str):
    df["elevation_m"] = sample_raster(to_points(df), elev_tif, 1)
    return df

def attach_viirs_annual(df: pd.DataFrame, viirs_tif: str, col="viirs_annual"):
    df[col] = sample_raster(to_points(df), viirs_tif, 1)
    return df

def attach_viirs_monthly(df: pd.DataFrame, tiles_arg: str, tag: str=None):
    tifs = parse_tiles_arg(tiles_arg)
    if not tifs:
        return df
    vals = sample_rasters_multi(to_points(df), tifs, 1)
    suffix = tag if tag else "monthly"
    df[f"viirs_{suffix}"] = vals
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=None)
    ap.add_argument("--city_csv", type=str, default=None)
    ap.add_argument("--worldclim_bio_dir", type=str, default=None)
    ap.add_argument("--elev_tif", type=str, default=None)
    ap.add_argument("--viirs_annual_tif", type=str, default=None)
    ap.add_argument("--viirs_monthly_tiles", type=str, default=None)
    ap.add_argument("--viirs_monthly_tag", type=str, default=None)
    ap.add_argument("--output_csv", type=str, default=None)
    args = ap.parse_args()

    cfg = read_config(args)
    df = pd.read_csv(cfg.city_csv, encoding="utf-8")
    require_cols(df, ["city","country","iso2","iso3","lat","lng","admin_name","population"])

    if cfg.worldclim_bio_dir:
        print("WorldClim BIO (1,4,12)")
        df = attach_worldclim(df, cfg.worldclim_bio_dir, (1,4,12))
    if cfg.elev_tif:
        print("Elevation")
        df = attach_elevation(df, cfg.elev_tif)
    if cfg.viirs_annual_tif:
        print("VIIRS Annual")
        df = attach_viirs_annual(df, cfg.viirs_annual_tif, col="viirs_annual_ave")
    if cfg.viirs_monthly_tiles:
        print("VIIRS Monthly tiles")
        df = attach_viirs_monthly(df, cfg.viirs_monthly_tiles, cfg.viirs_monthly_tag)

    out = cfg.output_csv or str(Path(cfg.city_csv).with_name("city_features.csv"))
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Saved -> {out}")

if __name__ == "__main__":
    main()
