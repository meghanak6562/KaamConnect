# Contributing to KaamConnect

Thank you for your interest in contributing to **KaamConnect**!

This repository is currently a **documentation-first architecture and proof-of-concept** project for **Problem Statement 4: Hyper-Local Job Matching for Informal & Semi-Skilled Workers**.

## How You Can Contribute

1. **Documentation & Architecture Improvements**
   - Refine system architecture diagrams in `diagrams/*.mmd` and `docs/`.
   - Improve API contract examples in `api/openapi.yaml`.
   - Add regional-language query examples for voice accessibility.

2. **Matching Engine Proof of Concept (`poc/`)**
   - Enhance scoring heuristics or edge-case handling in `poc/matching_engine.py`.
   - Add unit tests in `poc/test_matching.py`.

## Pull Request Workflow

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Verify the Python proof of concept and unit tests pass locally:
   ```bash
   python -m py_compile poc/matching_engine.py poc/test_matching.py
   pytest -v poc/test_matching.py
   ```
3. Ensure all Markdown links and Mermaid diagrams remain valid.
4. Open a Pull Request describing your changes clearly.

## Code of Conduct

Please be respectful, constructive, and inclusive when collaborating on issues and pull requests.
