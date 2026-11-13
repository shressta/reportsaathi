# System Architecture & Technical Specification: ReportSaathi

**Document Version:** 1.0  
**Status:** Approved for Implementation  
**Constraint Mandate:** Built exclusively using **free and open-source software (FOSS)** tools, prioritizing simplicity, zero-hallucination deterministic safety, and minimal hosting overhead.

---

## 1. Architecture Overview & Core Philosophy

ReportSaathi operates on a strict **safety-first, hybrid-deterministic architecture**:
* **Medical Logic & Translation:** **100% Deterministic Code.** Latin regimens, dosage counts, and lay Hindustani purpose strings are mapped via hardcoded rules and pre-vetted relational databases. Zero generative LLMs are permitted in the medical scheduling path.
* **Voice Synthesis:** **Open-Source Neural AI Model.** Neural Text-to-Speech (TTS) synthesizes the deterministic Hindi script into warm, natural, elder-friendly spoken audio.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLINIC LOCAL NETWORK                             │
│                                                                             │
│  [Screen 1: Assistant Desk]            [Screen 2: Doctor Console]           │
│  Browser (HTML5/HTMX)                  Browser (HTML5/HTMX)                 │
│         │                                     ▲                             │
│         │ 1. POST /api/prescriptions          │ 2. GET /api/reviews/pending │
│         ▼                                     │                             │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │               ReportSaathi Monolithic Core                   │           │
│  │                 (FastAPI + Python 3.12)                      │           │
│  ├───────────────────────────────┬──────────────────────────────┤           │
│  │  DETERMINISTIC PIPELINE       │  AI MODEL PIPELINE           │           │
│  │  • Drug Auto-Complete DB      │  • Neural Hindi TTS Engine   │           │
│  │  • Latin Regimen Parser       │    (Piper-TTS / Edge-TTS)    │           │
│  │  • Lay Hindustani Mapper      │    -> Outputs OGG Opus Audio │           │
│  │  • Cryptographic Audit Logger │                              │           │
│  └──────────────┬────────────────┴──────────────┬───────────────┘           │
│                 │                               │                           │
│                 ▼                               ▼                           │
│     [Local Thermal/A5 Printer]      [SQLite Embedded Database]              │
│       (window.print() / ESC-POS)           (WAL Mode)                       │
└─────────────────┬───────────────────────────────────────────────────────────┘
                  │
                  │ 3. Dispatch Webhook (HTTPS)
                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLOUD DELIVERY GATEWAY                           │
│                                                                             │
│                Meta WhatsApp Business Cloud API (Free Tier)                 │
│                                 │                                           │
│         ┌───────────────────────┴───────────────────────┐                   │
│         ▼                                               ▼                   │
│   [Audio Voice Note]                             [Visual Slip Image]        │
│   (42s Hindustani OGG)                           (High-Contrast PNG)        │
│         │                                               │                   │
│         └───────────────────────┬───────────────────────┘                   │
│                                 ▼                                           │
│                     [Screen 5: Patient Phone]                               │
│                   Native WhatsApp (No App Install)                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Stack Evaluation & Recommendation

We evaluate two lightweight, modern, free/open-source technology stacks suitable for single-developer development and low-cost deployment:

| Criterion | Option A: Python Monolith (FastAPI + HTMX + SQLite + Piper TTS) | Option B: Full-Stack TypeScript (Next.js + PostgreSQL + External TTS API) |
| :--- | :--- | :--- |
| **Backend & Logic** | **FastAPI (Python 3.12)**: Native async performance, Pydantic validation. | **Next.js / Node.js**: Heavy dependency tree, Node runtime overhead. |
| **Frontend Rendering**| **HTMX + Tailwind CSS (via CDN)**: Server-rendered HTML, 0 npm build steps, instantaneous reactivity. | **React 18 / Next App Router**: Large client-side JS bundles, client hydration penalties. |
| **Voice / AI Integration**| **Native Python AI Ecosystem**: Direct in-process execution of open-source TTS models (Piper-TTS / Edge-TTS) with zero external API fees. | **Requires External Microservice**: JS cannot easily run neural speech models locally; requires external Python sidecar or paid API. |
| **Database** | **SQLite (WAL mode)**: Zero-configuration, zero network latency, embedded single file, effortlessly backed up. | **PostgreSQL**: Requires standalone daemon, connection pooling, and multi-tenant hosting setup. |
| **Hosting Footprint** | **`< 150 MB RAM`**: Runs smoothly on free-tier containers (Render / Fly.io / Hugging Face Spaces) or a $3/mo mini-PC at the clinic. | **`> 512 MB RAM`**: Exceeds free tier container limits during React production builds. |

### Architectural Recommendation: OPTION A (Python Monolith)
**Why Option A Wins:**
1. **Direct Speech Model Execution:** Python is the native home for open-source AI. Running neural TTS directly inside the Python backend eliminates API billing and multi-container orchestration.
2. **Operational Simplicity:** A single FastAPI service with HTMX produces a complete SPA-like user experience for clinic staff without managing a `node_modules` directory, Webpack/Vite build steps, or client-server state synchronization.
3. **Rock-Solid Determinism:** Pydantic models guarantee strict type validation for drug names and dosing parameters.

---

## 3. Deterministic Code vs. AI Model Boundaries

To satisfy medical safety and prevent clinical hallucinations, system components are strictly segregated:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DETERMINISTIC CODE (100% Rule-Based)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Drug Auto-Complete & Formulation Lookup (Curated SQLite Table)            │
│ 2. Latin Regimen Parser (1-0-1 -> Morning/Night; PC -> After Meals)          │
│ 3. Lay-Language Purpose Mapping (Pre-vetted physician dictionary)            │
│ 4. Hindi Script Assembly (Deterministic string templates)                    │
│ 5. Audit Hashing (SHA-256 cryptographic signing of clinician sign-off)       │
│ 6. Print Slip Generation (CSS Grid / A5 layout)                              │
│ 7. Inbound WhatsApp Firewall (Hardcoded auto-redirect to clinic helpline)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Raw Hindi Text String
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI MODEL (Neural Inference Only)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Text-to-Speech (TTS) Engine:                                              │
│   Converts vetted Hindi text to OGG Opus audio.                             │
│   Model: Piper-TTS (`hi_IN` open voice) or Microsoft Edge-TTS (Free)        │
│   Constraint: Fixed pitch, 0.88x speed, zero freedom to alter words.         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Model & Database Schema

The database uses **SQLite 3** with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) enabled for high-concurrency read/write operations.

```sql
-- 1. Clinics and Registered Medical Practitioners (RMPs)
CREATE TABLE clinicians (
    id TEXT PRIMARY KEY,                       -- UUID
    full_name TEXT NOT NULL,                   -- e.g. "Dr. R. K. Verma"
    registration_number TEXT NOT NULL UNIQUE,  -- State Medical Council Reg No.
    clinic_name TEXT NOT NULL,                 -- e.g. "Verma Clinic & Daycare"
    phone_number TEXT NOT NULL,
    emergency_contact TEXT NOT NULL,           -- Displayed on patient slips
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Curated Essential Medicines Library (Top 300 Indian Outpatient Formulations)
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT NOT NULL,                  -- e.g. "Telma 40"
    generic_name TEXT NOT NULL,                -- e.g. "Telmisartan 40mg"
    category TEXT NOT NULL,                    -- "Hypertension", "Diabetes", etc.
    hindi_lay_name TEXT NOT NULL,              -- "टेल्मा 40"
    hindi_purpose TEXT NOT NULL,               -- "बीपी (खून का दबाव) सामान्य रखने के लिए"
    typical_form TEXT NOT NULL DEFAULT 'tablet'-- 'tablet', 'capsule', 'syrup'
);

-- 3. Patient Encounter Sessions
CREATE TABLE encounters (
    id TEXT PRIMARY KEY,                       -- UUID v4
    clinician_id TEXT NOT NULL,
    patient_mobile_hash TEXT NOT NULL,         -- SHA-256(phone + salt) for privacy
    patient_name TEXT NOT NULL,                -- Lay name (e.g. "रमेश कुमार")
    patient_age INTEGER NOT NULL,
    status TEXT CHECK(status IN ('DRAFT', 'PENDING_REVIEW', 'APPROVED', 'DISPATCHED', 'FAILED')) DEFAULT 'DRAFT',
    consent_obtained BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    FOREIGN KEY (clinician_id) REFERENCES clinicians(id)
);

-- 4. Prescribed Regimen Items (Child table of encounters)
CREATE TABLE encounter_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encounter_id TEXT NOT NULL,
    medicine_id INTEGER NOT NULL,
    dose_morning REAL NOT NULL DEFAULT 0,      -- e.g. 1.0 or 0.5
    dose_afternoon REAL NOT NULL DEFAULT 0,
    dose_night REAL NOT NULL DEFAULT 0,
    food_relation TEXT CHECK(food_relation IN ('AFTER_FOOD', 'BEFORE_FOOD', 'EMPTY_STOMACH')) DEFAULT 'AFTER_FOOD',
    special_instruction TEXT,                  -- Optional pre-vetted warning
    FOREIGN KEY (encounter_id) REFERENCES encounters(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- 5. Immutable Statutory Audit Log (DPDPA 2023 & NMC Compliance)
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encounter_id TEXT NOT NULL UNIQUE,
    clinician_id TEXT NOT NULL,
    clinician_reg_number TEXT NOT NULL,
    payload_hash TEXT NOT NULL,                -- SHA-256 of the exact JSON approved
    approved_timestamp TIMESTAMP NOT NULL,
    whatsapp_message_id TEXT,
    delivery_status TEXT DEFAULT 'PENDING'
);
```

---

## 5. API Routes & Endpoint Specifications

All endpoints are hosted on the monolithic FastAPI application.

### 5.1 Prescription Ingestion & Review APIs
* **`GET /`**: Renders Screen 1 (Prescription Quick-Entry) via HTMX.
* **`GET /api/medicines/search?q={query}`**: Instant JSON search returning top 10 matching medications from the 300-drug cache (`<20ms` latency).
* **`POST /api/encounters`**: Creates a draft encounter with prescribed drugs and patient mobile number. Returns redirect to Screen 2.
* **`GET /reviews/pending`**: Renders Screen 2 (Doctor Review Queue) displaying pending encounters for the logged-in clinician.
* **`POST /api/encounters/{id}/approve`**:
  * Triggers 1-click doctor sign-off.
  * Records cryptographic entry into `audit_logs`.
  * Asynchronously enqueues:
    1. Audio TTS synthesis.
    2. Image rendering of visual slip.
    3. WhatsApp API dispatch.
  * Returns HTMX partial confirming handoff to Screen 3.

### 5.2 Output & Delivery APIs
* **`GET /encounters/{id}/print`**: Renders clean, high-contrast, black-and-white HTML formatted with `@media print` CSS for standard A5 laser and 80mm thermal receipt printers.
* **`POST /webhooks/whatsapp`**: Handles incoming delivery status receipts (`sent`, `delivered`, `read`) from the Meta WhatsApp Cloud API and updates `audit_logs.delivery_status`.
* **`POST /webhooks/whatsapp/inbound`**: Intercepts any incoming text messages sent by patients. Automatically replies with a deterministic safety message:
  * *"नमस्ते, यह क्लीनिक की स्वचालित सूचना सेवा है। कृपया किसी भी सवाल या दवा बदलाव के लिए अपने डॉक्टर से संपर्क करें: {emergency_contact}।"*

---

## 6. Third-Party Services Evaluation

| Service Domain | Selected Tool / Provider | Licensing / Cost | Justification |
| :--- | :--- | :--- | :--- |
| **Optical Character Recognition (OCR)** | **EXCLUDED (None in MVP)** | Free / N/A | Handwritten Indian prescriptions cause severe OCR hallucinations (`02-research.md`). Fast auto-complete eliminates the need. |
| **Large Language Models (LLM)** | **EXCLUDED in Core Path** | Free / N/A | Core translation and schedule generation is 100% deterministic code to prevent hallucinations. |
| **Translation Engine** | **Internal Dictionary** | Open-Source (Built-in) | Hardcoded English-to-Hindustani medical purpose dictionary. Zero unconstrained translation drift. |
| **Text-to-Speech (TTS)** | **Piper-TTS / Edge-TTS** | MIT / Open-Source | High-quality, natural Devanagari Hindi neural voice models. Runs 100% free locally or via Python runtime. |
| **Messaging Gateway** | **Meta WhatsApp Cloud API** | **Free Tier** | Meta provides **1,000 free service conversations per month** for registered businesses. Zero software license cost. |
| **Maps & Geolocation** | **EXCLUDED (None needed)** | Free / N/A | Irrelevant to prescription schedule handoff. |

---

## 7. Authentication, Security & DPDPA 2023 Compliance

* **Clinic & Doctor Authentication:** Simple, secure session-based cookie authentication backed by PBKDF2/Argon2 password hashing for clinic staff and doctors. Individual doctors have unique PINs for 1-click approvals.
* **Patient Privacy & Ephemeral Minimization:**
  * Patients are never required to create accounts or passwords.
  * In compliance with Section 8 of DPDPA 2023, the patient's plaintext mobile number is kept in temporary memory only for WhatsApp dispatch. Once delivery is confirmed (or after a 72-hour window), the raw number is purged, leaving only a salted cryptographic hash (`patient_mobile_hash`) in the database.
* **Network Security:** Enforced HTTPS with TLS 1.3.

---

## 8. Deployment & Hosting Strategy

ReportSaathi can be deployed in two zero-cost / low-cost configurations:

### Configuration 1: Cloud-Hosted (Free Tier Ready)
* **Web & API Host:** **Render / Fly.io** (Free tier container, 512MB RAM).
* **Static Assets & Audio Storage:** Local container ephemeral storage or free **Cloudflare R2** bucket (10GB free tier) for caching audio notes.
* **Database:** SQLite database stored on a persistent volume mount (`/data/reportsaathi.db`).

### Configuration 2: Local Clinic Edge Deployment (Recommended for Indian OPDs)
* **Hardware:** Any existing Windows 10/11 desktop PC or a ₹4,000 Raspberry Pi 4 running inside the clinic.
* **Network:** Runs on `localhost:8000` accessible over the clinic's local Wi-Fi router.
* **Advantage:** 100% immune to clinic broadband outages. Direct, instant local USB thermal printing.

---

## 9. Environment Variables (`.env.example`)

```bash
# Server Configuration
ENV="production"
PORT=8000
SECRET_KEY="replace-with-a-secure-random-64-character-hex-string"
DATABASE_URL="sqlite:////data/reportsaathi.db"

# WhatsApp Business Cloud API (Free Tier from Meta for Developers)
WHATSAPP_API_TOKEN="EAAxxxxxxx..."
WHATSAPP_PHONE_NUMBER_ID="109876543210987"
WHATSAPP_BUSINESS_ACCOUNT_ID="123456789012345"
WHATSAPP_WEBHOOK_VERIFY_TOKEN="reportsaathi_verify_token_secure"

# TTS Engine Configuration ('piper' or 'edge')
TTS_ENGINE="edge"
TTS_VOICE_HINDI="hi-IN-MadhurNeural"
TTS_SPEED="0.88"

# Clinic Defaults
DEFAULT_CLINIC_NAME="Verma Clinic & Daycare"
DEFAULT_CLINIC_PHONE="011-23456789"
```

---

## 10. Open Questions (Unresolved Technical & Regulatory Nuances)

Rather than making risky assumptions, the following 4 questions are flagged for real-world validation during the 4-week pilot:

1. **Meta WhatsApp Business Onboarding Friction:** Does Meta's business verification process require official GSTIN and utility bill paperwork for every small, independent doctor clinic, or can ReportSaathi onboard multiple clinics under a unified multi-tenant Business Solution Provider (BSP) umbrella?
2. **Thermal Printer ESC/POS Fragmentation:** Indian retail pharmacies and clinics use a wide variety of unbranded Chinese 58mm/80mm thermal USB printers with non-standard ESC/POS protocols. Will browser-native `window.print()` with CSS `@page` styling be sufficient, or will an open-source local print spooler daemon (like `node-thermal-printer` or Python `python-escpos`) be needed?
3. **Doctor Authentication Legal Threshold:** Does the National Medical Commission (NMC) accept a clinic-session PIN authorization as a valid digital sign-off under the Telemedicine Practice Guidelines 2020, or will state medical councils eventually mandate Aadhaar e-Sign / Class 3 DSC tokens?
4. **Offline Resilience for Voice Delivery:** When a rural clinic loses internet connectivity, the physical slip prints immediately via local USB. How should WhatsApp voice note dispatches be queued and retried when the patient may have already left the clinic hours earlier?
