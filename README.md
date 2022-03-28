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

### Source
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

## Build Containerized App

The image may built by using either the Dockerfile or Makefile in this repository.
Replace `<username>` and `<tag>` with your own username and tag.
You may replace `<your port number>` with 5027 or another port not in use

### Using Makefile
#### Enter the following to pull and run a pre-containerized copy of the app

```
$ make pull
$ make run
```
####  Enter the following to build and run new image
```
$ NAME="<username>" make build
$ NAME="<username>" make run
```

### Using Dockerfile
#### Enter the following pull and run a pre-containerized copy of the app

```
$ docker pull osvasali/iss-tracker:midterm1
$ docker run --name "iss-tracker" -d -p <your port number>:5000 osvasali/iss-tracker:midterm1
```
####  Enter the following to build and run new image
```
$ docker build -t <username>/iss-tracker:<tag> .
$ docker run --name "iss-tracker" -d -p <your port number>:5000 osvasali/iss-tracker:midterm1
```

## How to Interact with the Application

The following is a template of how to interact with the application replacing  `<your port number>` with the port number you are using and
`<route>` with the one of the routes shown in this section.

```
$ curl localhost:<your port number>/<route>
```

#### /help - shows list of routes

```
$ curl localhost:<your port number>/help
```
 
Output below explains how to download the data and lists of the routes:

```
 
FIRST LOAD DATA USING THE FOLLOWING PATH: /load -X POST

    IF THERE ARE ERRORS LOAD THE DATA ONCE MORE


    Navigation:

    Use the following routes to access the data:
      1.  /epochs
          #lists all epochs
      2.  /epochs/<epoch>
          #data for specific epoch
      3.  /countries
          #lists all countries
      4.  /countries/<country>
          #data for specific country
      5.  /countries/<country>/regions
          #lists all regions
      6.  /countries/<country>/regions/<regions>
          #data for specific region
      7.  /countries/<country>/regions/<regions>/cities
          #lists all cities
      8. /countries/<country>/regions/<regions>/cities/<cities>
          #data for specific city

```

#### /load - loads data from XML files

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

The following output is an error message that appears when '-X POST' is accidentally omitted

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
````

#### /epochs - lists all epochs

```
$ curl localhost:<your port number>/epochs
```
 
Sample output of epoch names:

```
...
2022-057T10:12:56.869Z
2022-057T10:16:56.869Z
2022-057T10:20:56.869Z
2022-057T10:24:56.869Z
2022-057T10:28:56.869Z
2022-057T10:32:56.869Z
2022-057T10:36:56.869Z
2022-057T10:40:56.869Z
2022-057T10:44:56.869Z
2022-057T10:48:56.869Z
2022-057T10:52:56.869Z
2022-057T10:56:56.869Z
2022-057T11:00:56.869Z
2022-057T11:04:56.869Z
2022-057T11:08:56.869Z
2022-057T11:12:56.869Z
2022-057T11:16:56.869Z
2022-057T11:20:56.869Z
2022-057T11:24:56.869Z
2022-057T11:28:56.869Z
2022-057T11:32:56.869Z
2022-057T11:36:56.869Z
2022-057T11:40:56.869Z
2022-057T11:44:56.869Z
2022-057T11:48:56.869Z
2022-057T11:52:56.869Z
2022-057T11:56:56.869Z
2022-057T12:00:00.000Z
...
```

The list above may be much longer.

#### /epochs/<epoch> data for specific epoch

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries - lists all countries

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries/<country> - data for specific country

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries/<country>/regions - lists all regions

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries/<country>/regions/<regions> - data for specific region

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### / ---- - loads data from XML files

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries/<country>/regions/<regions>/cities - lists all cities

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```

#### /countries/<country>/regions/<regions>/cities/<cities> - data for specific city

```
$ curl localhost:<your port number>/load -X POST
```
 
Output below is confirmation that the functions in app.py can now use the XML data:

```
Data has been loaded
```
