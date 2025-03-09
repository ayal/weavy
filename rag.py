import weaviate
from weaviate.classes.query import MetadataQuery
import os
import json
import sys
import numpy as np
from openai import OpenAI
#from prompts import prompt_rag

prompt_rag = "\n".join([
    # "You are a strict assistant. Answer only based on the provided context JSON.",
    "You are a medical assistant. You answer only based on a provided context and a question.",
    "If the answer is not found in the context, respond with 'I don't know'.",
    "Use markdown format in your response, include a link to the referenced articles at the end of your response.",
#    "Always include the article page at the end of your response with a newline",
# "and then (page: PAGE)."
])

user_msg = "\n".join([
    "# Instructions:",
    "1. First go over all articles in the context one by one and mention for each:"
    "  a. How relevant it is to the question.",
    "  b. Include one very short sentence regarding what is relevant in the article"
    "  c. include a markdown link to the page in this format: [page N](/book?page=N)",
    "2. Then answer the question in a detailed medical manner based on the context and the user question.",
    "---",
    "# Your Response Markdown Format:",
    "# Sources:",
    "Source 1: Very relevant. The article mentions the history of breakfast cereals. [page N](/book?page=N)",
    "Source 2: Not relevant. The article mentions the history of lunch cereals. [page M](/book?page=M)",
    '---'
    "# Answer:",
    "<The detailed medical answer to the user question.>",
    "Sources: [page 1](/book?page=1), [page N](/book?page=N), [page M](/book?page=M)"
])

def article_to_markdown(index, page, content):
    md = f"# Source {index}\n\n"
    md += f"**page: {page}**\n\n"
    md += "## Content:\n"
    md += content

    return md

# Example usage

def do_rag(question, articles_no):
    weaviate_client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
        }
    )

    if not weaviate_client.is_ready():
        print ("Weaviat client failed to connect")
        return ({})

    print("Connected to Weaviat client")
    articles = weaviate_client.collections.get("Article")

    print("Querying articles with the query: ", question)
    result = (
        articles.query.hybrid(query=question,
                            alpha=0.4,
                            return_metadata=MetadataQuery(
                                score=True, explain_score=True),
                                limit=articles_no)
    )

    print("\n-------------------- Search Results --------------------\n")

    json_context = {"Article": []}
    md_context=""
    for i, obj in enumerate(result.objects, start=1):
        print("\n")
        print("Score: ", obj.metadata.score)
        print("Explain Score: ", obj.metadata.explain_score)
        print("----")
        json_context["Article"].append(obj.properties)
        md_context+=article_to_markdown(index=i, page=obj.properties["page"], content=obj.properties["content"])
        md_context+="\n"
        
    print(md_context)

    print("\n-------------------- RAG --------------------\n")

    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_rag},
            {"role": "user", "content": f"Context:\n\n{md_context}\n\n---\n\nQuestion:\n\n{question}\n\n---\n\n---\n\n{user_msg}"}
        ],
        max_tokens=1500,
        temperature=0
    )

    weaviate_client.close()  # Free up resources

    print("\n\nCompletion Answer:\n\n")
    print(completion.choices[0].message.content)
    print("\n\n")

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
    print(rag_result["articles"])

if __name__ == "__main__":
    main()