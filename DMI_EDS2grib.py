import requests
import eccodes as ec
from datetime import datetime, timedelta, timezone
import argparse
import os
from dotenv import load_dotenv
from tqdm import tqdm
import json

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, 'output_with_steps.grib2')

# Step 1: Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Download GeoJSON data and convert to GRIB2.")
parser.add_argument("--bbox", required=False, default="9.29,54.54,13.04,56.19", help="Bounding box of area to download - default is: 9.29,54.54,13.04,56.19(inner inner danish waters).")
parser.add_argument("--out-file", required=False, default=file_path, help="The location of the output file - default: os homedir")
parser.add_argument("--api-key", required=api_key==None, default=None, help="Overwrites the API_KEY located in .env")
args = parser.parse_args()

# Check if --api-key is set
if not (args.api_key == None):
    print("API Key overwritten")
    api_key = args.api_key

if args.out_file != "":
    file_path = args.out_file

print("Output file location: " + file_path)
print("Bounding box used: " + args.bbox)

# Step 2: Generate the dynamic datetime for the URL (current time UTC minus 1 hour)
current_time_utc_minus_1_hour = datetime.now(timezone.utc) - timedelta(hours=1)
datetime_string = current_time_utc_minus_1_hour.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

# Update the URL with the dynamic datetime and API key from .env file
url = f"https://dmigw.govcloud.dk/v1/forecastedr/collections/dkss_nsbs/cube?bbox={args.bbox}&parameter-name=wind-u,wind-v&datetime={datetime_string}%2F..&crs=crs84&f=GeoJSON&api-key={api_key}"

print(url)

# Step 3: Download GeoJSON data with a progress bar
response = requests.get(url, stream=True)

total_size = int(response.headers.get('content-length', 0))  # Get total file size
block_size = 1024  # 1 KB block size
tqdm_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

content = b""
for data in response.iter_content(block_size):
    tqdm_bar.update(len(data))
    content += data

tqdm_bar.close()

if response.status_code == 200:
    geojson_data = json.loads(content)
    print("GeoJSON data downloaded successfully.")
else:
    print("Failed to download GeoJSON data.")
    geojson_data = None

# Step 4: Parse GeoJSON and organize data by time step
if geojson_data:
    data_by_step = {}

    for feature in geojson_data.get("features", []):
        coordinates = feature["geometry"]["coordinates"]
        wind_u_value = feature["properties"].get("wind-u", 0.0)
        wind_v_value = feature["properties"].get("wind-v", 0.0)
        step_time = feature["properties"]["step"]

        if step_time not in data_by_step:
            data_by_step[step_time] = {"lats": [], "lons": [], "wind_u": [], "wind_v": []}

        data_by_step[step_time]["lons"].append(coordinates[0])
        data_by_step[step_time]["lats"].append(coordinates[1])
        data_by_step[step_time]["wind_u"].append(wind_u_value if wind_u_value is not None else 0.0)
        data_by_step[step_time]["wind_v"].append(wind_v_value if wind_v_value is not None else 0.0)

    # Step 5: Create a GRIB2 file with steps
    with open(file_path, "wb") as grib_file:
        for step_time, data in data_by_step.items():
            forecast_time = datetime.fromisoformat(step_time.replace("Z", "+00:00")).astimezone(timezone.utc)
            forecast_hour = int((forecast_time - datetime(2024, 8, 10, 0, 0, tzinfo=timezone.utc)).total_seconds() / 3600)
            dataDate = int(forecast_time.strftime("%Y%m%d"))
            refTime = int(forecast_time.strftime("%H%M"))

            # Creating wind-u field
            gid_u = ec.codes_grib_new_from_samples("regular_ll_sfc_grib2")
            ec.codes_set(gid_u, "discipline", 0)  # Meteorological products
            ec.codes_set(gid_u, "parameterCategory", 2)  # Momentum
            ec.codes_set(gid_u, "parameterNumber", 2)  # u-component of wind
            ec.codes_set(gid_u, "dataDate", dataDate)  # Set the date of the forecast
            ec.codes_set(gid_u, "dataTime", refTime)  # Set the data time
            ec.codes_set_values(gid_u, data["wind_u"])
            ec.codes_set(gid_u, "latitudeOfFirstGridPointInDegrees", min(data["lats"]))
            ec.codes_set(gid_u, "longitudeOfFirstGridPointInDegrees", min(data["lons"]))
            ec.codes_set(gid_u, "latitudeOfLastGridPointInDegrees", max(data["lats"]))
            ec.codes_set(gid_u, "longitudeOfLastGridPointInDegrees", max(data["lons"]))
            ec.codes_set(gid_u, "gridType", "regular_ll")
            ec.codes_set(gid_u, "Ni", len(set(data["lons"])))
            ec.codes_set(gid_u, "Nj", len(set(data["lats"])))
            ec.codes_write(gid_u, grib_file)
            ec.codes_release(gid_u)

            # Creating wind-v field
            gid_v = ec.codes_grib_new_from_samples("regular_ll_sfc_grib2")
            ec.codes_set(gid_v, "discipline", 0)  # Meteorological products
            ec.codes_set(gid_v, "parameterCategory", 2)  # Momentum
            ec.codes_set(gid_v, "parameterNumber", 3)  # v-component of wind
            ec.codes_set(gid_v, "dataDate", dataDate)  # Set the date of the forecast
            ec.codes_set(gid_v, "dataTime", refTime)  # Set the data time
            ec.codes_set_values(gid_v, data["wind_v"])
            ec.codes_set(gid_v, "latitudeOfFirstGridPointInDegrees", min(data["lats"]))
            ec.codes_set(gid_v, "longitudeOfFirstGridPointInDegrees", min(data["lons"]))
            ec.codes_set(gid_v, "latitudeOfLastGridPointInDegrees", max(data["lats"]))
            ec.codes_set(gid_v, "longitudeOfLastGridPointInDegrees", max(data["lons"]))
            ec.codes_set(gid_v, "gridType", "regular_ll")
            ec.codes_set(gid_v, "Ni", len(set(data["lons"])))
            ec.codes_set(gid_v, "Nj", len(set(data["lats"])))
            ec.codes_write(gid_v, grib_file)
            ec.codes_release(gid_v)

    print("GRIB2 file created successfully with time steps as 'output_with_steps.grib2'")
