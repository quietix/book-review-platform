from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from config import config
from api.v1.router import router as router_v1


app = FastAPI(
    title="Book review platform",
    description="A platform where users can write and read book reviews, rate books, "
                "and get recommendations based on reading history.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix="/api")


@app.get("/", tags=["Health"])
async def read_root():
    return Response(status_code=200)
