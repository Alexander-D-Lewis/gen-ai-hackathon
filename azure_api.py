import requests
from azure.identity import DefaultAzureCredential
import os  
import json  
import openai  
from dotenv import load_dotenv  
from tenacity import retry, wait_random_exponential, stop_after_attempt  
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import Vector  
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SearchField,  
    SemanticSettings,  
    VectorSearch,  
    VectorSearchAlgorithmConfiguration,  
)  
  
# Configure environment variables  
load_dotenv()  
service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") 
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME") 
key = os.getenv("AZURE_SEARCH_ADMIN_KEY") 
openai.api_type = "azure"  
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")  
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")  
credential = AzureKeyCredential(key)


creds =DefaultAzureCredential()
headers = {"Ocp-Apim-Subscription-Key": "52a37d06-0f17-4003-b329-f5b575261bb5"}

if __name__ == "__main__":

    url = "https://team-11.search.windows.net/indexes/azureblob-index-2/docs?api-version=2021-04-30-Preview&search=*"
    response = requests.get(url, headers=headers)
    breakpoint()
    data = response.json()
    breakpoint()