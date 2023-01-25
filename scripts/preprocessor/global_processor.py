
# On sépare la premiere liste (avec prix et cuisines) en deux listes. Le critère pour différencier le prix et le type de cuisine est la présence du symbole €. 
from geopy.geocoders import Nominatim
from utils import get_digits
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, DoubleType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, regexp_replace
from scripts.preprocessor.text_processor import clean_text_sentiment_analysis

class ETLPipeline():
    def __init__(self, json_filepath):
        """
        Initialize an ETLPipeline object with a json filepath.
        :param json_filepath: string, the filepath of the json file to be processed
        """

        self.json_filepath = json_filepath
        self.spark = SparkSession.builder.appName("ETL").getOrCreate()
        self.df = self.spark.read.option("multiline","true").json(self.json_filepath)

    def cast_columns(self):
        """ Cast good columns types (especially for numeric ones)
        """
        get_digits_udf = udf(get_digits, DoubleType())
        self.df = self.df.withColumn("average_note", regexp_replace(col("average_note"), ",", "."))
        self.df = self.df.withColumn("ranking", get_digits_udf(self.df["ranking"]))
        self.df = self.df.withColumn("average_note", get_digits_udf(self.df["average_note"]))
        self.df = self.df.withColumn("number_reviews", get_digits_udf(self.df["number_reviews"]))

    def separate_price_and_cuisine(self):
        
        def _separate_price_and_cuisine(elements):
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
                    price=elem
                else:
                    cuisine.append(elem)
            return price, cuisine

        # On renseigne ce schéma dans l' udf ainsi que la fonction
        udf_separate_price_and_cuisine = udf(_separate_price_and_cuisine, StructType([
            StructField("price", ArrayType(StringType())),
            StructField("cuisine", ArrayType(StringType()))]))


        self.df = self.df.withColumn("price", udf_separate_price_and_cuisine("price and cuisines").price[0]) 
        self.df = self.df.withColumn("cuisine", udf_separate_price_and_cuisine("price and cuisines").cuisine)
        self.df = self.df.drop(*["price and cuisines"])


    def geocode_location(self):

        def _geocode_address(address,timeout=10):
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
                return (location.latitude, location.longitude)
            else:
                return (None, None)

        geocode_udf = udf(_geocode_address, StructType([StructField("latitude", DoubleType()), StructField("longitude", DoubleType())]))
        self.df = self.df.withColumn("coordinates", geocode_udf("location"))

    
    def cleaning_text(self):
        """ Cleaning pipeline that seperates ratings from reviews and clean reviews using Spacy and NLTK 
        (remove stopwords, regex, lemmatization = reducing a word to its base or root form)
        
        """
        udf_text_cleaning = udf(clean_text_sentiment_analysis, StructType([
    StructField("reviews", ArrayType(StringType())),
    StructField("ratings", ArrayType(StringType()))]))
        self.df=self.df.withColumn("clean_reviews", udf_text_cleaning("reviews").reviews)
        self.df=self.df.withColumn("ratings", udf_text_cleaning("reviews").ratings)