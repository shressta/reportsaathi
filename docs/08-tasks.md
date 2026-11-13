# Implementation Task List & Engineering Roadmap: ReportSaathi

**Document Version:** 1.0  
**Status:** Approved for Implementation  
**Prerequisites:** 
* Product Requirements Document: [docs/05-prd.md](05-prd.md)
* System Architecture & FOSS Stack: [docs/06-architecture.md](06-architecture.md)
* API Specification & Contracts: [docs/06a-api-contract.md](06a-api-contract.md)
* Statutory & Clinical Safety Rules: [docs/06b-safety-rules.md](06b-safety-rules.md)
* Master Test Plan: [docs/07-test-plan.md](07-test-plan.md)
* Test Fixtures: [tests/fixture/](file:///c:/Users/ADMIN/reportsaathi/tests/fixture/)

---

## 1. Project Phasing & Dependency Graph

Tasks are grouped into 5 sequential phases designed for single-PR atomic merging. Parallel tracks are explicitly indicated.

```
[Phase 1: Foundation & Walking Skeleton]
  │
  ├── T-01: API Contract & Pydantic Models ─────────┐
  │                                                  │
  ├── T-02: SQLite WAL Schema & 300-Drug Library*    │
  │                                                  ▼
  └── T-03: Deployed Walking Skeleton (FastAPI+HTMX)─┴──────────────┐
                                                                    │
┌───────────────────────────────────────────────────────────────────┘
│
├── [Track A: Deterministic Engine]      [Track B: Point-of-Care Frontend]
│   T-04: Latin Regimen Parser             T-07: Screen 1 Ingestion UI
│     │                                      │
│   T-05: Lay Hindustani Script Builder    T-08: Screen 2 Doctor Review*
│     │                                      │
│   T-06: Cryptographic Audit Trail        T-09: Screen 3 Dispatch Console
│     │                                      │
│     └──────────────────────┬───────────────┘
│                            │
▼                            ▼
[Phase 4: Output Delivery Pipelines]
  ├── T-10: Screen 4 High-Contrast Print CSS (A5 / Thermal) (Parallel)
  ├── T-11: Neural Hindi TTS Audio Pipeline (AI Engine)*    (Parallel)
  ├── T-12: Meta WhatsApp Cloud API Dispatcher*             (Parallel)
  └── T-13: Inbound WhatsApp Patient Safety Firewall
  │
  ▼
[Phase 5: Hardening, Compliance & End-to-End Verification]
  ├── T-14: DPDPA 72-Hour Ephemeral Data Purge Worker*
  ├── T-15: Automated Adversarial Safety Test Suite
  └── T-16: End-to-End Clinic OPD Handoff Simulation

* Marked tasks require Human Approval (Physician, Legal, or Meta KYC sign-off).
```

---

## 2. Phase 1: Contract, Database & Walking Skeleton

### Task T-01: OpenAPI 3.1 Contract & Pydantic Data Models
* **Owner:** Backend
* **Requirements Covered:** `FR-1.2`, `FR-1.4`, `FR-1.5`, `FR-1.7`
* **Tests Covered:** `TC-FR1-02`, `TC-FR1-03`, `TC-FR1-04`, `TC-FR1-05`
* **Dependencies:** None (First Task)
* **Description:** Implement all request, response, and entity data models using Pydantic v2 matching [docs/06a-api-contract.md](06a-api-contract.md). Includes 10-digit Indian mobile regex validator (`^[6-9]\d{9}$`), frequency presets (`1-0-0`, `0-0-1`, `1-0-1`, `1-1-1`, `SOS`), meal relation enums (`AFTER_FOOD`, `BEFORE_FOOD`, `EMPTY_STOMACH`), and common error models.
* **Definition of Done:**
  - [ ] Pydantic models compile with 100% strict type hints.
  - [ ] Automated unit tests validate that valid Indian numbers pass and non-compliant numbers fail.
  - [ ] `consent_obtained: false` triggers validation error.
  - [ ] PR passes `pytest` with zero warnings.

---

### Task T-02: SQLite WAL Database Setup & 300-Drug Formulation Seed Library
* **Owner:** Database
* **Requirements Covered:** `FR-1.3`, `FR-2.2`, `NFR-3.1`
* **Tests Covered:** `TC-FR1-01`, `TC-FR2-03`, `TC-NFR1-01`
* **Dependencies:** None (Can run in parallel with T-01)
* **Flag:** ⚠️ **NEEDS HUMAN APPROVAL:** A registered physician must review and sign off on the 300 drug lay-Hindi purpose strings (e.g. verifying that *Telmisartan* is described accurately without diagnostic labeling).
* **Description:** Initialize SQLite 3 database with WAL mode (`PRAGMA journal_mode=WAL;`). Implement schema migrations for `clinicians`, `medicines`, `encounters`, `encounter_items`, and `audit_logs` as specified in [docs/06-architecture.md](06-architecture.md). Seed the `medicines` table with 300 essential outpatient drugs including brand, generic, Hindi name, and doctor-vetted lay-purpose string.
* **Definition of Done:**
  - [ ] Migration script initializes clean database schema with foreign keys enabled.
  - [ ] Curated seed script inserts 300 essential medicines with complete Hindi lay strings.
  - [ ] Doctor sign-off documented in `tests/fixture/doctor_seed_signoff.md`.
  - [ ] Benchmark query `SELECT * FROM medicines WHERE brand_name LIKE 'telm%'` executes in `< 10ms`.

---

### Task T-03: Deployed Walking Skeleton (FastAPI + HTMX Shell)
* **Owner:** Backend / Frontend
* **Requirements Covered:** `FR-1.1`, `NFR-1.1`, `NFR-3.1`
* **Tests Covered:** `TC-NFR1-01`
* **Dependencies:** T-01, T-02
* **Description:** Create the core FastAPI application structure with Jinja2 templating and HTMX CDN integration. Implement basic routing, application configuration from `.env`, database session dependency, and a working healthcheck endpoint `GET /healthz`. Deploy the container to the target runtime (local Docker or free cloud container on Render/Fly.io) demonstrating an operational end-to-end request lifecycle.
* **Definition of Done:**
  - [ ] `GET /healthz` returns `{"status": "healthy", "database": "connected"}`.
  - [ ] Minimal HTML page renders in browser with Tailwind CSS and HTMX loaded via CDN.
  - [ ] Application starts cleanly via `uvicorn app.main:app --port 8000` consuming `< 120MB` RAM.
  - [ ] Dockerfile builds and runs successfully.

---

## 3. Phase 2: Core Deterministic Medical Engine

### Task T-04: Deterministic Latin Medical Regimen & Meal Relation Parser
* **Owner:** Backend
* **Requirements Covered:** `FR-2.1`, `SR-2`, `SR-3`
* **Tests Covered:** `TC-FR2-01`, `TC-FR2-02`, `TC-SR3-02`
* **Dependencies:** T-01, T-03
* **Description:** Implement pure mathematical parsing logic converting Latin abbreviations (`OD`, `BD`, `TDS`, `AC`, `PC`, `HS`, `SOS`, and numeric arrays `1-0-0`, `1-0-1`, `1-1-1`) into visual time slots: `MORNING` (☀️ सुबह), `AFTERNOON` (🌤️ दोपहर), `NIGHT` (🌙 रात), and `SOS` (जरूरत पड़ने पर). Generative LLMs are strictly barred from this pipeline.
* **Definition of Done:**
  - [ ] 100% test coverage over all dosage frequency variations in `tests/fixture/`.
  - [ ] `EMPTY_STOMACH` correctly tags `🍽️❌ सुबह खाली पेट (नाश्ते से आधा घंटा पहले)`.
  - [ ] Zero floating point arithmetic errors in half-tablet fractions (`0.5` $\rightarrow$ `"आधी गोली"`).
  - [ ] Deterministic unit tests pass in `< 10ms`.

---

### Task T-05: Colloquial Hindustani Lay Script Generator
* **Owner:** Backend
* **Requirements Covered:** `FR-2.2`, `FR-2.3`, `NFR-2.1`
* **Tests Covered:** `TC-FR2-03`, `TC-FR2-04`, `TC-SR2-02`
* **Dependencies:** T-02, T-04
* **Description:** Implement the script builder that converts structured schedule items into a natural, respectful Hindustani audio script for elderly solo patients. Adheres to the exact template defined in PRD Section 3.2. Enforces Devanagari line-height compatibility rules and rejects Sanskritized jargon in favor of spoken Hindustani (*"बीपी (खून का दबाव)"*, *"नाश्ते के बाद 1 गोली"*).
* **Definition of Done:**
  - [ ] Generated scripts match the exact wording of all 10 fixtures in `tests/fixture/`.
  - [ ] Automated regex scanner proves zero occurrences of blacklisted diagnostic phrases.
  - [ ] Script builder outputs structured text with mandatory doctor disclaimer footer.

---

### Task T-06: Cryptographic Audit Trail & State Immutability Engine
* **Owner:** Backend / Database
* **Requirements Covered:** `FR-4.3`, `FR-4.4`, `NFR-4.1`, `SR-1`
* **Tests Covered:** `TC-FR4-03`, `TC-FR4-04`, `TC-SR1-01`
* **Dependencies:** T-01, T-02, T-04
* **Description:** Build the clinician verification lock. When an authorized clinician signs off on an encounter, this module computes an immutable SHA-256 hash across `encounter_id`, `clinician_reg_number`, `approved_at`, and the canonical JSON payload, writing it to `audit_logs`. Once approved, the encounter is permanently frozen (`status: APPROVED`); any subsequent mutation attempt returns HTTP `409 Conflict`.
* **Definition of Done:**
  - [ ] Cryptographic hash is reproducible and tamper-evident.
  - [ ] State machine enforces that an encounter cannot be approved twice.
  - [ ] Direct dispatch without a valid audit hash is blocked with HTTP `403 Forbidden`.

---

## 4. Phase 3: Point-of-Care Clinic Interface (Screens 1, 2, 3)

*(Can run in parallel with Phase 2 once T-03 is complete)*

### Task T-07: Screen 1 — Prescription Quick-Entry Form (Point-of-Care Assistant)
* **Owner:** Frontend
* **Requirements Covered:** `FR-1.1`, `FR-1.2`, `FR-1.3`, `FR-1.6`, `NFR-1.1`, `NFR-2.3`
* **Tests Covered:** `TC-FR1-01`, `TC-FR1-02`, `TC-FR1-03`, `TC-FR1-05`, `TC-NFR1-01`
* **Dependencies:** T-01, T-03
* **Description:** Implement Screen 1 using HTMX and Tailwind CSS. Features 10-digit mobile field with regex validation, instant search-as-you-type drug auto-complete against `/api/v1/medicines/search`, quick-toggle buttons for frequency and meal timing, multi-drug list table with edit/remove buttons, and verbal consent checkbox.
* **Definition of Done:**
  - [ ] Staff can complete entry of a 3-drug prescription in `< 30 seconds`.
  - [ ] Auto-complete returns results in `< 50ms`.
  - [ ] Minimum touch target height of `56px` for all buttons; inputs meet WCAG AAA contrast.
  - [ ] Empty submission and invalid phone numbers show inline Hindi error banners without full page reload.

---

### Task T-08: Screen 2 — Clinician Verification & 1-Click Approval Screen
* **Owner:** Frontend / Backend
* **Requirements Covered:** `FR-4.1`, `FR-4.2`, `FR-4.3`, `SR-1`
* **Tests Covered:** `TC-FR4-01`, `TC-FR4-02`, `TC-FR4-03`, `TC-FR4-05`
* **Dependencies:** T-05, T-06, T-07
* **Flag:** ⚠️ **NEEDS HUMAN APPROVAL:** Clinical usability walk-through with an active practicing general physician to ensure review and approval takes `< 15 seconds`.
* **Description:** Build the Doctor / Pharmacist verification screen displaying a side-by-side view (Raw clinical input on left; generated Hindi visual schedule and audio script on right). Includes inline quantity/timing modifier, clinician PIN authentication dialog, and a high-contrast green approval button: *"✓ अनुमोदित करें और भेजें (Approve & Send)"*.
* **Definition of Done:**
  - [ ] Side-by-side comparison displays with 100% data fidelity.
  - [ ] Inline dose changes (e.g. 1.0 to 0.5 tablet) immediately re-render Hindi preview via HTMX.
  - [ ] Submitting approval triggers T-06 cryptographic sign-off and advances to Screen 3.
  - [ ] Invalid PIN rejects with HTTP `401 Unauthorized`.

---

### Task T-09: Screen 3 — Dispatch & Handoff Confirmation Console
* **Owner:** Frontend
* **Requirements Covered:** `FR-5.4`, `NFR-1.3`
* **Tests Covered:** `TC-FR5-03`, `TC-NFR1-02`
* **Dependencies:** T-06, T-08
* **Description:** Build the confirmation and handoff console showing real-time indicators for print status (`🖨️ प्रिंट सफल`) and WhatsApp delivery status (`📲 WhatsApp भेजा गया ✓✓`). Features a prominent primary button: *"+ अगले मरीज की पर्ची दर्ज करें (Next Patient)"* that resets the workflow to Screen 1.
* **Definition of Done:**
  - [ ] Displays doctor name, council registration number, and masked patient mobile.
  - [ ] Webhook triggers dynamically update delivery status badges via HTMX polling or SSE.
  - [ ] Next patient button clears session state cleanly.

---

## 5. Phase 4: Output Delivery Pipelines (Print, Voice, WhatsApp)

### Task T-10: Screen 4 — High-Contrast Visual Intake Slip (Print Engine)
* **Owner:** Frontend
* **Requirements Covered:** `FR-5.1`, `FR-5.2`, `NFR-2.1`, `NFR-2.2`
* **Tests Covered:** `TC-FR5-01`, `TC-NFR2-01`, `TC-NFR2-02`
* **Dependencies:** T-04, T-05, T-08
* **Description:** Implement `GET /encounters/{id}/print` returning an HTML page specifically optimized for mono laser A5 and 80mm thermal receipt printers. Layout features high-contrast black on white (WCAG AAA $\ge 7:1$), bold visual icons (☀️ Morning, 🌤️ Midday, 🌙 Night, 🍽️ Meal), giant numerical quantities (`32px`), Devanagari line-height `1.6`, and clinic emergency contact footer.
* **Definition of Done:**
  - [ ] Print preview rendered in Chrome/Edge fits entirely on a single A5 sheet with zero page-2 overflow.
  - [ ] Works cleanly on thermal receipt printer simulations.
  - [ ] Visual diff confirms zero clipping of Devanagari matras.

---

### Task T-11: AI — Hindi Neural Text-to-Speech (TTS) Synthesis Pipeline
* **Owner:** AI / Backend
* **Requirements Covered:** `FR-3.1`, `FR-3.2`, `FR-3.3`, `NFR-1.2`
* **Tests Covered:** `TC-FR3-01`, `TC-FR3-02`, `TC-FR3-03`
* **Dependencies:** T-05, T-08
* **Flag:** ⚠️ **NEEDS HUMAN APPROVAL:** Senior native Hindi speaker must audit the synthesized voice note for pronunciation, natural conversational pacing, and warmth.
* **Description:** Integrate the open-source neural TTS engine (Microsoft Edge-TTS or Piper-TTS Python runtime) configured with the `hi-IN-MadhurNeural` voice model. Speech rate is hardcoded to `0.88x` for elderly comprehension. Audio output is compressed and encoded into OGG Opus format, with file size strictly constrained to `< 180 KB`.
* **Definition of Done:**
  - [ ] Audio synthesis for a 70-word script executes in `< 3.5 seconds` on CPU.
  - [ ] Output audio file size is `< 180 KB` in OGG Opus format.
  - [ ] Audio plays back smoothly in native mobile browsers and WhatsApp media players.

---

### Task T-12: Meta WhatsApp Business Cloud API Integration
* **Owner:** Backend
* **Requirements Covered:** `FR-5.3`, `FR-5.4`, `NFR-3.2`
* **Tests Covered:** `TC-FR5-02`, `TC-FR5-03`, `TC-FR5-04`
* **Dependencies:** T-06, T-10, T-11
* **Flag:** ⚠️ **NEEDS HUMAN APPROVAL:** Clinic owner or administrator must complete Meta Business Manager KYC verification and register WhatsApp Business sender phone number.
* **Description:** Implement the outbound WhatsApp dispatch worker using the Meta WhatsApp Cloud API. Automatically sends: 1) the OGG audio voice note, 2) the visual intake chart PNG image, and 3) the structured Devanagari text summary. Implements inbound status webhook endpoint (`/webhooks/whatsapp`) to receive delivery receipts (`sent`, `delivered`, `read`). Includes exponential backoff retry for network resiliency.
* **Definition of Done:**
  - [ ] Automated end-to-end test delivers audio note and image to a test phone number.
  - [ ] Webhook receives and updates status to `DELIVERED` in database.
  - [ ] If Meta API returns 500/rate-limit, printout still succeeds and message is queued for background retry.

---

### Task T-13: Inbound WhatsApp Patient Message Safety Firewall
* **Owner:** Backend
* **Requirements Covered:** `SR-5`, `Safety Rule 10`
* **Tests Covered:** `TC-SR3-01`, `TC-SR5-01`
* **Dependencies:** T-12
* **Description:** Implement the inbound message firewall on `/webhooks/whatsapp/inbound`. Intercepts any incoming text, audio, or media messages sent by patients. Conversational LLMs are 100% blocked from responding. The firewall immediately returns an unalterable canned Hindi safety auto-reply directing the patient to their doctor and emergency clinic phone number.
* **Definition of Done:**
  - [ ] Automated test sends `"Kya mai dawai band kar du?"` to inbound webhook.
  - [ ] System sends canned clinic redirect within `< 1.5 seconds`.
  - [ ] Clinician dashboard flags that the patient texted in.
  - [ ] Zero AI model or chat generation is invoked.

---

## 6. Phase 5: Hardening, Compliance & End-to-End Verification

### Task T-14: DPDPA 2023 Ephemeral Data Purge Cron Worker
* **Owner:** Backend / Database
* **Requirements Covered:** `NFR-4.1`, `NFR-4.2`, `NFR-4.3`, `Safety Rule 7`
* **Tests Covered:** `TC-NFR4-01`, `TC-NFR4-02`
* **Dependencies:** T-06, T-12
* **Flag:** ⚠️ **NEEDS HUMAN APPROVAL:** Legal counsel or Data Protection Officer (DPO) sign-off on data retention and pseudonymization policy.
* **Description:** Implement a recurring background cleanup worker that runs hourly. Scans `encounters` table for records older than 72 hours. Permanently erases plaintext patient phone numbers and names, replacing them with `NULL`, while preserving the irreversible salted SHA-256 hash (`patient_mobile_hash`) and cryptographic audit record for medical negligence defense.
* **Definition of Done:**
  - [ ] Records older than 72 hours have phone and name scrubbed.
  - [ ] Audit log hash remains valid and verifiable after phone purge.
  - [ ] Legal compliance sign-off document committed to repository.

---

### Task T-15: Automated Adversarial Safety Test Suite
* **Owner:** AI / Backend
* **Requirements Covered:** `SR-1`, `SR-2`, `SR-3`, `SR-4`, `SR-5`
* **Tests Covered:** `TC-SR1-01`, `TC-SR2-01`, `TC-SR2-02`, `TC-SR3-01`, `TC-SR4-01`
* **Dependencies:** T-04, T-05, T-13
* **Description:** Build and execute automated security and clinical safety test suites utilizing `report-09-adversarial-scan-rejection.json` and `report-10-adversarial-diagnostic-prompt.json`. Verifies hard rejection of radiology scan uploads (HTTP 422), immunity against diagnostic prompt injections, and total exclusion of autonomous dosage modifications.
* **Definition of Done:**
  - [ ] 100% of adversarial safety tests pass in CI/CD pipeline.
  - [ ] Attempting to upload a CT scan returns HTTP `422` with Hindi rejection banner.
  - [ ] Blacklist assertion scanner passes with zero diagnostic assertions detected.

---

### Task T-16: End-to-End Clinic OPD Handoff Simulation
* **Owner:** Frontend / Backend
* **Requirements Covered:** All Functional & Safety Requirements
* **Tests Covered:** All 26 Test Cases in `docs/07-test-plan.md`
* **Dependencies:** All previous tasks (T-01 to T-15)
* **Description:** Execute end-to-end integration walkthrough across all 10 clinical fixtures in `tests/fixture/`. Run simulations on a low-cost Android phone (360px viewport) over simulated 2G/3G throttled networks. Verify end-to-end timing: Staff entry `< 30s`, Doctor review `< 15s`, Audio delivery `< 8s`, Audio download `< 2s`.
* **Definition of Done:**
  - [ ] All 10 fixtures in `tests/fixture/` execute successfully from entry to audio playback.
  - [ ] Zero layout breaks on 360px Android viewport.
  - [ ] Final sign-off meeting conducted with product owner and clinician.
  - [ ] Production deployment tag `v1.0.0-rc1` cut.

---

## 7. Parallel Execution Matrix

The following table shows which tasks can be worked on concurrently by different team roles:

| Sprint / Week | Backend Track | Frontend Track | Database Track | AI Track |
| :---: | :--- | :--- | :--- | :--- |
| **Sprint 1 (Days 1–3)** | **T-01:** Contract & Pydantic Models | *(Wireframing & Setup)* | **T-02:** SQLite WAL & Drug Library | *(Model evaluation)* |
| **Sprint 1 (Days 4–5)** | **T-03:** Walking Skeleton & Healthz | **T-03:** HTMX Layout Shell | *(Seed verification)* | *(Piper TTS testing)* |
| **Sprint 2 (Days 6–8)** | **T-04:** Latin Regimen Parser | **T-07:** Screen 1 Ingestion UI | **T-06:** Audit Table Schema | *(Dataset benchmarking)*|
| **Sprint 2 (Days 9–10)**| **T-05:** Hindustani Script Builder | **T-08:** Screen 2 Review UI | **T-06:** Cryptographic Hash | **T-11:** Neural TTS Engine |
| **Sprint 3 (Days 11–13)**| **T-12:** WhatsApp Cloud Dispatcher | **T-09:** Screen 3 Dispatch UI<br>**T-10:** Screen 4 Print CSS | *(Index tuning)* | **T-11:** Audio Quality Audit |
| **Sprint 3 (Days 14–15)**| **T-13:** Inbound Safety Firewall | **T-16:** 360px Mobile Audit | **T-14:** Ephemeral Purge Job | **T-15:** Safety Test Suite |
| **Sprint 4 (Days 16–18)**| **T-15:** Adversarial Testing | **T-16:** OPD Clinic Simulation | *(Backup verification)* | **T-16:** Audio Pacing Audit |

---

## 8. Human Approval Checkpoints Summary

| Task ID | Approval Role | What Is Being Approved | Blocker Impact |
| :--- | :--- | :--- | :--- |
| **T-02** | Registered Medical Practitioner (RMP) | Top 300 medicine lay-Hindi purpose strings (ensuring 0% diagnosis). | Cannot seed production database. |
| **T-08** | Treating Clinic Doctor | Screen 2 review interface workflow (ensuring review takes `< 15s`). | Cannot finalize clinic OPD handoff. |
| **T-11** | Native Hindi Elder / Linguist | Synthesized audio pronunciation, tone warmth, and `0.88x` pacing. | Cannot dispatch voice notes to patients. |
| **T-12** | Meta / Clinic Administrator | WhatsApp Business Account (WABA) KYC & sender phone number. | Cannot dispatch live WhatsApp messages. |
| **T-14** | Data Protection Officer / Legal | DPDPA 2023 72-hour ephemeral data purge & patient consent policy. | Cannot launch commercial clinic pilot. |
