import os

from zep_python import ZepClient
from dotenv import load_dotenv

load_dotenv()
zep_api_key = os.getenv('OPENAI_API_KEY')
zep_base_url = os.getenv('ZEP_API_URL')

client = ZepClient(base_url=zep_base_url, api_key=zep_api_key)

collection_name = "babbagedocs"  # the name of your collection. alphanum values only

# collection = client.document.add_collection(
#     name=collection_name,  # required
#     description="Babbage's Calculating Engine",  # optional
#     metadata={"foo": "bar"},  # optional metadata to associate with this collection
#     embedding_dimensions=384,  # this must match the model you've configured for
#     is_auto_embedded=True,  # use Zep's built-in embedder. Defaults to True
# )
collection = client.document.get_collection(collection_name)

print(collection)
