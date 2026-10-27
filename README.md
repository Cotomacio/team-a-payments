# Team A — Payments Service (`team-a-payments`)

Example application repository demonstrating how an application team ("Team A") consumes the centralized **CodeMender Enterprise Reusable Workflows** (`Cotomacio/codemender-enterprise-workflows`).

## Workflows Inherited
- `.github/workflows/codemender-monthly-async.yml` -> Calls `Cotomacio/codemender-enterprise-workflows/.github/workflows/codemender-reusable.yml@main` (`deep` / `quick` scan + SARIF upload + GCS FinOps telemetry + Automated Fix PR).
- `.github/workflows/codemender-pr-gate.yml` -> Calls `Cotomacio/codemender-enterprise-workflows/.github/workflows/codemender-reusable.yml@main` (`diff` mode on Pull Requests).
