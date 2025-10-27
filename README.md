Here’s the updated README — only the backend-related additions have been inserted under appropriate sections (✅ minimal, precise, no unrelated edits):

---

# Cat Database for Tartu Kassikaitse

Web app to track cats, managers, foster homes, vet visits and so on

Devs: Aaron Anders Jaani, Mark Riispapp, Caroline Markov, Sebastian Mais

Customer: MTÜ Tartu Kassikaitse, contact ([hanna.pook@gmail.com](mailto:hanna.pook@gmail.com))

## Links

* [Wiki](https://gitlab.cs.ut.ee/aajaani/catdb/-/wikis/home)
* [Issue Board](https://gitlab.cs.ut.ee/aajaani/catdb/-/boards)

## Structure

* backend/
* frontend/

## 1) Prerequisites

* **Docker** & **Docker Compose**
* **Python** 3.11+
* **Node.js**
* **npm (comes with Node)**

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


# 3) start the server
uvicorn app.main:app --reload
```

Health check:

```
http://127.0.0.1:8000/
→ {"Hello":"World"}
```

---

### Authentication system 



* `users` table

  * `username`, `password_hash`, `is_manager`, `is_active`, `manager_id (FK)`
* Passwords hashed securely with **Argon2** (`passlib`).
* **JWT-based login** at `/login`:

  * Returns `access_token` containing user ID, role, and expiry.

  * Managers (`is_manager=True`) can create, update, and delete.
  * Non-managers can only view data.
* Added `/users/full-create` endpoint:

  * Managers can invite or register new users.
  * If `is_manager=True`, automatically creates and links a `Manager` record.
* Added `bootstrap_admin()`:

  * On first run, creates an admin user (`admin / admin12345`) with linked Manager row


---

## 4) Frontend setup & run

```bash
# 1) go to vue directory
cd frontend/vue-project

# 2) install dependencies
npm install

# 3) start development server
npm run dev
```

Visit `http://localhost:8081` in your browser

## 5) API endpoints

### Cats

* `POST /cats` – create a new cat (multipart form: `payload` JSON string + optional `primary_image` file)
* `GET /cats` – list all cats (includes related manager & foster home)
* `GET /cats/{cat_id}` – get one cat by ID
* `PATCH /cats/{cat_id}` – update cat fields (multipart form + optional new `primary_image`)
* `DELETE /cats/{cat_id}` – delete cat (hard delete; cascades to tasks & procedures)

### Procedures

* `POST /cats/{cat_id}/procedures` – add medical procedure for a cat (multipart form: `payload` JSON string + optional `file`)

  * payload fields: `type` (`DEWORMER`, `SPOT_ON`, `VACCINE`), `is_repeat`, `at_date`, `notes`, `payment`
* `GET /cats/{cat_id}/procedures` – list all procedures for a cat (sorted by date desc)

### Tasks (Calendar)

* `POST /tasks` – create a task for a cat (JSON body: `cat_id`, `type`, `due_date`, `notes`)

  * type options: `VET_VISIT`, `MEDICATION`, `PERSONAL`
* `GET /tasks` – list all tasks (for calendar feed)
* `GET /cats/{cat_id}/tasks` – list all tasks related to one cat

### Managers

* `POST /managers` – create manager
* `GET /managers` – list all managers

### Foster Homes

* `POST /foster-homes` – create foster home
* `GET /foster-homes` – list foster homes

### Media (MinIO)

* `GET /image/{object_name}` – stream a stored image or file by its MinIO object key

---

## 6) Database layout overview

**Main tables:**

| Table            | Purpose                             | Key columns                                                          | Relations                                               |
| ---------------- | ----------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| `cats`           | Base table for all cats             | `id`, `name` (unique), `status`, `manager_id`, `foster_home_id`      | → `managers`, `foster_homes`, `cat_procedures`, `tasks` |
| `cat_procedures` | Unlimited medical records per cat   | `type`, `is_repeat`, `at_date`, `notes`, `payment`, `file_object`    | → `cats` (many-to-one)                                  |
| `tasks`          | Calendar tasks / reminders          | `type`, `due_date`, `notes`                                          | → `cats` (many-to-one)                                  |
| `managers`       | Staff or volunteers managing cats   | `display_name`, `phone`, `email`                                     | ← `cats.manager_id`                                     |
| `foster_homes`   | Temporary homes                     | `name`, `phone`, `email`, `address`                                  | ← `cats.foster_home_id`                                 |
| `users`          | Login accounts (new)                | `username`, `password_hash`, `is_manager`, `is_active`, `manager_id` | → `managers` (optional FK)                              |
| `audit_logs`     | Automatic CRUD audit trail          | `entity_type`, `entity_id`, `action`, `timestamp`                    | n/a                                                     |
| `cat_files`      | Additional uploaded files (per cat) | `object_name`, `label`                                               | → `cats`                                                |

---

## 7) Tests

To run tests

```
cd backend
python -m pytest
```

<img src="https://media.tenor.com/BuImo5Z739UAAAAM/cat.gif" width="100">

---

✅ **Backend now supports secure authentication, password hashing, JWT session management, and role-based authorization — ready for frontend integration.**
