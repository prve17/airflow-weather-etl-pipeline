import json
from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http  import HttpSensor
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
import pandas as pd

api_key = Variable.get("weather_api_key")
city_name = Variable.get("weather_city")
bucket_name = Variable.get("weather_bucket")

def kelvin_to_farenheit(kelvin_temp):
    farenheit_temp = (kelvin_temp - 273.15) * 9/5 + 32
    return farenheit_temp

def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids='extract_weather_data')
    city = data['name']
    weather_description = data['weather'][0]['description']
    temp_farenheit = kelvin_to_farenheit(data['main']['temp'])
    feels_like_farenheit = kelvin_to_farenheit(data['main']['feels_like'])
    min_temp_farenheit = kelvin_to_farenheit(data['main']['temp_min'])
    max_temp_farenheit = kelvin_to_farenheit(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature (F)": temp_farenheit,
        "Feels Like (F)": feels_like_farenheit,
        "Minimum Temp (F)": min_temp_farenheit,
        "Maximum Temp (F)": max_temp_farenheit,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Time of Record": time_of_record,
        "Sunrise (Local Time)": sunrise_time,
        "Sunset Time (Local Time)": sunset_time
    }

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_Pune_' + dt_string
    file_name = f"{dt_string}.csv"
    df_data.to_csv(file_name, index=False)

    s3_hook = S3Hook()

    s3_hook.load_file(
        filename=file_name,
        key=file_name.split('/')[-1],
        bucket_name=bucket_name,
        replace=False
    )


default_args = {
    'owner': 'airflow',
    'depends_on_past':False,
    'start_date':datetime(2026,1,9),
    'email':{'simpy1221@gmail.com'},
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':2,
    'retry_delay':timedelta(minutes=2)
}

with DAG('weather_dag',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False) as dag:


        is_weather_api_ready= HttpSensor(
            task_id = 'is_weather_api_ready',
            http_conn_id = 'weathermap_api',
            endpoint=f'/data/2.5/weather?q={city_name}&appid={api_key}'
        )

        extract_weather_data = HttpOperator(
            task_id = 'extract_weather_data',
            http_conn_id = 'weathermap_api',
            endpoint=f'/data/2.5/weather?q={city_name}&appid={api_key}',
            method='GET',
            response_filter=lambda r: json.loads(r.text),
            log_response=True
        )

        transform_load_weather_data = PythonOperator(
            task_id = 'transform_load_weather_data',
            python_callable =  transform_load_data
        )

        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
