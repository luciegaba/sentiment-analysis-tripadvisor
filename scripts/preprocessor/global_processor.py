
# On sépare la premiere liste (avec prix et cuisines) en deux listes. Le critère pour différencier le prix et le type de cuisine est la présence du symbole €. 
from geopy.geocoders import Nominatim
from utils import get_digits
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf



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
        self.df = self.df.select("average note",col("average note").cast('double').alias("average note"))
        self.df = self.df.select("number reviews",col("number reviews").cast('integer').alias("number reviews"))

    def extract_tripadvisor_rank(self):
        get_digits_udf = udf(get_digits, IntegerType())
        self.df = self.df.withColumn("tripadvisor_rank", get_digits_udf(self.df["tripadvisor rank"]))

    def separate_price_and_cuisine(self):
        
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
                    price=elem
                else:
                    cuisine.append(elem)
            return price, cuisine
        
        udf_separate_price_and_cuisine = udf(separate_price_and_cuisine, StructType([
            StructField("price", ArrayType(StringType())),
            StructField("cuisine", ArrayType(StringType()))
        ])) 
        self.df = self.df.withColumn("price", udf_separate_price_and_cuisine("price and cuisines").price) 
        self.df = self.df.withColumn("cuisine", udf_separate_price_and_cuisine("price and cuisines").cuisine)

    def geocode_location(self):
        def geocode_address(address,timeout=10):
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

        geocode_udf = udf(geocode_address, StructType([StructField("latitude", DoubleType()), StructField("longitude", DoubleType())]))
        self.df = self.df.withColumn("coordinates", geocode_udf("location"))