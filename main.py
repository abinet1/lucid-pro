from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from database import engine
import models

from database import engine
from controllers import router as api_router

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MaxSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_size: int):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request, call_next):
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.max_size:
            raise HTTPException(status_code=413, detail="Request payload too large")
        return await call_next(request)

app.add_middleware(MaxSizeMiddleware, max_size=1 * 1024 * 1024)

models.Base.metadata.create_all(bind=engine)

app.include_router(api_router)
    