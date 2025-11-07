# Datasets

## 原始数据集

### UFO Sightings

https://www.kaggle.com/datasets/NUFORC/ufo-sightings

| datetime | city | state | country | shape | duration (seconds) | duration (hours/min) | comments | date posted | latitude | longitude |
| -------- | ---- | ----- | ------- | ----- | ------------------ | -------------------- | -------- | ----------- | -------- | --------- |

## 其他数据来源

### World cities database

https://simplemaps.com/data/world-cities

| city | city_ascii | lat  | lng  | country | iso2 | iso3 | admin_name | capital | population | id   |
| ---- | ---------- | ---- | ---- | ------- | ---- | ---- | ---------- | ------- | ---------- | ---- |

不需要额外清洗的城市数据集，同时包含了人口信息

### Annual VNL V2

https://eogdata.mines.edu/products/vnl/

包含了城市夜间光亮度的数据，同时滤去了临时光源等干扰因素

### WorldClim Bioclimatic variables

https://www.worldclim.org/data/worldclim21.html

wc2.1_30s_bio

### WorldClim Elevation variables

https://www.worldclim.org/data/worldclim21.html

wc2.1_30s_elev



## 最终清洗后的数据集（city_features）

| 列名                 | 含义                                                         | 来源                             |
| -------------------- | ------------------------------------------------------------ | -------------------------------- |
| **city**             | 城市名（带重音符、原始写法）                                 | World cities database            |
| **city_ascii**       | 城市名的 ASCII 版本（无重音符，比如 *São Paulo* → *Sao Paulo*） | World cities database            |
| **lat**              | 纬度（°）                                                    | World cities database            |
| **lng**              | 经度（°）                                                    | World cities database            |
| **country**          | 国家名（英文）                                               | World cities database            |
| **iso2**             | 国家 ISO 2 位代码（如 US, GB）                               | World cities database            |
| **iso3**             | 国家 ISO 3 位代码（如 USA, GBR）                             | World cities database            |
| **admin_name**       | 州/省名（行政区划）                                          | World cities database            |
| **capital**          | 是否为首都（可能是 "primary"、"admin" 或空）                 | World cities database            |
| **population**       | 城市人口（估算）                                             | World cities database            |
| **id**               | 城市唯一 ID（原文件中自带）                                  | World cities database            |
| **wc_bio1**          | **年平均温度**（单位 °C）                                    | WorldClim `wc2.1_30s_bio_1.tif`  |
| **wc_bio4**          | **温度季节性（变异系数×100）** — 反映年内温度波动强度        | WorldClim `wc2.1_30s_bio_4.tif`  |
| **wc_bio12**         | **年降水量**（mm）                                           | WorldClim `wc2.1_30s_bio_12.tif` |
| **elevation_m**      | **海拔高度**（米）                                           | WorldClim `wc2.1_30s_elev.tif`   |
| **viirs_annual_ave** | **年度平均夜光强度**（单位 nW/cm²/sr）                       | VIIRS  `average_masked.tif`      |

