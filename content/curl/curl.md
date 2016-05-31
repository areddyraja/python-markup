
curl -v -H "Content-Type: application/json" \
	 -X POST http://localhost:5000/questions \
	 -d '{"id": "test", "title": "MyTitle", "text":"The text of my question"}'


	 curl -v http://localhost:5000/questions/test


	 curl -v -H "Content-Type: application/json" \
	 -X PUT http://localhost:5000/questions/test \
	 -d '{"text":"Another text"}'
	 

