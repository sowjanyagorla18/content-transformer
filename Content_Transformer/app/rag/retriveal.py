import logging
from rag.vector_store import get_style_collection
from rag.embedding_client import rerank

# Configure logging
logger = logging.getLogger(__name__)

def retrieve_style_examples(query: str, n_results: int = 5) -> list[str]:
    """
    Performs semantic search and reranking to retrieve the most relevant style examples.
    
    Returns:
        List of top-matching style guide texts (strings).
    """
    try:
        logger.info(f"Starting RAG search with query: '{query}'")
        
        # Step 1: Initial semantic search using ChromaDB
        collection = get_style_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        logger.info(f"ChromaDB query results: {results}")
        
        # Extract documents from ChromaDB results
        docs = results['documents'][0] if results['documents'] and results['documents'][0] else []

        logger.info(f"Extracted {len(docs)} documents from results")

        if docs:
            reranked_docs = rerank(query, docs)
            logger.info(f"Reranked to {len(reranked_docs)} documents")
            return reranked_docs
        else:
            logger.warning("No documents found in ChromaDB query results")
            return []
    except Exception as e:
        logger.error(f"Error in retrieve_style_examples: {e}")
        return []
