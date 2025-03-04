- change rag context to markdown
- calculate usage for both embedding operation and completions and do an intial cost estimation
- improve pdf reading with logs and batching for more pages
- optimize it with xpdf
- improve insert - add logs, not delete everything each time.
webapp:
- implement answer_question
- change prompt to respond in markdown including a "link" to the page
- add "other related sources" (all rag page results) to both the /ask reponse body and the UI.