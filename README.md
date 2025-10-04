# Cat Database for Tartu Kassikaitse

Web app to track cats, managers, foster homes, vet visits and so on

Devs: Aaron Anders Jaani, Mark Riispapp, Caroline Markov, Sebastian Mais

Customer: MTÜ Tartu Kassikaitse, contact (hanna.pook@gmail.com)

## Links
- [Wiki](https://gitlab.cs.ut.ee/aajaani/catdb/-/wikis/home)
- [Issue Board](https://gitlab.cs.ut.ee/aajaani/catdb/-/boards)

## Structure
- backend/  
- frontend/ — (to be added later)


## 1) Prerequisites

* **Docker** & **Docker Compose**
* **Python** 3.11+ 


## 2) Start dependencies (Postgres, MinIO, Adminer)

From the `backend/` folder:

```bash
docker compose up -d
```

What this starts:

* **PostgreSQL** on `localhost:5432`

  * DB: `catdb`
  * User: `user`
  * Password: `password`
  * Volume: `data`
* **MinIO** (S3 compatible object storage)

  * API: `http://localhost:9000`
  * Console (UI): `http://localhost:9001`
  * Credentials: `minioadmin / minioadmin`
  * Bucket: `tkk-cats` (auto-created at app startup)
* **Adminer** (DB web UI) on `http://localhost:8080`


## 3) Backend setup & run

From `backend/`:

```bash
# 1) create and activate venv
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 2) install deps
pip install -r requirements.txt


# 4) start the server
uvicorn app.main:app --reload
```


Health check:

```
http://127.0.0.1:8000/
→ {"Hello":"World"}
```




## 4) API endpoints (current)

### Cats

* `post /cats` - create new cat (multipart form with JSON string + optional file)
* `get /cats` - list all cats (includes manager & foster home if linked)
* `get /cats/{cat_id}` - get one cat by id
* `patch /cats/{cat_id}` - partial update (multipart form with JSON string + optional file)
* `delete /cats/{cat_id}` - delete cat (hard delete currently)

### Managers

* `post /managers` - create manager
* `get /managers` - list managers

### Foster homes

* `post /foster-homes` - create foster home
* `get /foster-homes` - list foster homes

### Media (MinIO)

* `get /image/{object_name}` - stream an object (image/file) by object key

## 5) Tests

To run tests 
``` 
cd backend
python -m pytest
```


