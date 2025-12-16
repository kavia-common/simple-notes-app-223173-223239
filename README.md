# simple-notes-app-223173-223239

Simple Notes backend (Flask) providing CRUD endpoints with SQLite persistence.

- Base URL (preview): http://localhost:3001
- OpenAPI/Swagger UI: http://localhost:3001/docs
- Health check: GET /

## Run locally
The service is configured to run on port 3001.
```
cd notes_backend
pip install -r requirements.txt
python run.py
```
On first run, a SQLite file `notes.db` is created automatically under `notes_backend/app/../`.

## Endpoints

- GET /notes
  - List all notes ordered by most recently updated first.
  - 200 OK -> [{"id":1,"title":"...","content":"...","created_at":"...","updated_at":"..."}]

- POST /notes
  - Create a new note.
  - Body JSON:
    {
      "title": "My title",
      "content": "My content"
    }
  - 201 Created -> created note object

- GET /notes/{id}
  - Retrieve a specific note by ID.
  - 200 OK -> note object
  - 404 Not Found if missing

- PUT /notes/{id}
  - Update a note (title and/or content).
  - Body JSON (any of the fields):
    {
      "title": "New title",
      "content": "New content"
    }
  - 200 OK -> updated note
  - 404 Not Found if missing

- DELETE /notes/{id}
  - Delete a note.
  - 204 No Content on success
  - 404 Not Found if missing

## Sample curl

# List
curl -s http://localhost:3001/notes | jq .

# Create
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First","content":"Hello world"}' | jq .

# Get by ID
curl -s http://localhost:3001/notes/1 | jq .

# Update
curl -s -X PUT http://localhost:3001/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content"}' | jq .

# Delete
curl -i -X DELETE http://localhost:3001/notes/1

## Notes
- CORS is enabled for development.
- Error handling:
  - 400 for invalid payloads (validation)
  - 404 for missing resources
  - 500 for unexpected server/database errors
