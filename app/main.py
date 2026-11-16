from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import publish_message

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="POST a short message with one CTA link to multiple third-party platforms.",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "Automated Multi-Platform Posting System",
        "docs": "/docs",
        "posting": "POST /posting",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/posting", response_model=PostingResponse)
async def posting(body: PostingRequest) -> PostingResponse:
    return await publish_message(body.message)


@app.exception_handler(ValidationError)
async def validation_exception_handler(_request, exc: ValidationError):
    errors = exc.errors()
    detail = "; ".join(
        f"{'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}" for e in errors
    )
    return JSONResponse(status_code=422, content={"detail": detail})


@app.exception_handler(ValueError)
async def value_error_handler(_request, exc: ValueError):
    raise HTTPException(status_code=422, detail=str(exc)) from exc
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
