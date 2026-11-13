# Clinical & Statutory Safety Rules: ReportSaathi

**Document Version:** 1.0  
**Status:** Mandatory Operating Policy  
**Statutory Cross-References:** 
* Drugs and Cosmetics Act, 1940 & Rules, 1945
* Pharmacy Act, 1948
* Telemedicine Practice Guidelines, 2020 (MoHFW & National Medical Commission)
* Digital Personal Data Protection Act, 2023 (DPDPA 2023)
* CDSCO Medical Device Rules, 2017 (Software as a Medical Device - SaMD)
* Consumer Protection Act, 2019 (Sections 82–87: Product Liability)

---

## 1. The Core Invariant: Zero Diagnosis, Zero Treatment Alteration

> [!CAUTION]
> **The Prime Directive of ReportSaathi:**  
> The software shall **NEVER** diagnose an illness, predict pathology, assign clinical severity, or modify a doctor's prescribed treatment. Any code, prompt, template, or feature that breaches this directive is classified as a Critical Severity Hazard (Severity 1) and is strictly barred from the codebase.

---

## 2. The 10 Inviolable Safety Rules

### Rule 1: Zero Autonomous Diagnosis (CDSCO SaMD & NMC Clause 1.3.3)
* **Rule:** The system shall never assert, infer, or suggest any medical diagnosis, disease label, or clinical condition to a patient.
* **Prohibited Behavior:** Stating *"Your blood sugar indicates Type 2 Diabetes"* or *"This medicine is for your kidney damage"*.
* **Enforced Behavior:** The system describes only the intended pharmacological action as prescribed by the treating physician: *"यह दवा शुगर को सामान्य रखने के लिए है"* (This medicine is for keeping blood sugar normal).
* **Legal Rationale:** Under Clause 1.3.3 of the Telemedicine Practice Guidelines 2020 and Section 3 of the Indian Medical Degrees Act, only an RMP is legally licensed to practice medicine. Autonomous AI diagnosis violates statutory law and immediately reclassifies the tool as a Class C SaMD device under CDSCO MDR 2017.

---

### Rule 2: Zero Autonomous Treatment Modification or Deprescribing
* **Rule:** The system shall never recommend changing a dose, skipping a medication, altering timing contrary to the doctor's prescription, or advising deprescribing.
* **Prohibited Behavior:** Advising *"Take half a tablet if your BP drops"*, *"Skip night dose if you feel dizzy"*, or *"Stop this antibiotic after 3 days"*.
* **Enforced Behavior:** Every dose quantity, timing slot, and duration must mirror the doctor's prescription exactly. The system outputs a mandatory warning: *"डॉक्टर से पूछे बिना कोई दवा बंद न करें या खुराक न बदलें।"*
* **Legal Rationale:** Unlicensed modification of prescription drugs violates Section 18 of the Drugs and Cosmetics Act 1940 and Section 42 of the Pharmacy Act 1948, exposing developers and clinics to criminal prosecution.

---

### Rule 3: Zero Autonomous Drug Substitution
* **Rule:** The system shall never propose generic substitutions, brand swaps, or alternative medicine (Ayurvedic/Homeopathic) alternatives.
* **Prohibited Behavior:** Showing banners like *"Save 60% by switching to Generic Metformin"* or *"Try this herbal supplement instead"*.
* **Enforced Behavior:** The system strictly reproduces the specific brand or generic molecule selected by the treating doctor.
* **Clinical Rationale:** Bioequivalence variations, inactive binder allergies, and drug-drug interactions can cause acute clinical harm in elderly chronic patients.

---

### Rule 4: Mandatory Clinician-in-the-Loop Verification Gate
* **Rule:** No patient-facing output (printed visual slip or WhatsApp audio/text dispatch) shall ever be generated or transmitted without explicit, affirmative verification by an authenticated Registered Medical Practitioner or licensed pharmacist.
* **Technical Enforcement:**
  * The WhatsApp API dispatch webhook and local printer spooler are programmatically locked behind a valid `approved_by` clinician signature token.
  * System architecture does not expose any direct B2C patient intake endpoint.
* **Legal Rationale:** Ensures the software remains classified as an administrative decision-support drafting aid, preserving full clinical accountability under the treating doctor.

---

### Rule 5: 100% Deterministic Regimen Generation (Anti-Hallucination Firewall)
* **Rule:** All medication names, dosage numbers, frequency mappings, and lay-purpose strings must be generated through **deterministic code and relational database lookups**.
* **Prohibited Behavior:** Using Large Language Models (LLMs) or generative AI to parse or output dosage instructions, pill counts, or timing slots.
* **Enforced Behavior:** 
  * `1-0-1` $\rightarrow$ Morning: 1, Night: 1 (Pure mathematical parsing).
  * `PC` $\rightarrow$ After Food (Hardcoded dictionary mapping).
* **Engineering Rationale:** Generative LLMs exhibit non-zero hallucination rates, numerical drift, and prompt-injection vulnerabilities. In prescription management, a 0.1% error rate (e.g. 5mg vs 0.5mg) is clinically fatal.

---

### Rule 6: Absolute Exclusion of Diagnostic Scans & Medical Imaging
* **Rule:** The system shall never ingest, parse, OCR, summarize, or explain radiologic imaging films or diagnostic scan reports (MRI, CT, X-Ray, Ultrasound, Mammography, PET).
* **Enforced Behavior:** Ingestion interfaces strictly reject image uploads of radiological scans with an error banner: *"रेडियोलॉजी और स्कैन रिपोर्ट इस सेवा में समर्थित नहीं हैं। कृपया स्कैन रिपोर्ट की व्याख्या के लिए सीधे अपने विशेषज्ञ चिकित्सक से संपर्क करें।"*
* **Legal & Clinical Rationale:** Imaging interpretation carries the highest medical negligence liability and litigation rates in Indian consumer jurisprudence.

---

### Rule 7: DPDPA 2023 Data Privacy & Ephemeral Minimization
* **Rule:** Patient personal and health data must be protected through strict data minimization, encryption, and automated purging.
* **Enforced Technical Standards:**
  * **Multilingual Consent:** A mandatory consent statement in clear Hindi must be verbally acknowledged or tapped prior to dispatch.
  * **Ephemeral Storage:** The patient's raw 10-digit mobile number and encounter text are encrypted via AES-256 and purged from memory 72 hours after successful WhatsApp delivery.
  * **Zero Patient Tracking:** Only an irreversible, salted cryptographic hash (`SHA-256(phone + salt)`) is retained for audit logging.
* **Statutory Compliance:** Protects against massive penalties (up to ₹250 Crore) under Section 33 of the Digital Personal Data Protection Act, 2023.

---

### Rule 8: Emergency Escalation & Safe Fallback Protocols
* **Rule:** Every patient communication must prominently display local emergency escalation guidance and clinic contact details.
* **Mandatory Copy:** Every printed slip and WhatsApp message must conclude with:
  * *"⚠️ किसी भी गंभीर लक्षण (जैसे सीने में तेज दर्द, सांस लेने में तकलीफ, या चक्कर आना) की स्थिति में तुरंत नजदीकी अस्पताल की इमरजेंसी में जाएं।"*
  * *"क्लीनिक फोन नंबर: {emergency_contact}"*

---

### Rule 9: Immutable Cryptographic Audit Trail
* **Rule:** The system must cryptographically sign and store an immutable audit log for every approved encounter to provide definitive proof of clinician sign-off in the event of consumer disputes.
* **Required Log Schema:**
  $$\text{Payload Hash} = \text{SHA-256}(\text{EncounterID} + \text{RMP\_RegNo} + \text{Timestamp} + \text{ApprovedJSON})$$
* **Legal Rationale:** Under Sections 82–87 of the Consumer Protection Act 2019 (Product Liability), maintaining an unalterable proof of physician verification legally protects software operators from liability arising from doctor prescribing errors.

---

### Rule 10: Inbound WhatsApp Patient Message Firewall
* **Rule:** The system shall never engage in open-ended, two-way conversational chat with patients on WhatsApp.
* **Prohibited Behavior:** Answering patient queries like *"Can I drink tea after taking this?"* or *"My headache isn't gone, what should I do?"* via an AI chatbot.
* **Enforced Behavior:** Any incoming text or voice message received from a patient triggers an immediate, deterministic automated safety auto-reply:
  * *"नमस्ते, यह क्लीनिक की केवल-सूचना सेवा है। सुरक्षा कारणों से यह नंबर चिकित्सा सलाह या सवालों के जवाब नहीं दे सकता। कृपया सीधे अपने डॉक्टर से संपर्क करें: {clinic_phone}।"*
