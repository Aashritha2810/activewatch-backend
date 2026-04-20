from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import save, tasks, verify, summary, guard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(save.router)
app.include_router(tasks.router)
app.include_router(verify.router)
app.include_router(summary.router)
app.include_router(guard.router)