# DMI_gribcatcher

This files will get grib wind data from DMI's api and convert it to grib data to go into OpenCpn - it will get the entire time lenght define by the bbox coordinates in the file.

just run with your API key as argument.

## Requirements
### requests - any version
### eccodes python lib > 1.7.1
#### eccodes lib > 2.36.0
### datetime - any version
### argparse - any version


## Running
Download GeoJSON data and convert to GRIB2.

options:
  -h, --help         show this help message and exit
  --api-key API_KEY  API key for accessing the weather data.
  --bbox BBOX        Bounding box of area to download - default is: 9.29,54.54,13.04,56.19(inner inner dansih waters).
