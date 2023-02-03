import time
from mysql.connector import Error
import os
import pandas as pd
import pickle
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
from random import randint
from sentiment_analysis_tripadvisor.scripts.scraper.scrapy_tripadvisor_scraper.tripadvisor_scraper.spiders.restaurants_urls_scraper import TripAdvisorSpider
from sentiment_analysis_tripadvisor.scripts.scraper.scrapy_tripadvisor_scraper.tripadvisor_scraper.spiders.reviews_scraper import ReviewSpider
from sentiment_analysis_tripadvisor.scripts.preprocessor.global_processor import ProcessingPipeline
import scrapy
from scrapy.crawler import CrawlerProcess
from _scproxy import _get_proxy_settings

_get_proxy_settings()



default_args = {
    'owner': 'me',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'email': ['lgabagnou@gmail.com'],
    'email_on_failure': False,
    'retry_delay': timedelta(minutes=5),
}



def scraping_task(id="city"):
    table_json=f"{os.path.dirname(os.path.dirname(os.getcwd()))}+/data/{id}.json"
    spider = TripAdvisorSpider()
    crawler = scrapy.CrawlerProcess()
    crawler.crawl(spider)
    crawler.start()
    df = pd.DataFrame(spider.results)
    df.to_json(table_json)
def processing_task(table_json):
    ProcessingPipeline(table_json).run_pipeline()
def loading_task():






with DAG(
    'scrape_and_save_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=24),
    catchup=False,
) as dag:
# Create a PythonOperator task
    scrape_and_save_task = PythonOperator(
        task_id='scrape_and_save_task',
        python_callable=scrape_and_save_task,
        provide_context=True,
        dag=dag,
    )

scrape_and_save_task 

