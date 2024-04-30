import pandas as pd
from pymongo import MongoClient


mongo_uri = "mongodb+srv://tanmaykulkarni:password@bapproject.sjdqrax.mongodb.net/?retryWrites=true&w=majority&appName=BapProject"


def insert_data_to_mongodb(file_path, collection_name):
    
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

    
    data = df.to_dict(orient='records')
    
    
    client = MongoClient(mongo_uri)
    
    
    db = client['BapProject']
    
    
    collection = db[collection_name]
    
    
    collection.insert_many(data)
    
    
    client.close()


files = {
    "IT_COMPS.csv": "it_comps_collection",
    "SEM-II-EXTC-CSDS.csv": "sem_ii_extc_csds_collection",
    "all.xlsx": "all_collection"
}


for file, collection in files.items():
    insert_data_to_mongodb(file, collection)
