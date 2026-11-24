# Cloud Infrastructure & AWS Integration Plan (Proposed)

KaamConnect proposes a pragmatic, two-stage cloud architecture: a low-friction MVP deployment using **Vercel**, **Render**, and **Firebase**, paired with a scalable **AWS** architecture for production growth.

> **Status:** Proposed architecture and future integration plan only. No AWS resources, IAM roles, or live cloud deployments are configured in this repository.

---

## Deployment Architecture Diagram

Standalone Mermaid source: [`diagrams/deployment-architecture.mmd`](../diagrams/deployment-architecture.mmd)

```mermaid
flowchart TB
    subgraph Client["Client Devices (Mobile & Desktop Browsers)"]
        PWA["React + TypeScript SPA"]
        MIC["Browser Microphone (Web Speech API)"]
        GPS["Browser Geolocation API"]
    end

    subgraph Edge["Frontend Hosting (Proposed)"]
        VER["Vercel Edge Network (Static Assets & SPA)"]
    end

    subgraph BackendHost["Backend Hosting (Proposed)"]
        REN["Render Web Service (Python FastAPI + Matching Engine)"]
    end

    subgraph Firebase["Firebase Services (Proposed)"]
        FAUTH["Firebase Authentication (Phone OTP)"]
        FDB["Cloud Firestore (NoSQL Document DB)"]
    end

    subgraph AWS["AWS Cloud Architecture (Proposed Future Integration)"]
        APIGW["Amazon API Gateway"]
        LAMBDA["AWS Lambda (Async Notifications & Batch Scoring)"]
        S3["Amazon S3 (Voice Clips & Verification Docs)"]
        CW["Amazon CloudWatch (Logs, Metrics & Alarms)"]
    end

    PWA <-->|HTTPS| VER
    MIC --> PWA
    GPS --> PWA
    PWA <-->|Auth Tokens| FAUTH
    PWA <-->|REST API| APIGW
    APIGW <-->|Routes| REN
    REN <-->|CRUD & Queries| FDB
    REN -.->|Async Events| LAMBDA
    REN -.->|Media Upload| S3
    REN -.->|Telemetry| CW
    LAMBDA -.->|Logs| CW
```

---

## Proposed AWS Services & Responsibilities

| AWS Service | Proposed Role in KaamConnect | Why It Fits |
| :--- | :--- | :--- |
| **Amazon API Gateway** | Front-door API management, rate limiting, CORS enforcement, and request throttling. | Protects backend matching endpoints from abuse and provides a unified HTTPS endpoint. |
| **AWS Lambda** | Serverless event-driven processing (e.g., sending job-match alerts, periodic cleanup of expired jobs, async audio processing). | Zero idle cost for spiky hyper-local workloads. |
| **Amazon S3** | Durable object storage for optional worker ID/skill verification documents, profile photos, and cached TTS audio clips. | Keeps binary media out of Firestore documents. |
| **Amazon CloudWatch** | Centralized application logs, API latency metrics, error alarms, and matching-engine performance dashboards. | Enables proactive monitoring and faster incident triage. |

---

## MVP vs. Production Hosting Path

1. **MVP Stage:** Frontend on **Vercel**, FastAPI backend on **Render**, Auth + Data on **Firebase**. Fast iteration with minimal DevOps overhead.
2. **Production / Scale Stage:** Introduce **Amazon API Gateway**, **AWS Lambda**, **Amazon S3**, and **Amazon CloudWatch** to handle higher regional traffic, async notifications, and enterprise-grade observability.
