import weaviate
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery
import os
import json
from dataset_file import dataset

client = weaviate.connect_to_local(headers={
    "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
})

client.collections.delete_all()
client.collections.create(name="Article",
                          vectorizer_config=Configure.Vectorizer.text2vec_openai(
                              model="text-embedding-3-small"),
                          generative_config=Configure.Generative.openai(model="gpt-4o"))


articles = client.collections.get("Article")

counter = 0
with articles.batch.dynamic() as batch:
    for article in dataset:
        if (counter % 10 == 0):
            print(f"Insert {counter} / {len(dataset)} ")

        properties = {
            "title": article["title"],
            "content": article["text"],
            "url": article["url"]
        }

        print("Adding article: ", properties)
        batch.add_object(properties)
        counter = counter + 1

print("Inserting Articles complete")

client.close()  # Free up resources
