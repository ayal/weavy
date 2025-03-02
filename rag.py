import weaviate
from weaviate.classes.query import MetadataQuery
import os
import json
import sys

# task query from the process argument i.e python search.py "breakfast cereals"
if len(sys.argv) < 2:
    print("Please provide a query as an argument, e.g. python rag.py \"breakfast cereals\"")
    sys.exit(1)
query = sys.argv[1]

client = weaviate.connect_to_local(headers={
    "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
})

articles = client.collections.get("Article")

print(f"\n\nQuerying articles with the query:\n\n{query}")
result = (
    articles.generate.hybrid(query=query,
                             limit=10,
                             grouped_task=f"answer this question:\n{query}\n---\nbased only on the given context.\nGive links as sources to your response\nif you dont find the answer in the context - say - 'I don't know'."
    )
)

print("\n-------------------- RAG Result --------------------\n")

print(result.generated)




client.close()  # Free up resources
