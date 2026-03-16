# Weather Data ETL Pipeline using Apache Airflow

## Project Overview

This project demonstrates an **ETL (Extract, Transform, Load) pipeline** built using **Apache Airflow**.

The pipeline extracts real-time weather data from the **OpenWeatherMap API**, transforms the data using **Python and Pandas**, and loads the processed data into an **AWS S3 bucket**.

The workflow is orchestrated using **Apache Airflow** and runs on an **AWS EC2 instance**.

---

## Architecture

OpenWeather API
↓
HttpSensor (Check API availability)
↓
HttpOperator (Extract weather data)
↓
PythonOperator (Transform data using Pandas)
↓
S3Hook (Upload processed data)
↓
AWS S3 Bucket

---

## Airflow Dag




---

## Technologies Used

- Apache Airflow
- Python
- Pandas
- AWS EC2
- AWS S3
- OpenWeatherMap API

---

## Project Structure

weather-airflow-etl/
│
├── dags/
│ └── weather_dag.py
├── README.md
└── .gitignore


---

## Pipeline Workflow

### 1. API Availability Check
`HttpSensor` checks whether the weather API is available before running the pipeline.

### 2. Data Extraction
`HttpOperator` extracts weather data from the OpenWeatherMap API.

### 3. Data Transformation
A `PythonOperator` processes the extracted data:

- Converts temperature from **Kelvin to Fahrenheit**
- Extracts useful fields such as:
  - temperature
  - humidity
  - wind speed
  - pressure
  - sunrise and sunset times
- Converts the data into a **Pandas DataFrame**
- Saves the data as a CSV file

### 4. Data Loading
The transformed CSV file is uploaded to an **AWS S3 bucket** using the `S3Hook`.

---

## Airflow Configuration

### Airflow Variables

The project uses **Airflow Variables** to avoid storing secrets in the code.

Variables used:

| Variable Name | Description |
|---|---|
weather_api_key | OpenWeatherMap API key |
weather_city | City name (example: Pune) |
weather_bucket | AWS S3 bucket name |

These can be configured in the Airflow UI:

Admin → Variables
---

### Airflow Connection

Connection used:

Conn Id: weathermap_api
Conn Type: HTTP
Host: https://api.openweathermap.org

## I have attached setup file in which I have mentioned some of the troubleshoot that I have done also.

---

## Output




---


## Learning Outcomes

### This project demonstrates:

- Building an ETL pipeline with Apache Airflow

- Using Airflow operators and hooks

- Extracting data from APIs

- Data transformation using Pandas

- Loading data to AWS S3

- Running Airflow on AWS EC2




