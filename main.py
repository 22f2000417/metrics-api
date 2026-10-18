import time
import uuid
from statistics import mean

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        parts = values.split(",")
        if any(not p.strip() for p in parts):
            raise ValueError
        numbers = [int(p.strip()) for p in parts]
        if not numbers:
            raise ValueError
    except ValueError:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=400,
            content={"detail": "values must be comma-separated integers"},
        )

    return {
        "email": "22f2000417@ds.study.iitm.ac.in",
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": mean(numbers),
    }


# Register CORS first, then the header middleware.
# Starlette makes the last-added middleware the outermost layer.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-onbmho.example.com"],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


class RequestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = max(0.0, time.perf_counter() - start)
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{elapsed:.8f}"
        return response


app.add_middleware(RequestHeadersMiddleware)
