import weaviate
from weaviate.classes.config import Configure
import os

def setup_weaviate():
    client = weaviate.connect_to_local(headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    })
    client.collections.delete_all()
    client.collections.create(
        name="Article",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(model="text-embedding-3-small"),
        generative_config=Configure.Generative.openai(model="gpt-4o")
    )
    return client

def insert_articles(client, articles):
    article_collection = client.collections.get("Article")
    with article_collection.batch.dynamic() as weaviate_batch:
        for article in articles:
            weaviate_batch.add_object(article)