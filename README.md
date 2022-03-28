# ISS Tracker - Positions and Sightings

This application outputs data for the position and velocity of the International Space Station (ISS), as well as the places around the world where the ISS was sighted.
The application does this by collecting data from XML files and making them easier for a person to read the country, region, city, time, 
position in cartesian coordinates, units of velocity, magnitude of velocity, and other details associated with the ISS for a particular sighting or epoch.   

## Files
##### Scripts
- ```app.py```: this is the python application that uses GET and POST fucntions that output information about the ISS 
- ```test_app.py```: tests the functionality of the routes created in app.py
##### Container files
- ```Dockerfile```: creates a an a docker image needed to containerize the application
- ```Makefile```: automation tool that serves as a second option to create a container
- ```requirements.txt```: captures the required libraries and packages for the application in Dockerfile
##### XML files to be used as examples:
- ```ISS.OEM_J2K_EPH.xml```: an XML with ISS positional data set that describes each epoch
- ```XMLsightingData_citiesUSA06.xml```: an XML file with ISS sighting data set (country - > region -> city)

The XML files above come from NASA's official website found [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq).

### Get files

##### Clone the contents of this repository by entering what follows the $ into a terminal or SCP client:

```
$ git clone https://github.com/osvasali/ISS-Tracker
```

(other methods for cloning a repository are described here [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository))

#### XML file download
- Required data files: `ISS.OEM_J2K_EPH.xml` and `XMLsightingData_citiesUSA06.xml`
- Download the data [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq)
    - ```ISS.OEM_J2K_EPH.xml```: Titled "Public Distribution"
    - ```XMLsightingData_citiesUSA06.xml```: Titled "XMLsightingData_citiesUSA06"

##### Download the files by entering what follows the $ into a terminal or SCP client:

```
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA06.xml
```

