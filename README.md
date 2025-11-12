# ufo-cis545

### Dataset Preparation Pipeline

##### Objective

The goal of this process is to create a city-level feature dataset. The goal dataset links cities to the following features:

- Climate variables
- Elevation
- Nighttime light intensity

##### Source Datasets

| Name                     | Dataset                                                      | Description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Base city dataset**    | [SimpleMaps World Cities](https://simplemaps.com/data/world-cities) | Contains coordinates, population, and country codes for all global cities. Used as the base dataset. |
| **Climate data**         | [WorldClim v2.1 (30 arc-second resolution)](https://www.worldclim.org/data/worldclim21.html) | Gridded global climate data. Used for extracting temperature and precipitation per city. |
| **Elevation data**       | [WorldClim Elevation (wc2.1_30s_elev.tif)](https://www.worldclim.org/data/worldclim21.html) | Gridded global elevation data.                               |
| **Nighttime light data** | [Earth Observation Group (EOG) VIIRS Annual VNL V2](https://eogdata.mines.edu/products/vnl/) | A consistently processed time series of annual global VIIRS nighttime lights. Produced from monthly cloud-free average radiance grids spanning 2012 to 2020. |

##### Extracted Features

| Column                                                       | Description                                       | Units     | Source              |
| ------------------------------------------------------------ | ------------------------------------------------- | --------- | ------------------- |
| `city`, `country`, `iso2`, `iso3`, `lat`, `lng`, `admin_name`, `population` | City metadata                                     | —         | SimpleMaps          |
| `wc_bio1`                                                    | Annual mean temperature                           | °C        | WorldClim BIO1      |
| `wc_bio4`                                                    | Temperature seasonality (standard deviation ×100) | —         | WorldClim BIO4      |
| `wc_bio12`                                                   | Annual precipitation                              | mm        | WorldClim BIO12     |
| `elevation_m`                                                | Elevation above sea level                         | m         | WorldClim Elevation |
| `viirs_annual_ave`                                           | Annual mean nighttime light intensity             | nW/cm²/sr | VIIRS VNL V2 Annual |

##### Python Process Script

All additional features other than those in the base city dataset are extracted based on city coordinates (`lat`, `lng`).

**Script file:** `build_city_features.py`

To run the script file, a config file is required. It's expected for user to specify the locations of the original data files.

Example configuration:

```json
{
  "city_csv": "./worldcities.csv",
  "worldclim_bio_dir": "./wc2.1_30s_bio/",
  "elev_tif": "./wc2.1_30s_elev.tif",
  "output_csv": "./city_features.csv"
}
```

