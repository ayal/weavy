- change rag context to markdown
- calculate usage for both embedding operation and completions and do an intial cost estimation
- improve pdf reading with logs and batching for more pages
- optimize it with xpdf? seems to have column problems - make sure!
- improve insert - add logs, not delete everything each time.

webapp:
- implement answer_question
- change prompt to respond in markdown including a "link" to the page
- add "other related sources" (all rag page results) to both the /ask reponse body and the UI.
- add score to refrences (for dev mode)

logistics:
- make it a python proejct (poetry?) with all listed deps and version
- improve readme


weavitate:
- read docs see all options
- consider reranking: https://weaviate.io/developers/weaviate/search/rerank

pdf:
- fix formatting, for example: 9\n\nC\nH\nA\nP\nT\nE\nR\n2\n\nP\nr\no\nm\no\nt\ni\nn\ng\nG\no\no\nd\nH\ne\na\nl\nt\nh\n\n
- identify structure, separate to sections