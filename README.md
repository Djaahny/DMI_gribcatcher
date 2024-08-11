# DMI gribcatcher

## Intro
This little tool was written by "Djaahny", "Bamsen" and ChatGPT - it downloads GeoJson info on wind forecast from DMI.dk's API and converts it a GRIB file that can be used in OpenCPN's grib and weather routing. The software is provided as is - enjoy or don't.  

This files will get grib wind data from DMI's api and convert it to grib data to go into OpenCpn - it will get the entire time lenght of the forecast defined by the bbox coordinates in the file.

# Setting up on Windows
1. Install [Docker](https://www.docker.com/)
2. Create `.env` file and put `API_KEY=<api_token_here>` 
## Running on Windows
1. Run `dmi_util test` in **COMMAND PROMPT**
2. Or use VSCode and press `Ctrl+Shift+P` and search for `Tasks: Run Task` then select it, and run `DMI Test`
### Args on Windows
1. Use `dmi_util peek` in **COMMAND PROMPT**
2. Or use VSCode and press `Ctrl+Shift+P` and search for `Tasks: Run Task` and selec it, and run `DMI Peek`
3. Then you can run `python DMI_EDS2grib.py <args>`

# Setting up on Linux
1. Run `chmod +x setup.sh`
2. Run `setup.sh`
3. Open up `.env` and put `API_KEY=<api_token_here>` 
## Running on Linux
1. In bash run `source venv/bin/activate`
2. Run `python DMI_EDS2grib.py <args>`
2. Or use VSCode and press `Ctrl+Shift+P` and search for `Tasks: Run Task` then select it, and run `DMI Test`

## Program Info
Downloads a GeoJSON file and converts it to GRIB2.  
  
options:  
    --help         show this help message and exit  
    --bbox BBOX        Bounding box of area to download - default is: 9.29,54.54,13.04,56.19 (inner inner danish waters).  
    --out-file OUT_FILE  The location of the output file - default: os homedir  

  ### Example for Denmark
    For most of Denmark use this Bounding box:
    `>> python3.11 DMI_EDS2grib.py --bbox=9.11,53.51,15.22,57.46`
    For Sjællannd and Fyn use the default.  

  ### Getting the api key:
  https://dmiapi.govcloud.dk/

  ### Bounding box tool:  
    https://boundingbox.klokantech.com/
