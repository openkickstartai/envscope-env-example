# 🔬 EnvScope

**Cross-codebase environment variable topology analyzer.** Stop guessing which env vars your project needs.

EnvScope statically analyzes your codebase to find every environment variable read, detects dead configs, orphan reads, and inconsistent defaults.

## Features

- **Multi-language scanning** — Python (`os.getenv`, `os.environ`), Node.js (`process.env`), Go (`os.Getenv`)
- **Dead config detection** — Variables defined in `.env` but never read by code
- **Orphan read detection** — Variables read in code but missing from config files
- **Inconsistent default alerts** — Same variable with different defaults across files
- **Auto-generate `.env.example`** — Always-accurate config manifest from actual code reads

## Install

```bash
git clone https://github.com/openks/envscope && cd envscope
pip install -r requirements.txt
```

## Usage

```bash
# Scan current project
python main.py scan ./my-project

# Output as JSON (for CI pipelines)
python main.py scan ./my-project -f json

# Generate .env.example from code
python main.py generate ./my-project -o .env.example
```

## CI Guard Mode

Add to your GitHub Actions workflow:

```yaml
- run: python main.py scan . -f json
  # Exit code 1 = config issues found, fails the build
```

## Example Output

```
📊 EnvScope Scan: ./my-project
   12 env reads in source · 8 definitions in config

💀 Dead Configs (2):
   OLD_API_KEY                    defined .env:5
   LEGACY_MODE                    defined .env.example:12

👻 Orphan Reads (1):
   NEW_FEATURE_FLAG               read at src/app.py:42

⚠️  Inconsistent Defaults (1):
   PORT: "8080" @api/main.py:10 vs "3000" @web/server.js:5
```

## Running Tests

```bash
pytest test_envscope.py -v
```

## License

MIT
