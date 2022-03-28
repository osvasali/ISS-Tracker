NAME ?= osvasali

all: build run

images:
        docker images | grep ${NAME}

ps:
        docker ps -a | grep ${NAME}

build:
        docker build -t ${NAME}/iss-tracker:midterm1 .

run:
        docker run --name "iss-tracker" -d -p 5027:5000 --rm -v \:/iss_tracker ${NAME}/iss-tracker:midterm1

pull:
        docker pull ${NAME}/iss-tracker:midterm1
