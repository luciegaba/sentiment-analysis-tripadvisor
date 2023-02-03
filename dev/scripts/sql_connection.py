import logging
logging.basicConfig(level=logging.INFO)
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine




def test_connection_mysql(config):
    """
    Test connection to MySQL database using provided configuration.
    """
    try:
        connection = mysql.connector.connect(
            host=config.get('POSTGRES_HOST'),
            database=config.get('POSTGRES_DB'),
            user=config.get('POSTGRES_PASSWORD'),
            password=config.get('POSTGRES_PASSWORD')
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            logging.info("You're connected to database: ", record)
    except Error as e:
        logging.info("Error while connecting to MySQL", e)


def generate_table(config,name_table):
    connection = mysql.connector.connect(
            host=config.get('POSTGRES_HOST'),
            database=config.get('POSTGRES_DB'),
            user=config.get('POSTGRES_PASSWORD'),
            password=config.get('POSTGRES_PASSWORD'))
    cursor = connection.cursor()
    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name_table}(
                average_note decimal(10,4),
                location string,
                name string,
                number_reviews decimal(10,4),
                ranking decimal(10,4),
                reviews ARRAY string,
                url string,
                price ARRAY string,
                cuisine ARRAY string,
                longitude decimal(10,4),
                latitude decimal(10,4),
                clean_reviews ARRAY string,
                ratings ARRAY string
            );
            TRUNCATE TABLE {name_table};

        """
    )
    connection.commit()


