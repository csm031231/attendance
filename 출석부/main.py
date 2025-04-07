from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import student, attendance

app = FastAPI(title="Board API")

app.include_router(student.router)
app.include_router(attendance.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)