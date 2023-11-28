from typing import List
from promptflow import tool
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from promptflow.connections import CognitiveSearchConnection

@tool
def retrieve_documentation(question: str, index_name: str, embedding: List[float], search: CognitiveSearchConnection, full_text_search: bool, vector_search: bool) -> str:
  
  search_client = SearchClient(endpoint=search.api_base, 
                                index_name=index_name, 
                                credential=AzureKeyCredential(search.api_key))
  

  search_parameters = { "top" : 1, "search_fields" : ["chunk"]}

  if full_text_search:
    search_parameters["search_text"] = question
  
  if vector_search:
    vector_query = VectorizedQuery(vector=embedding, fields="vector")
    search_parameters["vector_queries"] = [vector_query]

  results = search_client.search(**search_parameters)

  chunks = [result["chunk"] for result in results]

  return chunks