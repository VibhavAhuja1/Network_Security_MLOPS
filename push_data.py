import os
import sys
import json

import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)  # ✅ reuse client
            logger.info("MongoDB client initialized successfully")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logger.info(f"Converted CSV to {len(records)} records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            col = self.mongo_client[database][collection]
            col.insert_many(records)
            logger.info(f"Inserted {len(records)} records into {database}.{collection}")
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == '__main__':
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "Network_Vibhav"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(file_path=FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"Inserted {no_of_records} records successfully")