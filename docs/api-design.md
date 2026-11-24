# API Design (Proposed REST Specification)

KaamConnect proposes a **Python FastAPI** REST backend secured by Firebase Authentication bearer tokens.

> **Status:** Proposed API contract only. The full OpenAPI 3.0 specification is defined in [`api/openapi.yaml`](../api/openapi.yaml). No live FastAPI server is implemented in this repository.

---

## Endpoint Summary

### Authentication
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new worker or employer user record after OTP verification. |
| `GET` | `/api/auth/me` | Retrieve the authenticated user's profile and role. |

### Workers
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/workers/profile` | Create or update a worker's skills, experience, expected wage, availability, and location. |
| `GET` | `/api/workers/nearby` | Discover available workers within a specified radius (`lat`, `lng`, `radius_km`, `skill`). |

### Employers
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/employers/profile` | Create or update an employer's business name, contact details, and location. |
| `GET` | `/api/employers/profile/{id}` | Retrieve an employer's public profile details. |

### Jobs
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/jobs` | Publish a new hyper-local job posting with required skills, offered wage, and coordinates. |
| `GET` | `/api/jobs` | List open jobs with optional profession or status filters. |
| `GET` | `/api/jobs/{id}` | Retrieve detailed information for a specific job posting. |

### Matching
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `GET` | `/api/matching/jobs` | Return ranked nearby jobs for a worker using the 5-factor matching engine. |
| `GET` | `/api/matching/workers` | Return ranked nearby workers for a specific job ID. |

### Applications
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/api/applications` | Submit a worker's application to an open job. |
| `GET` | `/api/applications/worker` | List all applications submitted by the authenticated worker. |
| `GET` | `/api/applications/employer` | List all applications received for the authenticated employer's jobs. |

---

## Sample Request & Response (`GET /api/matching/jobs`)

**Request:**
```http
GET /api/matching/jobs?worker_id=w_101&max_distance_km=10 HTTP/1.1
Authorization: Bearer <firebase_jwt_token>
```

**Response (`200 OK`):**
```json
{
  "worker_id": "w_101",
  "matches": [
    {
      "job_id": "j_201",
      "title": "Residential Wiring & MCB Board Repair",
      "total_score": 92.4,
      "distance_km": 1.8,
      "score_breakdown": {
        "skill_score": 100.0,
        "location_score": 88.0,
        "availability_score": 100.0,
        "experience_score": 100.0,
        "wage_score": 100.0
      },
      "reasons": [
        "Matched 2/2 required skills: wiring, mcb_repair",
        "Very close: 1.8 km away (within 10.0 km radius)",
        "Worker is currently available",
        "Experience meets requirement (5 yrs >= 2 yrs)",
        "Offered wage (₹750/day) meets expected wage (₹700/day)"
      ]
    }
  ]
}
```
