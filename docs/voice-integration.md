# Voice Integration Architecture (Proposed)

Many informal and semi-skilled workers are more comfortable speaking in their regional language than typing English text into search forms. KaamConnect proposes a **voice-first search pipeline** supporting **Kannada**, **Hindi**, and **English**.

> **Status:** Proposed architecture only. Neither browser speech recognition nor ElevenLabs audio generation is wired into a live UI in this repository.

---

## Supported Sample Voice Queries

- *"Find electrician jobs near me."*
- *"Show plumbing jobs within five kilometres."*
- *"Find construction work available today."*
- Regional equivalents in Kannada (e.g., *"ಹತ್ತಿರದ ಎಲೆಕ್ಟ್ರಿಷಿಯನ್ ಕೆಲಸ ತೋರಿಸಿ"*) and Hindi (e.g., *"मेरे पास प्लंबर का काम दिखाओ"*).

---

## End-to-End Voice Processing Pipeline

1. **Microphone Input:** The worker taps a prominent microphone button in the React UI.
2. **Speech Recognition (Web Speech API):** The browser-native `SpeechRecognition` / `webkitSpeechRecognition` interface captures audio and converts it to text locally/via browser speech services using the user's `preferred_language` (`kn-IN`, `hi-IN`, or `en-IN`).
3. **Text Conversion:** The resulting transcript string is displayed on-screen for quick visual confirmation.
4. **Query Interpretation:** A lightweight NLU/keyword parser extracts:
   - **Trade / Skill:** e.g., `electrician`, `plumbing`, `construction`
   - **Radius:** e.g., `"five kilometres"` → `max_distance_km = 5`
   - **Urgency / Availability:** e.g., `"today"` → `availability = available`
5. **Location & Skill Extraction:** Combined with the user's Browser Geolocation coordinates (or manual town fallback).
6. **Matching Engine Execution:** The FastAPI backend runs the weighted matching engine against open jobs.
7. **Results Returned to User:** Ranked job cards are displayed with clear distance and daily-wage badges.

---

## Role Separation: Web Speech API vs. ElevenLabs

| Capability | Technology | Purpose in KaamConnect | Status |
| :--- | :--- | :--- | :--- |
| **Speech-to-Text (STT)** | **Web Speech API** | Captures worker's spoken search query directly in the mobile browser with zero API cost. | Proposed for MVP |
| **Text-to-Speech (TTS) / Audio AI** | **ElevenLabs** | Optional future enhancement to read matched job summaries aloud in natural regional-language voices for low-literacy users. | Proposed for Future Phase |

> **Important Distinction:** Web Speech API handles *voice input* (listening to the worker), whereas ElevenLabs is proposed strictly for *optional voice output* (speaking job details back to the worker). No live ElevenLabs API integration exists in this repository.
