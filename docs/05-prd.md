# Product Requirements Document (PRD): ReportSaathi

**Document Version:** 1.0  
**Status:** Approved for Implementation  
**Product Reference:** Based on [docs/01-problem.md](01-problem.md), [docs/02-research.md](02-research.md), [docs/03-scope.md](03-scope.md), and [docs/04-design.md](04-design.md).

---

## 1. Product Overview & Strategic Objectives

ReportSaathi is a clinician-assisted health literacy co-pilot for Indian outpatient clinics and retail pharmacies. It transforms intimidating, jargon-filled medical prescriptions into **doctor-verified visual intake charts** and **colloquial Hindustani audio notes**, delivered directly to patients via physical printouts and WhatsApp voice notes.

### 1.1 Goals
1. **Zero Reading Barrier for Medication Adherence:** Enable semi-literate or elderly patients (specifically a 50+ solo living patient) to follow their exact daily medicine regimen without relying on guesswork or unverified family WhatsApp advice.
2. **Zero Clinician Disruption:** Add fewer than **30 seconds** of clinic assistant data-entry time and fewer than **15 seconds** of physician review time per patient encounter.
3. **100% Deterministic Safety:** Eliminate AI hallucination risks in medication names, dosages, frequencies, and meal timings by using deterministic translation logic and a mandatory Registered Medical Practitioner (RMP) sign-off gate.
4. **Statutory Regulatory Immunity:** Remain strictly exempt from CDSCO Software as a Medical Device (SaMD) Class B/C licensing by operating exclusively as an administrative drafting aid under the NMC Telemedicine Practice Guidelines 2020.
5. **Zero-Tech Patient Onboarding:** Require **zero app downloads, zero logins, and zero account setups** on the patient’s smartphone.

### 1.2 Non-Goals (Strict Prohibitions)
1. **No Autonomous Clinical Diagnosis:** The system will **never** diagnose conditions, interpret symptoms, predict disease progression, or assign severity scores to diagnostic lab values.
2. **No Treatment Alteration or Deprescribing:** The system will **never** recommend changing a dose, skipping a medication, altering timing contrary to the doctor's prescription, or advising deprescribing.
3. **No Drug Brand / Generic Substitutions:** The system will **never** suggest swapping a prescribed brand for an unprescribed generic or Ayurvedic/alternative medicine.
4. **No Diagnostic Imaging / Scan Interpretation:** The system will **never** ingest, analyze, or explain MRI, CT, X-ray, or Ultrasound films or radiologist impression texts.
5. **No Direct-to-Consumer Cursive Handwriting OCR:** The system will **never** offer a direct-to-patient camera OCR feature for deciphering handwritten Indian doctor notes at home.
6. **No Two-Way Conversational Medical Q&A:** The system will **never** provide an open-ended conversational medical chatbot for patients to ask unvetted clinical questions.

---

## 2. User Personas & User Stories

### Persona 1: Ramesh Kumar (The Solo Patient)
* **Demographics:** 50 years old, lives alone in a Tier-2/3 Indian city, educated up to 5th grade, native Hindi speaker.
* **Tech Setup:** Budget Android phone ($70 Redmi A series) with a prepaid 1.5GB/day data plan. Uses WhatsApp daily for voice notes and family calls, but struggles with English apps and typing.
* **Pain Point:** Leaves the clinic with 3 medicine strips and a scribbled prescription. Forgets which tablet is for BP and which is for sugar, and whether to take them before or after food.

### Persona 2: Dr. R. K. Verma (The Treating Physician / RMP)
* **Demographics:** 48-year-old General Physician running a busy urban/semi-urban clinic seeing 60–80 patients per OPD shift.
* **Pain Point:** Spends repetitive time explaining schedules that patients immediately forget. Worried about medical liability, patient compliance, and regulatory audits under NMC guidelines.
* **Need:** An instantaneous, verified handoff tool that improves patient outcomes without slowing down his consultation queue.

### Persona 3: Sunita (The Clinic Assistant / Compounder)
* **Demographics:** 24-year-old clinic receptionist/compounder operating the desktop computer at the registration desk.
* **Pain Point:** Handles patient queues, billing, and medicine dispensing. Has zero patience for bloated enterprise hospital software with 20 mandatory fields.

---

### User Stories

* **US-1 (Patient Home Adherence):** As a 50-year-old solo Hindi-speaking patient, I want to listen to a voice note on WhatsApp in warm spoken Hindustani that tells me exactly which tablet to take in the morning and at night, so that I take my medicines correctly without guessing.
* **US-2 (Patient Visual Reference):** As a patient who cannot read English medical terms, I want a printed card with Sun ☀️ and Moon 🌙 icons and bold numbers (`1 गोली`), so that I can keep it near my medicine box and verify my dose at a glance.
* **US-3 (Clinic Staff Data Ingestion):** As a busy clinic assistant, I want to type the first 3 letters of a prescribed medicine and select it from an auto-complete dropdown in under 30 seconds, so that I don't delay the clinic queue.
* **US-4 (Doctor 1-Click Verification):** As a treating doctor, I want to glance at a side-by-side view of the original prescription and the Hindi visual draft, and approve it with one click, so that my patient receives an accurate schedule while I retain full clinical oversight.
* **US-5 (Statutory Consent & Privacy):** As a patient, I want to receive my schedule on WhatsApp with a clear notice explaining how my mobile number is used, so that my personal health data is protected under Indian privacy laws.

---

## 3. Numbered Functional Requirements

### 3.1 Point-of-Care Prescription Ingestion (FR-1)
* **FR-1.1:** The system shall provide a single-page web interface optimized for rapid desktop/tablet keyboard entry by clinic staff.
* **FR-1.2:** The system shall capture a mandatory 10-digit Indian mobile number with regex validation (`^[6-9]\d{9}$`).
* **FR-1.3:** The system shall provide an auto-complete search field populated with the top 300 essential Indian outpatient pharmaceutical formulations (brand names, active salts, strength).
* **FR-1.4:** The system shall allow the operator to select frequency using standard presets: `1-0-0` (सुबह), `0-1-0` (दोपहर), `0-0-1` (रात), `1-0-1` (सुबह-रात), `1-1-1` (तीनों समय), and `SOS` (जरूरत पड़ने पर).
* **FR-1.5:** The system shall allow selection of meal relationship: `नाश्ते/खाने के बाद` (After food), `खाली पेट` (Empty stomach / Before breakfast), `खाने से पहले` (Before food).
* **FR-1.6:** The system shall allow adding multiple medications to a single encounter session and provide 1-click delete/edit buttons for each added item.
* **FR-1.7:** The system shall enforce a mandatory verbal consent confirmation checkbox (*"मरीज ने WhatsApp पर समय-पत्रक प्राप्त करने की सहमति दी है"*) before submitting.

### 3.2 Deterministic Simplification & Vernacular Mapping (FR-2)
* **FR-2.1:** The system shall deterministically map Latin medical abbreviations to standard Hindi visual time slots without using generative LLMs:
  * `OD (Morning)` / `1-0-0` $\rightarrow$ `☀️ सुबह`
  * `OD (Night)` / `0-0-1` $\rightarrow$ `🌙 रात`
  * `BD` / `1-0-1` $\rightarrow$ `☀️ सुबह` and `🌙 रात`
  * `TDS` / `1-1-1` $\rightarrow$ `☀️ सुबह`, `🌤️ दोपहर`, and `🌙 रात`
  * `AC` $\rightarrow$ `🍽️❌ खाली पेट / खाने से पहले`
  * `PC` $\rightarrow$ `🍽️✅ नाश्ते या खाने के बाद`
* **FR-2.2:** The system shall map each drug to a pre-vetted, non-diagnostic lay purpose string from a curated dictionary (e.g., *Telmisartan* $\rightarrow$ *"बीपी (खून का दबाव) सामान्य रखने के लिए"*).
* **FR-2.3:** The system shall generate a structured Hindustani text script for audio synthesis following a strict template:
  * *Template:* *"नमस्ते [मरीज का नाम/जी], [क्लीनिक का नाम] से आपकी दवाओं का समय: सुबह नाश्ते के बाद [दवा 1 का नाम], [खुराक] लें। यह दवा [उद्देश्य] के लिए है..."*

### 3.3 Audio Voice Note Synthesis (FR-3)
* **FR-3.1:** The system shall convert the generated Hindi script into natural, human-paced spoken audio using an open-source/free neural Text-to-Speech (TTS) model.
* **FR-3.2:** The speech rate shall be calibrated to 0.85x–0.90x normal speed to accommodate elderly listeners.
* **FR-3.3:** The audio output shall be encoded in OGG Opus format, with total file size constrained to `< 180 KB` for instant playback on low-bandwidth 2G/3G connections.

### 3.4 Clinician Review & Audit Logging (FR-4)
* **FR-4.1:** The system shall present a side-by-side verification screen displaying the raw clinical input alongside the generated Hindi visual card and audio transcript.
* **FR-4.2:** The system shall allow the clinician to make inline corrections to quantity, timing, or instructions with immediate real-time preview updates.
* **FR-4.3:** The system shall require the clinician to authenticate sign-off via a single button tap: *"अनुमोदित करें और भेजें (Approve & Send)"*.
* **FR-4.4:** Upon approval, the system shall record an immutable cryptographic audit record storing: `EncounterID`, `ClinicianID`, `ClinicianRegNumber`, `PatientMobileHash`, `ApprovedPayload`, and `Timestamp`.

### 3.5 Dual-Channel Output Delivery (FR-5)
* **FR-5.1:** **Print Delivery:** The system shall generate a high-contrast, black-and-white, print-ready document formatted for standard A5 laser printers and 80mm thermal receipt printers.
* **FR-5.2:** The printed slip shall feature universal visual icons (☀️, 🌤️, 🌙, 🍽️) and large numerical quantities (`1 गोली`) with minimum 24px/18pt font.
* **FR-5.3:** **WhatsApp Delivery:** The system shall trigger an automated dispatch via the WhatsApp Business API containing:
  1. The pre-synthesized Hindustani audio voice note.
  2. A high-contrast PNG image of the Visual Intake Slip.
  3. A concise text summary in Devanagari Hindi.
* **FR-5.4:** The system shall monitor delivery webhooks and display real-time status (`Sent`, `Delivered`, `Failed`) on the clinic confirmation screen.

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance & Latency
* **NFR-1.1:** Drug auto-complete search results shall return in `< 50 ms` from local memory/database.
* **NFR-1.2:** Audio TTS synthesis for a typical 45-second voice note shall complete in `< 4.0 seconds`.
* **NFR-1.3:** Total end-to-end processing time from Doctor 1-click approval to WhatsApp message dispatch shall be `< 8.0 seconds`.

### 4.2 Usability & Accessibility (Elderly & Vernacular Standards)
* **NFR-2.1:** Body text in Hindi (Devanagari) shall maintain a line-height of `1.55` to `1.65` across all screens to prevent clipping of upper and lower diacritic matras (`ि`, `ी`, `ु`, `ू`, `े`, `ै`).
* **NFR-2.2:** The interface shall achieve WCAG 2.1 AAA contrast ratio ($\ge 7:1$ for body text, $\ge 4.5:1$ for large headings and icons) on pure white background (`#FFFFFF`) to ensure outdoor readability on low-nit budget phone screens.
* **NFR-2.3:** All interactive touch targets shall have a minimum height and width of `56 px`, separated by at least `12 px` margins to mitigate mis-taps caused by hand tremors.
* **NFR-2.4:** The patient-facing mobile card shall be fully responsive on low-cost Android screens down to `360 px` viewport width without horizontal scrolling.

### 4.3 Reliability & Availability
* **NFR-3.1:** The clinic ingestion portal shall maintain 99.5% uptime during standard OPD clinic operating hours (08:00 to 21:00 IST).
* **NFR-3.2:** If the WhatsApp API gateway experiences an outage, the system shall fail gracefully by completing the local printout and flagging the encounter for automated WhatsApp retry once service resumes.

### 4.4 Data Protection & Privacy (DPDPA 2023)
* **NFR-4.1:** All patient personal data (mobile numbers, encounter notes) shall be encrypted at rest using AES-256 and in transit using TLS 1.3.
* **NFR-4.2:** **Ephemeral Data Minimization:** Patient raw phone numbers and medical payloads shall be purged from the active database after 72 hours, retaining only the irreversible SHA-256 hash and clinician sign-off timestamp for statutory audit defense.
* **NFR-4.3:** Notice of data collection and consent mechanisms shall be rendered in Hindi in compliance with Section 5 of DPDPA 2023.

---

## 5. Safety & Clinical Risk Requirements

* **SR-1 (Clinician Mandatory Gate):** No patient-facing output (printed slip or WhatsApp message) shall ever be generated or transmitted without an explicit affirmative click from an authenticated Registered Medical Practitioner or licensed pharmacist.
* **SR-2 (Deterministic Mapping Isolation):** Drug names, quantities, frequencies, and meal relations shall strictly originate from deterministic code templates. Generative LLMs are strictly barred from inventing or modifying medication parameters.
* **SR-3 (Hardcoded Non-Diagnostic Boundaries):** Purpose descriptions must describe the intended physiological target as instructed by the doctor (e.g. *"बीपी सामान्य रखने के लिए"*), never asserting an independent diagnostic claim (e.g. *"आपको उच्च रक्तचाप की बीमारी है"*).
* **SR-4 (Statutory Emergency Disclaimer):** Every print slip and WhatsApp delivery must feature an unalterable safety footer: *"⚠️ यह पत्रक केवल आपकी सुविधा के लिए डॉक्टर के परामर्श अनुसार तैयार किया गया है। डॉक्टर से पूछे बिना कोई दवा बंद न करें। आपातकाल में तुरंत अस्पताल जाएं।"*
* **SR-5 (Inbound Patient Chat Firewall):** Inbound patient replies to the WhatsApp delivery number shall be intercepted by an automated firewall rule that blocks conversational AI generation and replies with the clinic's physical phone number and emergency instructions.

---

## 6. Success Metrics & Key Performance Indicators (KPIs)

| Metric | Target (MVP Phase) | Measurement Method |
| :--- | :--- | :--- |
| **North Star: Doctor-Verified Safe Handoffs** | 1,000+ completed encounters in Month 1 | Encounters with completed clinician sign-off. |
| **Clinic Staff Entry Time** | `< 30 seconds` per prescription | Time from opening form to clicking "Send to Doctor". |
| **Doctor Review Time** | `< 15 seconds` per prescription | Time from opening review screen to clicking "Approve". |
| **Patient Audio Playback Rate** | `> 75%` of recipients listen to audio | WhatsApp voice note `Played` delivery receipt status. |
| **Zero SaMD / Diagnostic Incidents** | **0** autonomous diagnoses | Automated audit logs scanning 100% of generated copy. |
| **Prescription Transcription Error Rate** | `< 0.01%` (Target: 0%) | Clinician rejection rate during Screen 2 verification. |
| **WhatsApp Message Delivery Rate** | `> 95%` | Webhook delivery receipts over 10-digit mobile numbers. |
