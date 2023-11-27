from typing import List
from promptflow import tool
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import CognitiveSearchConnection

@tool
def retrieve_documentation(question: str, index_name: str,  search: CognitiveSearchConnection) -> str:
  
  search_client = SearchClient(endpoint=search.api_base, 
                                index_name=index_name, 
                                credential=AzureKeyCredential(search.api_key))
  

  results = search_client.search(
    search_text=question,
    top=1,
    search_fields=["chunk"],
    
  )

  chunks = [result["chunk"] for result in results]

  return chunks