import chromadb
import uuid
import logging
from typing import Optional, Dict, Any
from rag.embedding_client import get_embedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chroma_client = chromadb.PersistentClient(path="./chroma_fresh")
style_collection = None

def get_style_collection():
    """Get or create the style collection. Only creates if it doesn't exist."""
    global style_collection
    if style_collection is None:
        try:
            style_collection = chroma_client.get_collection(name="style_guides")
            print("Using existing style_guides collection")
        except Exception as e:
            print(f"Could not get existing collection: {e}")
            try:
                style_collection = chroma_client.create_collection(name="style_guides")
                print("Created new style_guides collection")
            except Exception as e2:
                print(f"Could not create collection: {e2}")
                style_collection = chroma_client.get_or_create_collection(name="style_guides")
                print("Using get_or_create for style_guides collection")
    return style_collection

def add_style_guide(text: str, metadata: Optional[Dict[str, Any]] = None):
    try:
        id = str(uuid.uuid4())
        if metadata is None:
            metadata = {}
        
        embedding = get_embedding(text)
        
        if embedding is None:
            logger.error(f"Failed to get embedding for text: {text[:50]}...")
            return None
        
        collection = get_style_collection()
        collection.add(
            ids=[id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )
        
        logger.info(f"Successfully stored style guide with ID: {id}")
        return id
        
    except Exception as e:
        logger.error(f"Failed to store style guide: {str(e)}")
        raise e

