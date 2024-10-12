# from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
# from flask_cors import CORS
# from rag.core import RAG
# from embeddings import OpenAIEmbedding
# from semantic_router import SemanticRouter, Route
# from semantic_router.samples import productsSample, chitchatSample
# import google.generativeai as genai
# import openai
# from reflection import Reflection
from rag.core import RAG


rag=RAG(None,None,None,None)
print(rag.embeddingName)
# load_dotenv()
# # Access the key
# MONGODB_URI = os.getenv('MONGODB_URI')
# print(MONGODB_URI)
# DB_NAME = os.getenv('DB_NAME')
# DB_COLLECTION = os.getenv('DB_COLLECTION')
# LLM_KEY = os.getenv('GEMINI_KEY')
# EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') or 'keepitreal/vietnamese-sbert'
# OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
# OPEN_AI_EMBEDDING_MODEL = os.getenv('OPEN_AI_EMBEDDING_MODEL') or 'text-embedding-3-small'