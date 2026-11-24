# Security and Privacy Architecture (Proposed)

Because KaamConnect handles personal phone numbers, precise GPS coordinates, and employment records for vulnerable informal workers, privacy-by-design is a core architectural requirement.

> **Status:** Proposed security design. No live authentication, Firestore rules, or encryption infrastructure is deployed in this repository.

---

## 1. User Authentication
- **Phone OTP via Firebase Authentication:** Eliminates password reuse and email requirements while verifying real mobile numbers.
- **Short-Lived JWTs:** Every API request to FastAPI carries a Firebase ID token validated on the server.

## 2. Role-Based Authorization (RBAC)
- Users are assigned an explicit `role` (`"worker"` or `"employer"`).
- Workers can only modify their own `workers` profile and submit `applications` as themselves.
- Employers can only create/edit `jobs` owned by their `employer_id` and review `applications` for their own jobs.

## 3. Location Privacy & Consent
- **Explicit Consent:** The UI requests browser geolocation only when the user initiates location sharing or job search, with clear explanation in their preferred language.
- **Manual Fallback:** Users who decline GPS permission can select a town or pincode manually.
- **Coordinate Masking:** Exact worker coordinates are never exposed publicly to employers; the API returns only rounded distance (e.g., `2.4 km away`).

## 4. Protection of Contact Details
- Worker and employer phone numbers remain hidden during browsing.
- Direct contact details are exchanged **only** after an employer accepts a worker's application (or explicitly shortlists/contacts them under mutual consent).

## 5. Secure API Communication & Input Validation
- All client–server traffic is enforced over **HTTPS/TLS**.
- FastAPI **Pydantic** schemas validate coordinate bounds (`-90 <= lat <= 90`, `-180 <= lng <= 180`), positive wages, and allowed enum values to prevent injection or malformed payloads.

## 6. Proposed Firestore Security Rules
- Deny all unauthenticated reads/writes by default.
- Enforce `request.auth.uid == resource.data.uid` for profile updates.
- Restrict `applications` status transitions (`pending` → `accepted` / `rejected`) to the owning employer.

## 7. Credential & Secret Protection
- Environment variables (`.env`), Firebase service account keys, and future AWS/ElevenLabs keys are strictly excluded from version control via `.gitignore` and managed via hosting secret stores (Vercel/Render/AWS Secrets Manager).
