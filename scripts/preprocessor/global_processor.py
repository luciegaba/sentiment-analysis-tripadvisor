import os
from geopy.geocoders import Nominatim
from scripts.utils import get_digits
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    DoubleType,
)
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, regexp_replace,mean
from scripts.preprocessor.text_processor import clean_text_sentiment_analysis


########## EXECUTION
# pipeline = ETLPipeline(json_filepath)
# pipeline.run_pipeline()


def geocode_address(address, timeout=10):
    """
    Given an address, this function uses the geopy library to geocode the address and return
    its latitude and longitude.
    :param address: string, the address to geocode
    :param timeout: int, the maximum time (in seconds) to wait for the geocoding service
    :return: a tuple of floats (latitude, longitude)
    """
    geolocator = Nominatim(user_agent="geo_pyspark", timeout=timeout)
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return (None, None)


def separate_price_and_cuisine(elements):
    """
    Given a list of elements, this function separates the elements that contain the symbol '€'
    into a list of prices and the rest of the elements into a list of cuisines.
    :param elements: list of elements (strings)
    :return: a tuple of two lists, one for prices and one for cuisines
    """
    price = []
    cuisine = []
    for elem in elements:
        if "€" in elem:
            price.append(elem)
        else:
            cuisine.append(elem)
    return price, cuisine


class ProcessingPipeline:
    def __init__(self, json_filepath):
        """
        Initialize an ETLPipeline object with a json filepath.
        :param json_filepath: string, the filepath of the json file to be processed
        Notice that user-functions begin with "_"
        """

        self.json_filepath = json_filepath
        self.spark = SparkSession.builder.appName("ETL").getOrCreate()
        self.df = self.spark.read.option("multiline", "true").json(self.json_filepath)

    def cast_columns(self):
        """Cast good columns types (especially for numeric ones) and fillna"""
        get_digits_udf = udf(get_digits, DoubleType())
        self.df = self.df.withColumn(
            "average_note", regexp_replace(col("average_note"), ",", ".")
        )
        self.df = self.df.withColumn("ranking", get_digits_udf(self.df["ranking"]))
        self.df = self.df.withColumn(
            "average_note", get_digits_udf(self.df["average_note"])
        )
        self.df = self.df.withColumn(
            "number_reviews", get_digits_udf(self.df["number_reviews"])
        )

        self.df = self.df.na.fill(
            {"average_note": 0, "ranking": 0, "number_reviews": 0}
        )

    def _separate_price_and_cuisine(self):
        """ Apply separate_price_and_cuisine to PySpark df"""
        udf_separate_price_and_cuisine = udf(
            separate_price_and_cuisine,
            StructType(
                [
                    StructField("price", ArrayType(StringType())),
                    StructField("cuisine", ArrayType(StringType())),
                ]
            ),
        )
        self.df = self.df.withColumn(
            "price", udf_separate_price_and_cuisine("price_and_cuisines").price
        )
        self.df = self.df.withColumn(
            "cuisine", udf_separate_price_and_cuisine("price_and_cuisines").cuisine
        )
        self.df = self.df.drop(*["price_and_cuisines"])

    def _geocode_location(self):
        """ Apply geocode_location to PySpark df + fillna"""
        geocode_udf = udf(
            geocode_address,
            StructType(
                [
                    StructField("longitude", DoubleType()),
                    StructField("latitude", DoubleType()),
                ]
            ),
        )
        self.df = self.df.repartition(20)
        self.df = self.df.withColumn("longitude", geocode_udf("location").longitude)
        self.df = self.df.withColumn("latitude", geocode_udf("location").latitude)

        avg_longitude = self.df.agg(mean(self.df["longitude"])).first()[0]
        avg_latitude = self.df.agg(mean(self.df["latitude"])).first()[0]
    
        self.df = self.df.fillna(avg_longitude, subset="longitude")
        self.df = self.df.fillna(avg_latitude, subset="latitude")

    def cleaning_text(self):
        """Cleaning pipeline that seperates ratings from reviews and clean reviews using Spacy and NLTK
        (remove stopwords, regex, lemmatization = reducing a word to its base or root form)
        """
        udf_text_cleaning = udf(
            clean_text_sentiment_analysis,
            StructType(
                [
                    StructField("reviews", ArrayType(StringType())),
                    StructField("ratings", ArrayType(StringType())),
                ]
            ),
        )
        self.df = self.df.withColumn(
            "clean_reviews", udf_text_cleaning("reviews").reviews
        )
        self.df = self.df.withColumn("ratings", udf_text_cleaning("reviews").ratings)

    def save_json(self, save_path):
        """
        save the dataframe in json format
        :param save_path: string, the path to save the json file
        """
        self.df.write.json(save_path, mode="overwrite")

    def run_pipeline(self):
        """
        Execute the different steps of the ETL pipeline
        """
        self.cast_columns()
        self._separate_price_and_cuisine()
        self._geocode_location()
        self.cleaning_text()
        self.save_json(
            os.path.join(os.path.dirname(self.json_filepath), "clean_data.json")
        )
