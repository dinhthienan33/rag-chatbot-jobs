import pandas as pd
import pymongo

class CSVToMongoDB:
    def __init__(self, mongodb_uri: str, db_name: str, collection_name: str):
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def ingest_csv(self, csv_file_path: str):
        """
        Ingest a CSV file into the MongoDB collection.

        Args:
        csv_file_path (str): The path to the CSV file.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Convert DataFrame to a list of dictionaries
            data = df.to_dict(orient='records')

            # Insert data into MongoDB collection
            self.collection.insert_many(data)
            print(f"Successfully ingested {len(data)} records into MongoDB.")
        except Exception as e:
            print(f"Error ingesting CSV to MongoDB: {e}")

# Example usage
if __name__ == "__main__":
    mongodb_uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
    db_name = "your_database_name"
    collection_name = "your_collection_name"
    csv_file_path = "path/to/your/csvfile.csv"

    ingestor = CSVToMongoDB(mongodb_uri, db_name, collection_name)
    ingestor.ingest_csv(csv_file_path)