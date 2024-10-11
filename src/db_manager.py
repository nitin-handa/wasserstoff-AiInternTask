# src/db_manager.py
from pymongo import MongoClient
from bson.objectid import ObjectId  
from logger import logger
from datetime import datetime
import os

class DBManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="pdf_pipeline"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db['documents']
            logger.info("Connected to MongoDB successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def insert_metadata(self, metadata):
        try:
            # Check if document already exists based on document_name
            existing_document = self.collection.find_one({'document_name': metadata['document_name']})
            if existing_document:
                logger.warning(f"Document {metadata['document_name']} already exists. Skipping insertion.")
                return None

            # Convert datetime objects to strings
            for key, value in metadata.items():
                if isinstance(value, datetime):
                    metadata[key] = value.isoformat()

            result = self.collection.insert_one(metadata)
            logger.info(f"Inserted metadata with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting metadata: {e}")
            return None

    def update_document(self, doc_id, summary, keywords):
        try:
            object_id = ObjectId(doc_id)  # Convert string to ObjectId
            self.collection.update_one(
                {'_id': object_id},
                {'$set': {'summary': summary, 'keywords': keywords}}
            )
            logger.info(f"Updated document ID {doc_id} with summary and keywords.")
        except Exception as e:
            logger.error(f"Error updating document ID {doc_id}: {e}")

    def get_all_documents(self, status_filter='all', sort_by=None, sort_order='desc'):
        try:
            query = {}
            if status_filter != 'all':
                query['status'] = status_filter

            sort_fields = {
                'document_name': '_id',
                'num_pages': 'num_pages',
                'processing_time': 'processing_time'
            }
            sort_field = sort_fields.get(sort_by, '_id')

            documents = list(self.collection.find(query).sort(sort_field, 1))
            # Determine sort order
            sort_direction = 1 if sort_order == 'asc' else -1

            logger.info(f"Retrieved {len(documents)} documents from the database.")
            return list(self.collection.find(query).sort(sort_by, sort_direction))
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []

from bson.objectid import ObjectId

def get_document_by_id(self, doc_id):
    try:
        object_id = ObjectId(doc_id)  # Convert string to ObjectId
        document = self.collection.find_one({'_id': object_id})
        if document:
            logger.info(f"Retrieved document ID {doc_id}: {document}")
        else:
            logger.warning(f"No document found with ID {doc_id}.")
        return document
    except Exception as e:
        logger.error(f"Error retrieving document ID {doc_id}: {e}")
        return None