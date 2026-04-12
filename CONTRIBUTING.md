# Contributing to Snorq

## Setup

```bash
git clone https://github.com/snorqdevs/Snorq.git
cd Snorq
pip install -e ".[dev]"
pytest tests/ -v
```

## Branch Strategy

- `main` — stable
- `feature/<name>` — new skill signals or features
- `fix/<name>` — bug fixes

## Commit Style

```
feat(module): description
fix(module): description
test(module): description
docs: description
chore: maintenance
```

## Adding a New Signal

1. Add signal function to `snorq/signals.py`
2. Register in `evaluate_candidate()`
3. Rebalance weights to sum to 1.0
4. Add tests in `tests/test_signals.py` (minimum 5)
5. Update TypeScript types in `dashboard/src/types.ts`

## Pull Request

- `pytest tests/ -v` must pass
- No external dependencies in core
- New signal = new tests

## Code of Conduct

Ship real utility. No bloat.
