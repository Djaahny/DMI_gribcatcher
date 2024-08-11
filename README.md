# DMI_gribcatcher

## Intro
This little tool was written by "Djaahny" and ChatGPT - it downloads GeoJson info on wind forecast from DMI.dk's API and converts it a GRIB file that can be used in OpenCPN's grib and weather routing. The software is provided as is - enjoy or don't.  

This files will get grib wind data from DMI's api and convert it to grib data to go into OpenCpn - it will get the entire time lenght of the forecast defined by the bbox coordinates in the file.

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
    --help         show this help message and exit  
    --api-key API_KEY  API key for accessing the weather data.  
    --bbox BBOX        Bounding box of area to download - default is: 9.29,54.54,13.04,56.19(inner inner dansih waters).  
    
    For most of Denamrk use this Bounding box - or for Sjællannd and Fyn - use the default:  
    
    >> python3.11 DMI_EDS2grib.py --bbox=9.11,53.51,15.22,57.46 --api-key=xxxx

  #### Bounding box tool:  
    https://boundingbox.klokantech.com/
