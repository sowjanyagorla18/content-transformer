import requests
from config import API_KEY, EMBEDDING_URL, RERANKER_URL

HEADERS = {"x-api-key": API_KEY}

def get_embedding(text: str):
    data = {"model": "usf1-embed", "input": text}
    response = requests.post(EMBEDDING_URL, json=data, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Embedding API error: {response.status_code} - {response.text}")
        return None
    
    try:
        result = response.json()
        if "result" in result and "data" in result["result"] and len(result["result"]["data"]) > 0:
            return result["result"]["data"][0]["embedding"]
        else:
            print(f"Unexpected API response format: {result}")
            return None
    except Exception as e:
        print(f"Error parsing embedding response: {e}")
        return None

def rerank(query: str, texts: list[str]):
    data = {
        "model": "usf1-rerank",
        "query": query,
        "texts": texts
    }
    response = requests.post(RERANKER_URL, json=data, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Reranker API error: {response.status_code} - {response.text}")
        return texts  # Return original texts if reranking fails
    
    try:
        result = response.json()
        if "result" in result and "data" in result["result"]:
            result_data = result["result"]["data"]
            
            # Create list of (text, score) tuples and sort by score in increasing order
            scored_docs = [(item["text"], item["score"]) for item in result_data]
            scored_docs.sort(key=lambda x: x[1])  
            
            return [doc[0] for doc in scored_docs]
        else:
            print(f"Unexpected reranker API response format: {result}")
            return texts  # Return original texts if parsing fails
    except Exception as e:
        print(f"Error parsing reranker response: {e}")
        return texts  # Return original texts if error occurs
