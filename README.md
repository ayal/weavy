# docs:
https://weaviate.io/developers/weaviate/quickstart/local

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
`python search.py "what are the foods richest in b12"`

# run rag:
`python rag.py "what are the foods richest in b12"`
`python rag.py "kaki"`
