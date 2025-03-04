import weaviate
from weaviate.classes.query import MetadataQuery
import os
import json
import sys
import numpy as np
from openai import OpenAI

# task query from the process argument i.e python search.py "breakfast cereals"
if len(sys.argv) < 2:
    print("Please provide a query as an argument, e.g. python search.py \"breakfast cereals\"")
    sys.exit(1)
query = sys.argv[1]
weaviate_client = weaviate.connect_to_local(headers={
    "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
})

articles = weaviate_client.collections.get("Article")

print ("Querying articles with the query: ", query)
result = (
    articles.query.hybrid(query=query,
                          alpha=0.4,
                          return_metadata=MetadataQuery(
                            score=True, explain_score=True),
                            limit=3)
)

print("\n\n\n-------------------- Search Results --------------------\n\n\n")

json_context = {"Article": []}

for obj in result.objects:
    print(json.dumps(obj.properties, indent=2))
    print("\n\n")
    print("Score: ", obj.metadata.score)
    print("Explain Score: ", obj.metadata.explain_score)
    print("----")
    json_context["Article"].append(obj.properties)

print("\n\n\n-------------------- RAG --------------------\n\n\n")

openai_client = OpenAI()
# print(json.dumps(json_context, indent=2))

completion = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a strict assistant. Answer only based on the provided context JSON. If the answer is not found, respond with 'I don't know'. Always include the article page in your response."},
        {"role": "user", "content": f"Context JSON:\n{json_context}\n\nQuestion: {query}"}
    ]
)

print("Answer:");

print(completion.choices[0].message)

weaviate_client.close()  # Free up resources
