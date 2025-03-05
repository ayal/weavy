import weaviate
from weaviate.classes.query import MetadataQuery
import os
import json
import sys
import numpy as np
from openai import OpenAI
#from prompts import prompt_rag

prompt_rag="You are a strict assistant. Answer only based on the provided context JSON. If the answer is not found, respond with 'I don't know'. U se markdown. Always include the article page at the end of your response with a newline ans then (page: PAGE)."

def do_rag(question, articles_no):
    weaviate_client = weaviate.connect_to_local(headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    })

    articles = weaviate_client.collections.get("Article")

    print ("Querying articles with the query: ", question)
    result = (
        articles.query.hybrid(query=question,
                            alpha=0.4,
                            return_metadata=MetadataQuery(
                                score=True, explain_score=True),
                                limit=articles_no)
    )

    print("\n-------------------- Search Results --------------------\n")

    json_context = {"Article": []}

    for obj in result.objects:
        print(json.dumps(obj.properties, indent=2))
        print("\n")
        print("Score: ", obj.metadata.score)
        print("Explain Score: ", obj.metadata.explain_score)
        print("----")
        json_context["Article"].append(obj.properties)

    print("\n-------------------- RAG --------------------\n")

    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_rag},
            {"role": "user", "content": f"Context JSON:\n{json_context}\n\nQuestion: {question}"}
        ],
        temperature=0
    )

    weaviate_client.close()  # Free up resources

    return ({"completion_msg":completion.choices[0].message, "articles":json_context})

def main():
    # task query from the process argument i.e python search.py "breakfast cereals"
    if len(sys.argv) < 2:
        print("Please provide a query as an argument, e.g. python rag.py \"breakfast cereals\"")
        sys.exit(1)
    query = sys.argv[1]

    rag_result=do_rag(query, 3)
    print("Answer:")
    print(rag_result["completion_msg"].content)
    print("\nArticles:")
    print(json.dumps(rag_result["articles"], indent=2))

if __name__ == "__main__":
    main()