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
            "page": article["page"],
            "content": article["text"]
        }

        print("Adding article: ", properties["page"])
        try:
            batch.add_object(properties)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        counter = counter + 1

print("Inserting Articles complete")

client.close()  # Free up resources
