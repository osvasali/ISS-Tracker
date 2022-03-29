NAME ?= osvasali

all: build run

images:
        docker images | grep ${NAME}

ps:
        docker ps -a | grep ${NAME}

build:
        docker build -t ${NAME}/iss-tracker:midterm1 .

run:
        docker run --name "iss-tracker" -d -p 5027:5000 ${NAME}/iss-tracker:midterm1

pull:
        docker pull ${NAME}/iss-tracker:midterm1
        
positions: 
        wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
        
sightings:
        wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA06.xml
