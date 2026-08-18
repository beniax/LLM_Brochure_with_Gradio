# BrochureGen — Gradio LLM Brochure Generator

BrochureGen is a small experimental Gradio web app that builds short brochure-style markdown summaries for companies by scraping a target website, selecting relevant pages, and using an LLM to generate a concise brochure. It supports streaming model output from multiple backends (OpenAI/GPT, Google's Gemini, and Ollama/local models).

**Purpose**

BrochureGen helps you automatically create customer-facing brochure text by combining simple web scraping (landing page + related links) with an LLM that synthesizes the information into a short, readable markdown brochure. It's designed for prototyping and demonstrating streaming LLM usage inside a lightweight Gradio UI.

**Repository layout (relevant files)**

- `gradio_llm_brochure.py` — Gradio app entry point. Provides the web UI and example inputs. Launches a streaming generator from `method_utils.create_brochure` and displays incremental output.
- `method_utils.py` — Core logic: scrapes the site, selects relevant links, builds prompts, and calls LLM backends (OpenAI, Gemini, Ollama). Streaming-compatible functions yield chunks of text as they're produced by the model.
- `scrapper.py` — Local helper (used by `method_utils.py`) to fetch page contents and links. Inspect it to see which HTTP and HTML parsing libraries are used.

**Libraries Used**

- `gradio` — lightweight web UI for demos and interactive apps.
- `openai` — official OpenAI client used to call GPT-style models (when configured).
- `litellm` — lightweight client wrapper used in this project for Gemini/Ollama-style completions (streaming examples exist in `method_utils.py`).
- `python-dotenv` (`dotenv`) — load `.env` environment variables for API keys and endpoints.
- `requests` — (likely used in `scrapper.py`) to fetch web pages.
- `beautifulsoup4` / `bs4` — (likely used in `scrapper.py`) to parse HTML and extract links and text.
- `json` / `os` / `typing` — standard library helpers for configuration and parsing.

If a package above is not actually used in your `scrapper.py`, adjust the dependency list accordingly.

## Prerequisites & Installation

1. Install Python 3.8 or newer.
2. Clone the repository and change into the project folder (adjust the path to your workspace):

```bash
git clone <your-repo-url>
cd "web UI Gradio, image gen, voice gen project aI airline assitant/Gradio_proj/gradio_llm_brochure"
```

3. Create and activate a virtual environment:

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies (example):

```bash
pip install --upgrade pip
pip install gradio openai litellm python-dotenv requests beautifulsoup4
```

5. Configure environment variables. Create a `.env` file in the same folder or export the variables in your shell. At minimum set:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=ya29....   # If you use Gemini
OLLAMA_HOST=http://localhost:11434  # Or your Ollama endpoint if using Ollama
```

## Key Commands

- Launch the Gradio web app (default, opens in browser):

```bash
python gradio_llm_brochure.py
```

- Run a quick one-off generation from Python REPL (example streaming):

```python
from method_utils import create_brochure
gen = create_brochure('Hugging Face', 'https://huggingface.co/', 'GPT')
for chunk in gen:
    print(chunk, end='')
```

## How to Use (end-user guide)

1. Start the app:

```bash
python gradio_llm_brochure.py
```

2. In the web UI enter:

- Company Name — a short display name (for context/prompt).
- URL — the public website URL to scrape and summarize.
- Model — choose one of `GPT`, `GEMINI`, or `Ollama`.

3. Click Submit. The UI streams the model output as it is produced. Example built-in examples are:

- `Hugging Face`, `https://www.huggingface.com/`, `GPT`
- `AI Engineer by edward donner`, `https://edwarddonner.com/`, `GEMINI`

4. The output is markdown text (no code blocks) describing the company, culture, products, and careers if available.

## Configuration & Notes

- Model names used in `method_utils.py`:
  - GPT: `gpt-4.1-mini` via the `openai` client.
  - Gemini: `gemini/gemini-2.5-flash` via `litellm.completion`.
  - Ollama: `ollama/llama3.2:1b` via `litellm.completion` (you may need to adjust the call/credentials depending on your Ollama setup).

- If you use Ollama locally, ensure the Ollama daemon is running and `OLLAMA_HOST` (or the script's configuration) points to it.

## Troubleshooting & Known Issues

- Streaming vs final string: The generator-based streaming functions (`message_def_gpt`, `message_def_gemini`, `message_def_ollama`) yield incremental chunks. If you need the full brochure as a single string, collect the generator:

```python
def collect_text(gen):
    text = ''
    for chunk in gen:
        text += chunk
    return text

# usage
# full_text = collect_text(create_brochure('Name','https://...', 'GPT'))
```

- Ensure environment variables are set correctly. Missing API keys cause silent failures or errors.
- `method_utils.py` currently passes `gemini_api_key=GEMINI_API_KEY` to the Ollama call — if you use Ollama, verify and update that argument to the correct key/parameter or host setting.
- Prompt length: The prompt is truncated at 5,000 characters in `get_brochure_user_prompt`. If you need more context, increase the limit, or implement chunking + summarization.

## Security & Rate Limits

- Keep API keys out of source control. Use `.env` and a `.gitignore` entry for `.env`.
- LLM providers have rate limits and usage costs. Test with small prompts and monitor API usage.

## Next Steps / Improvements

- Add a `requirements.txt` or `pyproject.toml` with exact package versions.
- Add a `.env.example` showing environment variable names.
- Improve error handling and timeouts in `scrapper.py` and `method_utils.py`.
- Add caching for fetched pages to avoid repeated HTTP requests when iterating.

---

If you'd like, I can now:

- add `requirements.txt` with versions based on your environment,
- patch `method_utils.py` to return a single string (or both a streaming and non-streaming API), or
- add `.env.example` and a small test harness.

Tell me which of these you'd like next.
