from promptflow import tool
import dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery

dotenv.load_dotenv('env', override=True)


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def get_search_results(query_text: str, embeddings: list, search_type:str, n_results:int) -> str:
    key = os.environ['AI_SEARCH_KEY']
    index = os.environ['AI_SEARCH_INDEX']
    service = os.environ['AI_SEARCH_NAME']

    if search_type=='KEYWORD':
        search_client = SearchClient(service, index, AzureKeyCredential(key))
        vector_query = VectorizedQuery(vector=embeddings, k_nearest_neighbors=n_results, fields="embeddings")

        results = search_client.search(
            search_text=query_text,
            select=["content", "sourcepage"],
            top=n_results
        )
    elif search_type=='HYBRID':
        search_client = SearchClient(service, index, AzureKeyCredential(key))
        vector_query = VectorizedQuery(vector=embeddings, k_nearest_neighbors=n_results, fields="embeddings")

        results = search_client.search(
            search_text=query_text,
            vector_queries=[vector_query],
            select=["content", "sourcepage"],
            top=n_results
        )
        
    else:
        search_client = SearchClient(service, index, AzureKeyCredential(key))
        vector_query = VectorizedQuery(vector=embeddings, k_nearest_neighbors=n_results, fields="embeddings")

        results = search_client.search(
            vector_queries=[vector_query],
            select=["content", "sourcepage"],
            top=n_results
        )

    contents = []
    for res in results:
        contents.append(res['content'] + ' | ' + res['sourcepage'])
    return '\n'.join(contents)

    # return os.environ['TEST']