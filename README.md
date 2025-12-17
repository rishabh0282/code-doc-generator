# Code Doc Generator

Intelligent CLI and web tool that automatically generates code documentation using LLMs (GPT-3.5/4). Parse Python code, extract functions/classes, and generate accurate docstrings powered by OpenAI.

## Features

? Parse Python files and directories with AST  
? Extract functions, classes, methods, signatures  
? Generate docstrings using GPT-3.5/4  
? Beautiful React web UI  
? FastAPI REST backend  
? Dry-run mode for preview  
? CLI and web interface  

## Tech Stack

- **Backend:** FastAPI, LangChain, OpenAI
- **Frontend:** React 18, Vite
- **Parser:** Python AST
- **LLM:** OpenAI GPT-3.5-turbo / GPT-4

## Installation

### Quick Setup (Recommended)

Linux/macOS:
```bash
chmod +x scripts/setup-full.sh
./scripts/setup-full.sh
```

Windows PowerShell:
```powershell
.\scripts\setup-full.ps1
```

### Manual Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install and build frontend:
```bash
cd frontend
npm install
npm run build
cd ..
```

4. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your_openai_key_here" > .env
```

## Usage

### Web Interface

```bash
# Activate venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Run FastAPI server
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

Open browser: http://localhost:8000

### API Endpoints

- `GET /` — Root endpoint with info
- `GET /health` — Health check
- `POST /api/parse-file` — Parse single Python file
- `POST /api/parse-directory` — Parse all Python files in directory
- `POST /api/generate` — Generate docstring for function signature
- `GET /docs` — Swagger UI

### Example API Calls

Parse a single file:
```bash
curl -X POST "http://localhost:8000/api/parse-file" \
  -H "Content-Type: application/json" \
  -d '{"path":"/path/to/myfile.py"}'
```

Parse a directory:
```bash
curl -X POST "http://localhost:8000/api/parse-directory" \
  -H "Content-Type: application/json" \
  -d '{"path":"/path/to/project/src"}'
```

Generate docstring:
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"signature":"process_data(data, format, encoding)","context":"Function to transform raw data"}'
```

### CLI Usage

```bash
# Parse Python file (dry-run shows what would be generated)
python src/cli.py /path/to/file.py --dry-run --api-key YOUR_KEY

# Parse directory
python src/cli.py /path/to/project --dry-run

# Specify output format
python src/cli.py /path/to/file.py --format docstring --dry-run

# Verbose output
python src/cli.py /path/to/file.py --dry-run --verbose
```

## Project Structure

```
code-doc-generator/
??? frontend/                 # React web UI
?   ??? src/
?   ?   ??? components/
?   ?   ?   ??? Parser.jsx
?   ?   ?   ??? Parser.css
?   ?   ??? App.jsx
?   ?   ??? main.jsx
?   ??? package.json
?   ??? vite.config.js
??? src/
?   ??? api.py               # FastAPI endpoints
?   ??? code_parser.py       # AST-based Python parser
?   ??? llm_generator.py     # LangChain + OpenAI wrapper
?   ??? doc_formatter.py     # Format docstrings
?   ??? cli.py               # Command-line interface
??? templates/
?   ??? docstring_template.txt
?   ??? readme_template.txt
??? scripts/
?   ??? setup-full.sh
?   ??? setup-full.ps1
??? requirements.txt
??? README.md
```

## Architecture

```
????????????????????????????????????????
?      React Web UI                     ?
?  Parse File | Parse Dir | Show Results?
????????????????????????????????????????
                 ? HTTP API
????????????????????????????????????????
?         FastAPI Backend               ?
?  /api/parse-file                      ?
?  /api/parse-directory                 ?
?  /api/generate                        ?
????????????????????????????????????????
  ?                              ?
??????????????????      ????????????????
? Code Parser    ?      ? LLM Generator?
? - AST analysis ?      ? - LangChain  ?
? - Extract defs ?      ? - OpenAI     ?
??????????????????      - Prompting   ?
                 ????????????????????

             CLI Tool
              ?
    Parse code locally
    Generate docstrings
    Preview or write
```

## Supported Languages

Currently supported:
- ? Python (full support)

Future:
- [ ] JavaScript/TypeScript
- [ ] Java
- [ ] Go

## Performance

- **Parse Speed:** ~500 lines/sec
- **Generate Speed:** ~5 sec per docstring (OpenAI API)
- **Memory:** ~100MB for 10K lines of code

## Development

### Frontend Development

```bash
cd frontend
npm run dev
```

### Backend Development

```bash
uvicorn src.api:app --reload --log-level debug
```

## Examples

### Example 1: Parse and Review

Web UI ? Enter path ? Click Parse ? Review extracted functions/classes

### Example 2: Batch Generate Docstrings

```bash
# List all functions in file
curl -X POST http://localhost:8000/api/parse-file \
  -d '{"path":"src/models.py"}' | jq '.items'

# Generate for each function
curl -X POST http://localhost:8000/api/generate \
  -d '{"signature":"load_model(model_path)","context":"Load pretrained model from disk"}'
```

## Configuration

Environment variables (in `.env`):

```bash
OPENAI_API_KEY=sk-...              # Required for LLM generation
OPENAI_MODEL=gpt-3.5-turbo        # Model to use (default)
```

## Future Improvements

- [ ] Support for JavaScript/TypeScript
- [ ] Type hint detection and inclusion
- [ ] Parameter type inference
- [ ] Return type annotation
- [ ] Automatic example generation
- [ ] Batch file processing with progress bar
- [ ] Git integration (auto-commit)
- [ ] Pre-commit hook integration
- [ ] IDE plugins (VS Code, PyCharm)

## Troubleshooting

**Issue:** "OpenAI API rate limit exceeded"
- Solution: Wait or upgrade API quota

**Issue:** "Module not found" when parsing
- Solution: Ensure the path is valid and accessible

**Issue:** Frontend not loading
- Solution: Run `cd frontend && npm run build` and restart server

## License

MIT

## Contributing

Pull requests welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow project code style
4. Add tests for new features
5. Submit PR with description

## Support

- GitHub Issues: Report bugs or feature requests
- API Docs: `/docs` endpoint (Swagger UI)