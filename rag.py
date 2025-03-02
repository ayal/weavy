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

print(
    f"\n\nQuerying articles with the query:\n\n{query}\n\nand answering the question based on the context\n\n")
result = (
    articles.generate.hybrid(query=query,
                             limit=10,
                             alpha=0.4,
                             grouped_task="\n".join([
                                 "This is the user search-term or query:",
                                 f"{query}",
                                 "---",
                                 "Find the most relevant parts of the given context to the search-term or query",
                                 "Then give an answer to the search-term or query according to the relevant parts of the context",
                                 "Always include links as sources to your response, in markdown format",
                                 "If you cannot find relevant info on the search-term or query - simply say 'I don't know'",
                             ]),
                             )
)

print("\n-------------------- RAG Result --------------------\n")

print(result.generated)


client.close()  # Free up resources
