# AI Cloud Load Tester

**AI-assisted cloud-native load testing for realistic API behavior.**

AI-Assisted-Cloud-Load-Tester is a portfolio cloud computing project that turns historical API access logs into synthetic user personas and runs persona driven load tests against a demo application before reporting likely performance bottlenecks. The project uses log ingestion, anonymization, user behavior modeling, containerized load agents, Kubernetes Jobs, and observability oriented reporting.

The goal is to demonstrate practical cloud engineering skills in a project that is realistic and easy to run locally.

---

## What the Project Does

The load tester helps developers answer a practical cloud reliability question:

> How will my application behave when realistic users, bots, and heavy shoppers interact with it all at the same time?

Instead of replaying a fixed script, AI-Assisted-Cloud-Load-Tester analyzes historical-style access logs and builds synthetic personas such as:

- **Power User**: fast navigation, many requests, frequent checkout behavior.
- **Window Shopper**: slower browsing, mostly read-heavy traffic.
- **Erratic Bot**: repeated requests, very low think time, and a higher chance of failures.

The system then uses those personas to generate load against a target API and produce a summary report showing latency, error rates, worst endpoints, and likely bottlenecks.

### Planned MVP Workflow

```bash
# 1. Start the demo application
docker compose up --build

# 2. Ingest sample access logs
load-tester ingest sample-data/access_logs.csv

# 3. Generate user personas from cleaned logs
load-tester model generate

# 4. Run a persona-driven load test
load-tester run \
  --target http://localhost:8000 \
  --duration 60 \
  --concurrency 50 \
  --persona-mix power_user=40,window_shopper=50,erratic_bot=10

# 5. Generate the latest bottleneck report
load-tester report latest
```

---

## Why the Project Is Useful

Traditional load tests often use simple scripts that do not reflect how real users behave. AI-Assisted-Cloud-Load-Tester focuses on behavior driven load generation: it models user sessions, endpoint transitions and think times so load tests are closer to real application traffic.

This project is useful because it demonstrates how cloud teams can:

- Convert raw traffic logs into anonymized behavioral data.
- Generate realistic synthetic users from historical request patterns.
- Run repeatable load tests locally or in Kubernetes.
- Identify slow endpoints and high-error workflows before production incidents.
- Apply cloud governance controls that prevent runaway tests and protect user data.

### Key Features

- **FastAPI demo application** with realistic API endpoints.
- **CSV log ingestion** with validation and malformed-row handling.
- **PII protection** through user identifier hashing.
- **Session reconstruction** from historical access logs.
- **Persona modeling** using rules and Markov-style endpoint transitions.
- **Async Python load agent** using configurable concurrency and duration.
- **Bottleneck reporting** with P95 latency, error rate, and persona failure attribution.
- **Docker-based local development** for repeatable setup.
- **Kubernetes manifests** for cloud-native deployment and load-agent Jobs.
- **Resource guardrails** such as max concurrency, max duration, and namespace quotas.
- **CI-ready structure** using pytest, Ruff, and GitHub Actions.

---

## Architecture Overview

AI-Assisted-Cloud-Load-Tester is organized into small, testable components.

```text
AI-Assisted-Cloud-Load-Tester/
├── demo/        # FastAPI target application used for testing
├── src
|   └── load_tester/     # Main Python package and CLI
│       ├── ingestion/   # CSV parsing, validation, anonymization, storage
│       ├── modeling/    # Session reconstruction and persona generation
│       ├── agent/       # Async load-generation agent
│       ├── reporting/   # Bottleneck detection and report generation
│       └── common/      # Shared config, logging, and utility code
├── personas/        # Generated persona JSON files
├── sample-data/     # Example access logs
├── deploy/          # Docker, Kubernetes, quotas, and service accounts
├── docs/            # Architecture, design decisions, governance, results
└── tests/           # Unit and integration tests
```

### Main Components

| Component | Purpose |
| --- | --- |
| Demo API | A small e-commerce-style service with product, cart, checkout, and health endpoints. |
| Ingestion Pipeline | Reads access logs, validates rows, hashes user IDs, and stores cleaned events. |
| Modeling Engine | Groups logs by session and generates synthetic user personas. |
| Load Agent | Sends probabilistic HTTP traffic based on persona behavior. |
| Orchestrator CLI | Provides commands for ingestion, modeling, running tests, and reporting. |
| Reporting Engine | Calculates latency percentiles, error rates, worst endpoints, and likely bottlenecks. |
| Kubernetes Layer | Runs the API and load agents using Deployments, Services, Jobs, and quotas. |

---

## How Users Can Get Started

### Prerequisites

Install the following tools:

- Python 3.11 or newer
- Docker Desktop or compatible Docker runtime
- Git
- Make, optional but recommended
- kubectl, optional for Kubernetes deployment
- kind or minikube, optional for local Kubernetes testing

### Clone the Repository

```bash
git clone https://github.com/<your-username>/ai-assisted-cloud-load-tester.git
cd ai-assisted-cloud-load-tester
```

### Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install Development Dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Run Quality Checks

```bash
ruff check .
ruff format --check .
pytest
```

### Start the Local Demo API

```bash
docker compose up --build
```

Once running, visit:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

### Example Usage

Ingest logs:

```bash
load-tester ingest sample-data/access_logs.csv
```

Generate personas:

```bash
load-tester model generate
```

Run a local load test:

```bash
load-tester run \
  --target http://localhost:8000 \
  --duration 60 \
  --concurrency 25 \
  --persona-mix power_user=40,window_shopper=50,erratic_bot=10
```

Generate a report:

```bash
load-tester report latest
```

Expected report output:

```text
Load Test Summary
-----------------
Duration: 60 seconds
Total Requests: 8420
Overall Error Rate: 2.4%
Worst Endpoint by P95 Latency: POST /checkout
Worst Endpoint by Error Rate: POST /checkout
Persona Causing Most Failures: erratic_bot
Likely Bottleneck: checkout database write path
```

---

## Kubernetes Quick Start

Kubernetes support is part of the MVP roadmap. Once the manifests are implemented, run:

```bash
kind create cluster --name load-tester
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/
```

Run a load-agent Job:

```bash
kubectl apply -f deploy/k8s/load-agent-job.yaml
```

Check Job status:

```bash
kubectl get jobs -n load-tester
kubectl get pods -n load-tester
```

---

## Security and Governance

AI-Assisted-Cloud-Load-Tester includes security and governance practices expected in production-minded cloud projects:

- User IDs are hashed during log ingestion.
- Raw personally identifiable information is not used for modeling.
- Load tests enforce maximum concurrency and duration limits.
- Docker containers should run as non-root users.
- Kubernetes manifests define resource requests and limits.
- Kubernetes ResourceQuota prevents runaway test workloads.
- ServiceAccounts follow least-privilege principles.

---

## Testing

Run the full test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=load_tester --cov-report=term-missing
```

Run formatting and linting:

```bash
ruff format .
ruff check .
```

---

## Documentation

Planned documentation lives in the `docs/` directory:

- `docs/architecture.md` explains system design and component responsibilities.
- `docs/design-decisions.md` records important implementation tradeoffs.
- `docs/security-governance.md` documents privacy, safety, and resource controls.
- `docs/demo-results.md` shows example reports, screenshots, and test results.

## Where Users Can Get Help

For help using or extending EchoPulse, start with:

- `README.md` for setup and common commands.
- `docs/architecture.md` for system design.
- `docs/design-decisions.md` for implementation reasoning.
- `docs/security-governance.md` for privacy and resource controls.
- GitHub Issues for bugs, questions, and feature requests.
- GitHub Discussions, if enabled, for design ideas and roadmap discussion.