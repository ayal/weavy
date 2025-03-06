# docs:
https://weaviate.io/developers/weaviate/quickstart/local

hybrid search and alpha:
https://weaviate.io/developers/weaviate/search/hybrid#balance-keyword-and-vector-search


# install
pip install -U weaviate-client

# env
make sure you have OPENAI_API_KEY in env vars

# config
is in docker-compose.yml

run docker with:
```
docker-compose up -d
```

stop docker from running:
`docker-compose down`

# data
is in dataset_file.py

# run insert:
`python insert.py`
run it once, currently it deletes all docs every time

# run search (hybrid)
`python search.py "gut microbiome"`

# run rag:
`python rag.py "what do you know about b12?"`
`python rag.py "kaki"`

# pdf
`pip install pdfminer.six`
assume harrison.pdf file in same dir, not included in repo since its too big
`python readpdf.py`
`python readpdf.py --pages=50 --start=1`

# webapp:
 run from root:
 `python -m webapp.server`

/: main ui for asking questions
/ask: api (POST, pass question as payload)
/book: ui for viewing one of the book pages (a json file needs to be in output_pages dir, use readpdf.py)
/page: api for getting a page data, gets page as query param and returns page json from output_pages
`http://127.0.0.1:5000/book?page=14`


 # deps:
 poetry (manager)
 numpy
 pdfminer.six (pdf reader)
 openai 
 weaviate-client (vector db)
 flask (web server)

React
React markdownnv 
Tailwind

