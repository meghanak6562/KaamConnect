# Proposed Technology Stack

This document outlines the proposed technologies for building KaamConnect from its current architecture and proof-of-concept stage into a full-scale production platform.

> **Note:** Only **Python** (used for the matching engine proof of concept) and **GitHub Actions** are active in this repository today. All other technologies listed below are **proposed** for the MVP and production phases.

---

| Layer | Technology | Status | Why It Is Proposed |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | **React.js** | Proposed | Component-based UI ideal for building distinct, simple Worker and Employer dashboards with fast mobile rendering. |
| **Frontend Language** | **TypeScript** | Proposed | Static typing prevents contract mismatches between UI forms, geolocation payloads, and REST API responses. |
| **Styling** | **Tailwind CSS** | Proposed | Utility-first CSS enables rapid development of high-contrast, touch-friendly interfaces for low-end mobile screens. |
| **Backend Framework** | **Python FastAPI** | Proposed | High-performance async Python framework with automatic OpenAPI docs, Pydantic validation, and native compatibility with the Python matching engine. |
| **Primary Database** | **Firebase Firestore** | Proposed | Serverless NoSQL document database with flexible schemas for diverse trade skills, real-time listeners for application updates, and generous free tier for hackathons/MVPs. |
| **Authentication** | **Firebase Authentication** | Proposed | Built-in Phone OTP authentication—critical because informal workers typically have a mobile number rather than an email address. |
| **Location Services** | **Browser Geolocation API** | Proposed | Zero-cost, native browser API to obtain GPS coordinates on smartphones without requiring a native mobile app install. |
| **Voice Input (STT)** | **Web Speech API** | Proposed | Free, browser-native Speech-to-Text supporting Indian locales (`kn-IN`, `hi-IN`, `en-IN`) for zero-typing job search. |
| **Voice Output (TTS)** | **ElevenLabs** | Proposed (Future) | High-naturalness AI voice synthesis proposed for future audio readouts of job descriptions and match summaries in regional languages. |
| **Cloud Infrastructure** | **AWS (S3, Lambda, API Gateway, CloudWatch)** | Proposed (Future) | Scalable cloud services for media/certificate storage, async notifications, API throttling, and centralized observability. |
| **Frontend Hosting** | **Vercel** | Proposed | Zero-config edge deployment for React/TypeScript SPAs with automatic HTTPS and preview URLs. |
| **Backend Hosting** | **Render** | Proposed | Simple managed container hosting for FastAPI services during MVP before scaling into full AWS infrastructure. |
