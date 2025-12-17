"""
FastAPI wrapper for code-doc-generator to serve as API and frontend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import os
import logging

from src.code_parser import CodeParser
from src.llm_generator import DocGenerator

logger = logging.getLogger(__name__)
app = FastAPI(title="Code Doc Generator")

# Initialize parser and generator
parser = CodeParser()
generator = DocGenerator(api_key=os.getenv("OPENAI_API_KEY"))


class ParseRequest(BaseModel):
    path: str


class GenerateRequest(BaseModel):
    signature: str
    context: Optional[str] = ""


@app.get("/")
async def root():
    return {
        "message": "Code Doc Generator API",
        "endpoints": {
            "parse_file": "POST /api/parse-file",
            "parse_directory": "POST /api/parse-directory",
            "generate": "POST /api/generate",
        },
    }


@app.post("/api/parse-file")
async def parse_file(req: ParseRequest):
    """Parse a single Python file."""
    try:
        if not os.path.exists(req.path):
            raise HTTPException(status_code=404, detail="File not found")
        result = parser.parse_python(req.path)
        return {"file": req.path, "items": result}
    except Exception as e:
        logger.exception("Parse file failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/parse-directory")
async def parse_directory(req: ParseRequest):
    """Parse all Python files in a directory."""
    try:
        if not os.path.isdir(req.path):
            raise HTTPException(status_code=404, detail="Directory not found")
        result = parser.parse_directory(req.path)
        return {"directory": req.path, "files": result}
    except Exception as e:
        logger.exception("Parse directory failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_docstring(req: GenerateRequest):
    """Generate a docstring for a function signature."""
    try:
        docstring = generator.generate_for_function(req.signature, req.context)
        return {"signature": req.signature, "docstring": docstring}
    except Exception as e:
        logger.exception("Generate failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


# Serve frontend static files if they exist
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=frontend_dist), name="static")

    @app.get("/index.html")
    async def serve_index():
        return FileResponse(frontend_dist / "index.html")

    @app.get("")
    async def serve_root():
        return FileResponse(frontend_dist / "index.html")
