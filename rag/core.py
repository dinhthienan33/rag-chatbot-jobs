import pymongo
import google.generativeai as genai  # gemini
from IPython.display import Markdown
import textwrap
from embeddings import SentenceTransformerEmbedding, EmbeddingConfig

class RAG():
    def __init__(self, 
                 mongodbUri: str,
                 dbName: str,
                 dbCollection: str,
                 llm,
                 embeddingName: str = 'thenlper/gte-large'):
        self.mongo_uri = mongodbUri
        self.dbName = dbName
        self.collection_name = dbCollection
        self.client = None
        self.db = None
        self.collection = None
        self.embedding_model = SentenceTransformerEmbedding(
            EmbeddingConfig(name=embeddingName)
        )
        self.llm = llm
        self.get_mongo_client()

    def get_mongo_client(self):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, appname="devrel.content.python")
            print("Connection to MongoDB successful")
            self.db = self.client[self.dbName]
            self.collection = self.db[self.collection_name]
            print("Done !!")
        except pymongo.errors.ConnectionFailure as e:
            print(f"Connection failed: {e}")
            return None

    def get_embedding(self, text):
        if not text.strip():
            return []

        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def vector_search(self, user_query: str, limit=4):
        """
        Perform a vector search in the MongoDB collection based on the user query.

        Args:
        user_query (str): The user's query string.

        Returns:
        list: A list of matching documents.
        """

        # Generate embedding for the user query
        query_embedding = self.get_embedding(user_query)

        if query_embedding is None:
            return "Invalid query or embedding generation failed."

        # Define the vector search pipeline
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 400,
                "limit": limit,
            }
        }

        unset_stage = {
            "$unset": "embedding"
        }

        # project_stage = {
        #     "$project": {
        #         "_id": 0,
        #         "title": 1,
        #         # "product_specs": 1,
        #         "color_options": 1,
        #         "current_price": 1,
        #         "product_promotion": 1,
        #         "score": {
        #             "$meta": "vectorSearchScore"
        #         }
        #     }
        # }

        pipeline = [vector_search_stage, unset_stage]

        # Execute the search
        results = self.collection.aggregate(pipeline)

        return list(results)

    def generate_content(self, prompt):
        return self.llm.generate_content(prompt)

    @staticmethod
    def _to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))