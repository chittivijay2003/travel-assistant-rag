# 🚀 Quick Start Guide - RAG Travel Assistant

## For Professor/Evaluator - 5 Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure API Key (30 seconds)
```bash
# Edit .env file
nano .env

# Add this line (get free key from https://makersuite.google.com/):
GOOGLE_API_KEY=your_api_key_here
```

### Step 3: Initialize Database (1 minute)
```bash
python main.py --mode setup
```
Expected output:
```
✅ Collection 'travel_documents' created
✅ Indexed 15 documents
✅ Database setup complete!
```

### Step 4: Run Application (30 seconds)
```bash
python main.py --mode both
```

### Step 5: Test (1 minute)
Open browser: http://localhost:7860

Try these queries:
1. "What visa requirements for Japan from India?"
2. "Cultural customs in UAE?"
3. "India e-visa process?"

## Alternative: API Only
```bash
# Start API server
python main.py --mode api

# Access docs
Open: http://localhost:8000/docs

# Test health endpoint
curl http://localhost:8000/api/v1/health
```

## Troubleshooting

**Issue**: `ModuleNotFoundError`
**Fix**: `pip install -r requirements.txt`

**Issue**: "Qdrant connection failed"
**Fix**: This uses local persistent storage, no server needed. Just run `python main.py --mode setup`

**Issue**: "Invalid API key"
**Fix**: Add valid `GOOGLE_API_KEY` in `.env` file

**Issue**: Port already in use
**Fix**: `python main.py --mode both --api-port 9000 --ui-port 9001`

## Stop Servers
Press `Ctrl+C` in terminal

Or:
```bash
pkill -f "python.*main.py"
```

## File Overview

- **main.py**: Entry point, runs UI/API
- **README.md**: Full documentation
- **requirements.txt**: Dependencies
- **src/**: Source code
- **scripts/**: Setup scripts
- **.env**: Configuration (YOU MUST ADD API KEY)

## Expected Results

✅ UI loads at http://localhost:7860  
✅ Purple-violet gradient interface  
✅ Queries return answers with sources  
✅ Confidence scores shown  
✅ API docs at http://localhost:8000/docs  
✅ 15 travel documents indexed  

## Questions?

Check:
1. README.md (comprehensive docs)
2. SUBMISSION_CHECKLIST.md (evaluation guide)
3. API docs: http://localhost:8000/docs
