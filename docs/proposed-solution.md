# Proposed Solution: KaamConnect

**Tagline:** *Local Skills. Local Jobs. Better Opportunities.*

KaamConnect is a proposed hyper-local, voice-enabled job matching platform designed specifically for informal and semi-skilled workers, local households, contractors, and small businesses in non-metropolitan and semi-urban areas.

> **Project Scope Note:** This repository presents the complete system architecture, technical specifications, and a working Python matching-engine proof of concept (`poc/`). The full web application, live Firebase backend, and cloud deployments are planned for subsequent phases (see [Implementation Roadmap](implementation-roadmap.md)).

---

## Core Capabilities

### 1. Hyper-Local Job Discovery
- Captures worker and job-site coordinates via the Browser Geolocation API (with a manual town/pincode fallback when GPS permission is denied).
- Computes exact point-to-point distance using the **Haversine formula** so workers only see jobs within a practical commuting radius (e.g., 2 km to 15 km).

### 2. Skill-Based Worker–Employer Matching
- Replaces resume parsing with structured **trade skill tags** (e.g., `wiring`, `pipe_fitting`, `plastering`, `interior_painting`).
- Scores every worker–job pair transparently across five weighted criteria:
  - **Skill Compatibility (40%)**
  - **Location Proximity (30%)**
  - **Availability (15%)**
  - **Experience (10%)**
  - **Wage Compatibility (5%)**
- Returns human-readable match reasons so both workers and employers understand *why* a match was recommended.

### 3. Voice-Enabled & Accessible Interaction
- Integrates browser-based speech recognition (**Web Speech API**) so workers can speak queries naturally instead of typing, such as:
  - *"Find electrician jobs near me."*
  - *"Show plumbing jobs within five kilometres."*
  - *"Find construction work available today."*
- Designed for multilingual accessibility across **Kannada**, **Hindi**, and **English**, with **ElevenLabs** proposed for future natural voice responses (audio playback of job details).

---

## Proposed Feature Set

| Feature | Target User | Description | Current Status |
| :--- | :--- | :--- | :--- |
| **Hyperlocal Job Discovery** | Worker | Radius-based filtering using Haversine distance | POC Implemented (`poc/matching_engine.py`) |
| **Skill-Based Matching** | Worker & Employer | Weighted multi-factor scoring & ranking | POC Implemented (`poc/matching_engine.py`) |
| **Voice-Based Job Search** | Worker | Speech-to-text query capture & intent extraction | Architecture & Spec Documented |
| **Regional-Language Support** | Worker & Employer | Kannada, Hindi, and English UI & voice support | Architecture & Spec Documented |
| **Worker Profiles** | Worker | Phone-first profile with skills, wage, and availability | Schema & API Contract Defined |
| **Employer Job Postings** | Employer | Quick job creation with required skills and offered wage | Schema & API Contract Defined |
| **Nearby Worker Discovery** | Employer | Ranked list of available local workers for a job | POC Implemented (`poc/matching_engine.py`) |
| **Direct Communication** | Worker & Employer | Direct phone/contact handoff after application acceptance | Workflow & Security Designed |
| **Application Management** | Worker & Employer | Apply, shortlist, accept, or reject workflows | Schema & API Contract Defined |
