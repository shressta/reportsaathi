# Product Scope & Core Flow Definition: ReportSaathi

Based on [docs/01-problem.md](01-problem.md) and [docs/02-research.md](02-research.md).

---

## 1. The Single Core Flow That Delivers Main Value

### Flow Title: The Clinician-Verified Intake & Audio Handoff
*(डॉक्टर की पर्ची, अपनी भाषा में — सही समय, सही खुराक)*

### Core Persona & Context
* **Patient:** 50-year-old Hindi-speaking patient living alone, leaving a clinic or pharmacy counter holding a handwritten/printed prescription and routine test slips.
* **Problem:** Cannot decipher clinical abbreviations (OD, TDS, AC, PC, mg), medical English jargon, or lab reference ranges. Zero at-home support. High risk of wrong dosing, dangerous food-drug interactions, and anxiety.
* **Core Value Delivered:** Transforming an intimidating clinical prescription into a **foolproof, visual, doctor-verified daily medicine schedule** delivered in **spoken everyday Hindustani** and a **tangible visual chart**, ensuring 100% adherence safety without requiring literacy or tech skills.

---

### End-to-End User Journey (Step-by-Step)

```
[ Clinic Desk / Pharmacy ]
           │
           ▼
1. INGESTION (Point-of-Care Assistant / Doctor)
   Staff selects prescribed medicines from auto-complete list (takes 20–30s).
   Enters patient mobile number.
           │
           ▼
2. AUTOMATED MAPPING & SIMPLIFICATION (ReportSaathi Engine)
   Translates Latin regimens (OD/BD/TDS, AC/PC) to visual icon slots (☀️/🌤️/🌙, 🍽️).
   Maps safe, non-diagnostic lay Hindustani purpose (e.g. "बीपी की गोली").
   Generates Hindi natural voice script.
           │
           ▼
3. CLINICIAN 1-CLICK VERIFICATION (<15–20s)
   Doctor or Pharmacist glances at visual screen, checks accuracy, clicks "Approve & Deliver".
   (Audit log recorded; legally compliant under Telemedicine Guidelines 2020).
           │
           ▼
4. DUAL-CHANNEL ZERO-FRICTION HANDOFF
   ├── A. Physical: Basic desk printer outputs high-contrast A5 visual intake chart.
   └── B. Digital Audio: Automated WhatsApp voice note + chart image sent to patient's phone.
           │
           ▼
[ Patient's Home ]
5. SAFE CONSUMPTION & ADHERENCE
   Patient pins visual chart near pillbox.
   Whenever taking medicine, taps WhatsApp voice note in warm spoken Hindi:
   "चाचाजी, सुबह नाश्ते के बाद यह नीली गोली लेनी है..."
```

---

## 2. Feature & Sub-Feature Breakdown

### Feature 1: Point-of-Care Prescription Ingestion (Clinician Web Interface)
* **1.1 Standardized Medicine Auto-Complete:** Search-as-you-type database of the top 300 essential Indian formulations (diabetes, hypertension, cardiac, antibiotics, gastro, analgesics). Eliminates spelling and handwriting ambiguities.
* **1.2 Regimen & Timing Selector:** Dropdown/quick-toggle for frequency (`1-0-1`, `0-1-0`, `1-1-1`, `SOS`) and relation to meals (`खाली पेट`, `नाश्ते/खाने के बाद`).
* **1.3 Patient Identifier & WhatsApp Field:** Single field for 10-digit Indian mobile number with DPDP-compliant verbal consent checkbox.

### Feature 2: Plain-Hindi Simplification & Audio Engine
* **2.1 Spoken Hindustani Regimen Generator:** Converts clinical jargon into everyday Hindustani (uses familiar terms like *"बीपी (खून का दबाव)"* instead of formal Sanskritized *"रक्तचाप"*).
* **2.2 Pre-Vetted Non-Diagnostic Purpose Library:** Hardcoded, doctor-authored 1-sentence explanations of *why* each medicine is taken (e.g., *"यह दवा शुगर को काबू में रखने के लिए है"*). Never diagnoses illness.
* **2.3 Visual Icon & Color Mapping System:** Standardized visual cues: Morning (Sun ☀️), Afternoon (Midday 🌤️), Night (Moon 🌙), Empty Stomach (Empty Plate 🍽️❌), After Food (Plate with Spoon 🍽️✅).
* **2.4 High-Fidelity Hindi Text-to-Speech (TTS):** Generates warm, human-paced audio voice notes simulating a respectful local compounder or physician speaking clearly.

### Feature 3: Clinician In-the-Loop Review & Approval Console
* **3.1 Side-by-Side Verification Screen:** Left side displays original input; right side displays the generated visual chart and Hindi voice transcript.
* **3.2 Rapid In-Line Modifier:** 1-click edits to adjust pill count or meal timing before sign-off.
* **3.3 One-Click Approval & Audit Logging:** "अनुमोदित करें और भेजें" (Approve & Send) button. Captures clinician ID, registration number, and timestamp to satisfy Telemedicine Practice Guidelines 2020.

### Feature 4: Dual-Channel Patient Delivery
* **4.1 Visual Intake Slip Generator (Print):** Instant PDF output formatted for standard A5 clinic printers or thermal receipt rolls, featuring large visual icons and bold Hindi numbers.
* **4.2 Automated WhatsApp Dispatcher:** Cloud API webhook delivering:
  * High-contrast visual schedule image.
  * Interactive WhatsApp Audio Note (OGG/MP3).
* **4.3 Multilingual Consent & Legal Safety Footer:** Clear non-diagnostic disclaimer required by DPDPA 2023.

### Feature 5: Safety, Privacy & Compliance Layer
* **5.1 Hardcoded Non-Diagnostic Guardrails:** Architecture blocks any freeform generation of diagnostic assertions or drug alteration advice.
* **5.2 Ephemeral Data Minimization (DPDPA 2023):** Patient phone number and medical details automatically encrypted and scrubbed after successful WhatsApp delivery.
* **5.3 RMP Audit Trail:** Permanent cryptographic log of clinician verification to protect against product liability under Consumer Protection Act 2019.

---

## 3. Product Sorting: MVP vs. Later vs. Never

| Feature / Sub-Feature | Category | Rationale & Regulatory Justification |
| :--- | :--- | :--- |
| **Clinician Web Entry with Top 300 Drug Auto-Complete** | **MVP** | Core input mechanism. Bypasses cursive handwriting failure while keeping staff data entry under 30 seconds. |
| **Rule-Based Visual Icon & Schedule Mapper** | **MVP** | Essential for illiteracy/semi-literacy. Converts clinical Latin symbols into universal visual icons. |
| **Pre-Vetted Hindi Purpose Library (Non-Diagnostic)** | **MVP** | Delivers peace of mind ("what is this medicine for?") without risking hallucination or autonomous diagnosis. |
| **Clinician Review & 1-Click Approval Screen** | **MVP** | **Non-negotiable safety & legal anchor.** Keeps tool outside CDSCO SaMD Class B/C; complies with Telemedicine Guidelines 2020. |
| **Printable Visual Intake Slip (A5 / Thermal)** | **MVP** | Immediate physical handoff at the clinic desk; works even if patient has no internet/data pack. |
| **WhatsApp Hindi Voice Note Dispatch** | **MVP** | Solves the solo 50-year-old living alone problem: audio instruction removes the reading barrier. |
| **Standard Hindi DPDP Consent & Disclaimer** | **MVP** | Statutory requirement under DPDPA 2023 (Section 5 multilingual notice). |
| **Routine Blood Lab Parameter Explainer (CBC, Sugar, Lipid)** | **Later** | High value, but secondary to daily medicine adherence. Adds data entry friction to MVP. |
| **Machine-Printed Lab PDF & EMR Ingestion (OCR/PDF Parsing)** | **Later** | Valuable automation for diagnostic chains, but core flow works reliably via structured auto-complete. |
| **Scheduled WhatsApp Dosage Reminders (Cron triggers)** | **Later** | Requires recurring scheduler, two-way delivery state tracking, and reminder opt-out mechanics. |
| **Regional Language Expansion (Marathi, Bengali, Telugu, etc.)** | **Later** | Important for national scale, but MVP must first achieve product-market fit in the core Hindi belt. |
| **Family / Caregiver WhatsApp Mirroring** | **Later** | Great for remote adult children, but requires secondary consent capture and phone routing logic. |
| **Hospital HMS / EMR Bidirectional Integration (FHIR/ABDM)** | **Later** | Long enterprise sales cycles and complex API certification. Standalone web console works day 1. |
| **Adhesive Thermal Sticker Printer for Medicine Strips** | **Later** | Requires specialized retail pharmacy hardware deployment. |
| **Autonomous Medical Diagnosis / Disease Labeling** | **NEVER** | **STRICT PROHIBITION.** Violates Telemedicine Guidelines Clause 1.3.3 and CDSCO SaMD rules. Diagnosis is exclusive to RMPs. |
| **Treatment Modification, Dosage Adjustment, Deprescribing** | **NEVER** | **STRICT PROHIBITION.** Violates Drugs & Cosmetics Act and Pharmacy Act. Altering doses creates fatal toxicity or cardiac collapse risk. |
| **Autonomous Drug Substitution (Brand to Generic / Ayurvedic)** | **NEVER** | High liability, consumer backlash, and bioequivalence risks. Doctor must select the exact formulation. |
| **Diagnostic Scan & Medical Imaging Interpretation (MRI, CT, USG)**| **NEVER** | High hallucination rates, catastrophic litigation risk under Consumer Protection Act 2019. |
| **Unassisted Patient Cursive Prescription Photo OCR** | **NEVER** | Indian doctor cursive handwriting OCR has intolerable error rates; reading 0.5mg as 5mg is fatal. |
| **Symptom Checker & Differential Diagnosis Decision Trees** | **NEVER** | Triggers cyberchondria, defensive over-triaging, and CDSCO Class C medical device classification. |
| **Two-Way Unconstrained AI Medical Chatbot for Patients** | **NEVER** | Hallucinates dangerous reassurance, displays sycophancy, and delays emergency medical intervention. |

---

## 4. Challenging the MVP (Ruthless Pruning)

To ensure the MVP is truly minimal and can be built, tested, and deployed rapidly without operational friction, every initial assumption was challenged:

### Challenge 1: Does MVP need Blood Test / Diagnostic Lab Explanations?
* **Assumption:** The problem statement mentions blood reports.
* **Challenge:** A patient takes medicines 2 to 3 times **every single day**, whereas blood tests are taken once every 3 to 6 months. Wrong dosing causes acute hospitalization within 48 hours; misunderstanding a borderline bilirubin level does not. Furthermore, entering 20 blood parameters at a busy OPD clinic counter takes 3–5 minutes—doctors and compounders will abandon the software.
* **Verdict: CUT FROM MVP (Moved to Later).** The MVP is 100% focused on **Medicine Intake & Regimen Safety**.

### Challenge 2: Does MVP need Computer Vision / OCR to read prescriptions?
* **Assumption:** Taking a photo of the prescription feels modern and effortless.
* **Challenge:** Research confirms OCR on Indian doctor handwriting fails catastrophically. The clinician or compounder would spend more time correcting OCR typos than typing fresh. Selecting 3 drugs from an auto-complete dropdown takes 15 seconds and has **0% OCR hallucination risk**.
* **Verdict: CUT FROM MVP (Vision OCR is Never for handwriting, Later for printed PDFs).**

### Challenge 3: Does MVP need a dedicated Patient Mobile App?
* **Assumption:** Digital health companies usually build Android apps.
* **Challenge:** A 50-year-old solo Hindi speaker with low digital literacy will not search the Play Store, download a 40MB app, complete OTP verification, and manage permissions.
* **Verdict: CUT PERMANENTLY FOR PATIENTS.** Zero-app delivery via printed paper and WhatsApp voice notes achieves 100% immediate usability.

### Challenge 4: Does MVP need bidirectional Clinic EMR Integration?
* **Assumption:** The software should plug directly into clinic EMR databases.
* **Challenge:** Indian outpatient clinics use fragmented software (or pure paper). Building bespoke integrations with Practo, KareXpert, or custom clinic databases delays launch by 6+ months.
* **Verdict: CUT FROM MVP (Moved to Later).** A standalone browser tab requiring zero installation works immediately on any computer, tablet, or smartphone at the clinic desk.

### Challenge 5: Does MVP need interactive two-way patient voice/text chat?
* **Assumption:** Patients might want to ask questions back to the AI.
* **Challenge:** An open conversational interface allows patients to ask "Can I skip my BP medicine?" or "Can I drink alcohol with this?". An AI answering autonomously violates Indian law and risks severe clinical harm.
* **Verdict: MOVED TO NEVER.** Communication to the patient must remain a one-way, doctor-approved briefing.

---

## 5. Summary of the Lean MVP

The resulting MVP consists of exactly **three screens and one background job**:
1. **Screen 1 (Clinic Assistant):** 30-second structured medicine selection + patient mobile number.
2. **Screen 2 (Doctor Review):** 15-second visual schedule verification + "Approve & Send" button.
3. **Background Job:** Synthesizes natural Hindi audio note and triggers WhatsApp message + local printer stream.
4. **Artifacts Received by Patient:** 
   - 1 high-contrast printed visual intake slip in hand.
   - 1 WhatsApp voice note in colloquial Hindustani explaining their exact daily schedule.
