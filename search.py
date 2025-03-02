import weaviate
from weaviate.classes.query import MetadataQuery
import os
import json
import sys

# task query from the process argument i.e python search.py "breakfast cereals"
if len(sys.argv) < 2:
    print("Please provide a query as an argument, e.g. python search.py \"breakfast cereals\"")
    sys.exit(1)
query = sys.argv[1]

client = weaviate.connect_to_local(headers={
    "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
})

articles = client.collections.get("Article")

print ("Querying articles with the query: ", query)
result = (
    articles.query.hybrid(query=query,
                          alpha=0.5,
                          return_metadata=MetadataQuery(
                              score=True, explain_score=True),
                          limit=10)

)

print("\n\n\n-------------------- Results --------------------\n\n\n")

for obj in result.objects:
    print(json.dumps(obj.properties, indent=2))
    print("\n\n")
    print("Score: ", obj.metadata.score)
    print("Explain Score: ", obj.metadata.explain_score)
    print("----")



client.close()  # Free up resources
