import pandas as pd

edu_path = "global_education_data.csv"
google_country_path = "country.csv" 
out_path = "global_education_modified.csv"

edu = pd.read_csv(edu_path, encoding="latin1")
google_countries = pd.read_csv(google_country_path, encoding="latin1")

def normalize_country_name(s):
    if not isinstance(s, str):
        return s
    s = s.strip()
    if s.lower().startswith("the "):
        s = s[4:]
    return s

edu_country_col = "Countries and areas"

edu["country_key"] = edu[edu_country_col].apply(normalize_country_name)
google_countries["country_key"] = google_countries["name"].apply(normalize_country_name)

google_for_merge = google_countries[["country_key", "latitude", "longitude"]].rename(
    columns={
        "latitude": "Latitude_new",
        "longitude": "Longitude_new"
    }
)

merged = edu.merge(google_for_merge, on="country_key", how="left")

missing = merged[merged["Latitude_new"].isna()][edu_country_col].unique()
print("Failed to merge: ", len(missing))

old_lat_col = "Latitude "
old_lon_col = "Longitude"

merged["Latitude_old"] = merged[old_lat_col]
merged["Longitude_old"] = merged[old_lon_col]

merged[old_lat_col] = merged["Latitude_new"]
merged[old_lon_col] = merged["Longitude_new"]

merged = merged.drop(columns=["country_key", "Latitude_new", "Longitude_new"])

merged.to_csv(out_path, index=False, encoding="utf-8")
print("Output path: ", out_path)
