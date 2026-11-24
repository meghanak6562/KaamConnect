# KaamConnect Matching Engine (Proof of Concept)

This directory contains a lightweight, dependency-free Python proof of concept demonstrating KaamConnect's **hyper-local, skill-based matching engine**.

## Files

- `matching_engine.py` — Implements the Haversine distance formula, 5-factor weighted scoring (`40%` skill, `30%` location, `15%` availability, `10%` experience, `5%` wage), ranking, and match explanation generation.
- `sample_workers.json` — Sample informal & semi-skilled worker profiles around Tumakuru, Karnataka.
- `sample_jobs.json` — Sample local job postings from households and small businesses.
- `test_matching.py` — Automated `pytest` suite verifying distance math, scoring weights, ranking order, and edge cases.

## Running the Demonstration

```bash
python poc/matching_engine.py
```

## Running Tests & Syntax Checks

```bash
python -m py_compile poc/matching_engine.py poc/test_matching.py
pytest -v poc/test_matching.py
```
