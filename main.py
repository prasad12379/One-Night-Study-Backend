from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ✅ MISSING IMPORT
import firebase_admin
from firebase_admin import credentials, db

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ ADD CORS (IMPORTANT FOR ANDROID)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Firebase Init (SAFE)
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": "https://database-3d487-default-rtdb.firebaseio.com"
            }
        )

BASE_PATH = "/education"

def get_data(path=""):
    init_firebase()
    ref = db.reference(BASE_PATH + path)
    return ref.get()

# ================= TEST =================
@app.get("/")
def home():
    return {"status": "Welcome all Fine"}

# ================= APIs =================

# 1️⃣ Stream → Branches
@app.get("/api/{stream}")
def get_stream(stream: str):
    print("🔥 HIT /api/{stream} WITH:", stream)
    data = get_data(f"/{stream}")
    if not data:
        return {"error": "Data not found"}
    return list(data.keys())


# 2️⃣ Stream + Branch → Semesters
@app.get("/api/{stream}/{branch}")
def get_stream_branch(stream: str, branch: str):
    data = get_data(f"/{stream}/{branch}")
    if not data:
        return {"error": "Branch not found"}
    return list(data.keys())

# 3️⃣ Stream + Branch + Sem → Subjects
@app.get("/api/{stream}/{branch}/{sem}")
def get_stream_branch_sem(stream: str, branch: str, sem: str):
    data = get_data(f"/{stream}/{branch}/{sem}")
    if not data:
        return {"error": "Semester not found"}
    return list(data.keys())

# 4️⃣ Stream + Branch + Sem + Subject → PDF URL
@app.get("/api/{stream}/{branch}/{sem}/{sub}")
def get_stream_branch_sem_sub(stream: str, branch: str, sem: str, sub: str):
    data = get_data(f"/{stream}/{branch}/{sem}/{sub}")
    if not data:
        return {"error": "Subject not found"}
    return [data]
