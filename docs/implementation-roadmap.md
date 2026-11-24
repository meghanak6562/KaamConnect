# Implementation Roadmap

KaamConnect is structured into five progressive engineering phases. **This repository covers Phase 1 (Architecture & Documentation) and Phase 2 (Matching Engine Proof of Concept).**

---

## Phase 1: Ideation and Architecture *(Completed in This Repository)*
- [x] Finalize official Problem Statement 4 scope.
- [x] Define Worker and Employer user roles and workflows.
- [x] Design six-layer system architecture and data-flow pipelines.
- [x] Define weighted matching algorithm and Haversine distance model.
- [x] Author OpenAPI specification, Firestore schema, and security documentation.

## Phase 2: Proof of Concept *(Completed in This Repository)*
- [x] Implement core matching logic in Python ([`poc/matching_engine.py`](../poc/matching_engine.py)).
- [x] Validate skill compatibility and Haversine geographic distance scoring.
- [x] Demonstrate ranked job and worker matching with human-readable reasons.
- [x] Add automated unit tests ([`poc/test_matching.py`](../poc/test_matching.py)) and GitHub Actions CI ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)).

## Phase 3: MVP Development *(Planned)*
- [ ] Build mobile-first Worker and Employer React + TypeScript interfaces.
- [ ] Implement Python FastAPI endpoints matching `api/openapi.yaml`.
- [ ] Integrate Firebase Authentication (Phone OTP) and Cloud Firestore.
- [ ] Enable end-to-end job posting, hyper-local discovery, and application management.

## Phase 4: Accessibility & Regional Languages *(Planned)*
- [ ] Integrate Web Speech API for voice-based job search.
- [ ] Add Kannada, Hindi, and English UI translations and voice intent parsing.
- [ ] Conduct usability testing with informal workers on low-end Android browsers.
- [ ] Evaluate ElevenLabs TTS for spoken job summaries.

## Phase 5: Cloud Deployment & Scale *(Planned)*
- [ ] Deploy React frontend to Vercel and FastAPI backend to Render.
- [ ] Configure Amazon CloudWatch monitoring, S3 document storage, and Lambda async notifications.
- [ ] Pilot in a target Tier-2/Tier-3 town and iterate on matching weights.
