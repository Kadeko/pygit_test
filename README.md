# pygit_test
Its simple request processing listener

To test the server using fake local requests, I added curl req and json files.
POST requests are compiled from WebHooks

curl -d "@pullreq.json" -X POST http://localhost:8080/data -H "X-GitHub-Delivery: 02022f00-b20c-11e9-83ce-3a02a8529880" -H "x-github-event: pull_request"

curl -d "@create.json" -X POST http://localhost:8080/data -H "X-GitHub-Delivery: b61dc97a-b150-11e9-8897-f546809e714f" -H "x-github-event: create"

curl -d "@push.json" -X POST http://localhost:8080/data -H "X-GitHub-Delivery: fbf4a556-b20c-11e9-89d1-70c09ce14042" -H "x-github-event: push"

curl -d "@delete.json" -X POST http://localhost:8080/data -H "X-GitHub-Delivery: 668964b0-b20d-11e9-9c12-93a4acef3d1f" -H "x-github-event: delete"

