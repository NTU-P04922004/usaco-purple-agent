# USACO Purple Agent
This repository implements a baseline purple agent for the USACO Benchmark on the [AgentBeats platform](https://agentbeats.dev/)
. The agent uses zero-shot prompting to solve USACO problems. The LLM API calls used by the agent are compatible with OpenAI client libraries.

## Project Structure
```
src/
├─ server.py      # Server setup and agent card configuration
├─ executor.py    # A2A request handling
├─ agent.py       # Your agent implementation goes here
└─ messenger.py   # A2A messaging utilities
.github/
└─ workflows/
   └─ test-and-publish.yml # CI workflow
tests/
└─ test_agent.py  # Agent tests
test_client.py    # Local test client
pyproject.toml    # Python dependencies
Dockerfile        # Docker configuration
```

## Getting Started
1. Clone the repo:
   ```bash
   git clone https://github.com/NTU-P04922004/usaco-purple-agent
   cd usaco-purple-agent
   ```

2. Set the following environment variables:
- `BASE_URL`: An API URL for the OpenAI-compatible API.
- `API_KEY`: An API key for the OpenAI-compatible API.
- `MODEL_ID`: A valid model ID supported by the target OpenAI-compatible API.

## Running Locally
```bash
# Install dependencies
uv sync

# Run the server
uv run src/server.py
```

For quick testing, run the following command
```bash
uv run test_client.py
```

## Running with Docker
```bash
# Build the image
docker build --platform linux/amd64 -t usaco-purple-agent .

# Run the container
docker run -p 9009:9009 --name usaco-purple-agent usaco-purple-agent
```

## Testing
Run A2A conformance tests against your agent.

```bash
# Install test dependencies
uv sync --extra test

# Start your agent (uv or docker; see above)

# Run tests against your running agent URL
uv run pytest --agent-url http://localhost:9009
```

## Publishing
The repository includes a GitHub Actions workflow that automatically builds, tests, and publishes a Docker image of your agent to GitHub Container Registry.

If your agent needs API keys or other secrets, add them in Settings → Secrets and variables → Actions → Repository secrets. They'll be available as environment variables during CI tests.

- **Push to `main`** → publishes `latest` tag:
```
ghcr.io/<your-username>/usaco-purple-agent:latest
```

- **Create a git tag** (e.g. `git tag v1.0 && git push origin v1.0`) → publishes version tags:
```
ghcr.io/<your-username>/usaco-purple-agent:1.0
```

Once the workflow completes, find your Docker image in the Packages section (right sidebar of your repository). Configure the package visibility in package settings.

## References
- [AgentBeats Platform](https://agentbeats.dev/)
- [Official USACO benchmark repo](https://github.com/princeton-nlp/USACO)