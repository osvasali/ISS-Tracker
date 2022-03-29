FROM python:3.9

RUN mkdir /app
RUN pip3 install --user xmltodict
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY XMLsightingData_citiesUSA06.xml /app
COPY ISS.OEM_J2K_EPH.xml /app
COPY . /app

ENTRYPOINT ["python"]
