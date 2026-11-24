# Architecture Diagrams Index

All architecture and workflow diagrams in this repository are authored in **Mermaid** so they render natively on GitHub and remain version-controllable as plain text.

## Available Diagrams

| Diagram | Standalone `.mmd` Source | Accompanying Documentation | Purpose |
| :--- | :--- | :--- | :--- |
| **System Architecture** | [`diagrams/system-architecture.mmd`](../diagrams/system-architecture.mmd) | [`docs/system-architecture.md`](system-architecture.md) | Six-layer component architecture from UI & Voice down to Cloud & Database. |
| **User Workflow** | [`diagrams/user-workflow.mmd`](../diagrams/user-workflow.mmd) | [`docs/system-workflow.md`](system-workflow.md) | End-to-end Worker and Employer journeys with decision branches. |
| **Data Flow** | [`diagrams/data-flow.mmd`](../diagrams/data-flow.mmd) | [`docs/data-flow.md`](data-flow.md) | Producers, processors, and consumers across registration, matching, and application. |
| **Matching Process Pipeline** | [`diagrams/matching-process.mmd`](../diagrams/matching-process.mmd) | [`docs/data-flow.md`](data-flow.md) | Step-by-step request execution pipeline from user input to ranked results. |
| **Deployment Architecture** | [`diagrams/deployment-architecture.mmd`](../diagrams/deployment-architecture.mmd) | [`docs/cloud-infrastructure.md`](cloud-infrastructure.md) | Proposed Vercel, Render, Firebase, and AWS cloud topology. |

---

## Visual Overview: Deployment Topology

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
