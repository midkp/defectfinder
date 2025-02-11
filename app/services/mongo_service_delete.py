# # mongo_service.py

# from pymongo import MongoClient
# from app.config import settings  # Assuming you have your MongoDB URI and DB name in settings

# class MongoService:
#     def __init__(self):
#         # Connect to MongoDB using the URI from config settings
#         self.client = MongoClient(settings.MONGO_URI)
#         self.db = self.client[settings.MONGO_DB_NAME]  # Use the DB name from settings

#     def get_collection(self, collection_name: str):
#         # Retrieve a collection from the database
#         return self.db[collection_name]

#     def insert_document(self, collection_name: str, document: dict):
#         # Insert a document into a collection
#         collection = self.get_collection(collection_name)
#         result = collection.insert_one(document)
#         return result.inserted_id

#     def find_documents(self, collection_name: str, query: dict = None):
#         # Find documents in a collection based on a query
#         collection = self.get_collection(collection_name)
#         return collection.find(query) if query else collection.find()

#     def update_document(self, collection_name: str, query: dict, update_data: dict):
#         # Update a document in a collection
#         collection = self.get_collection(collection_name)
#         result = collection.update_one(query, {"$set": update_data})
#         return result.modified_count

#     def delete_document(self, collection_name: str, query: dict):
#         # Delete a document from a collection
#         collection = self.get_collection(collection_name)
#         result = collection.delete_one(query)
#         return result.deleted_count
