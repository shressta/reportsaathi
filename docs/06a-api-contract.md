# API Specification & Data Contracts: ReportSaathi

**Document Version:** 1.0  
**Status:** Approved for Implementation  
**Standard:** OpenAPI 3.1.0 / JSON Schema Draft 2020-12  
**Base URL:** `https://api.reportsaathi.in/v1` (or `http://localhost:8000/api/v1` for local clinic edge deployments)

---

## 1. Authentication & Common Headers

All clinic-facing endpoints require session-based cookie authentication or Bearer token authorization. Webhook endpoints authenticate via provider-specific cryptographic signatures.

### Common Request Headers
```http
Authorization: Bearer <session_or_api_token>
Content-Type: application/json
Accept: application/json
X-Clinic-ID: "clinic_delhi_042"
```

### Common Error Model (`ErrorResponse`)
```json
{
  "error": {
    "code": "INVALID_PHONE_NUMBER",
    "message": "कृपया 10 अंकों का मान्य भारतीय मोबाइल नंबर दर्ज करें।",
    "details": [
      {
        "field": "patient_phone",
        "issue": "Must match regex ^[6-9]\\d{9}$"
      }
    ],
    "timestamp": "2026-11-13T08:30:00Z"
  }
}
```

---

## 2. Endpoints & Schemas

### 2.1 Medicine Search API

#### `GET /medicines/search`
**Description:** Fast auto-complete lookup against the curated library of top 300 Indian outpatient formulations. Bypasses cursive prescription OCR and eliminates typos.

* **Query Parameters:**
  * `q` (string, required): Search query (minimum 2 characters, matches brand or generic name).
  * `limit` (integer, optional, default: 10, max: 20).

* **Response: `200 OK`**
```json
{
  "query": "telm",
  "count": 2,
  "results": [
    {
      "medicine_id": 104,
      "brand_name": "Telma 40",
      "generic_name": "Telmisartan 40mg",
      "category": "Cardiovascular / Hypertension",
      "hindi_lay_name": "टेल्मा 40",
      "hindi_purpose": "बीपी (खून का दबाव) सामान्य रखने के लिए",
      "typical_form": "tablet",
      "default_timing": "MORNING",
      "default_food": "AFTER_FOOD"
    },
    {
      "medicine_id": 105,
      "brand_name": "Telma-H",
      "generic_name": "Telmisartan 40mg + Hydrochlorothiazide 12.5mg",
      "category": "Cardiovascular / Hypertension",
      "hindi_lay_name": "टेल्मा-एच",
      "hindi_purpose": "बीपी (खून का दबाव) सामान्य रखने के लिए",
      "typical_form": "tablet",
      "default_timing": "MORNING",
      "default_food": "AFTER_FOOD"
    }
  ]
}
```

---

### 2.2 Encounter Ingestion API

#### `POST /encounters`
**Description:** Point-of-care ingestion endpoint invoked by clinic assistant/compounder to submit a patient prescription draft.

* **Request Body (`CreateEncounterRequest`):**
```json
{
  "patient_name": "रमेश कुमार",
  "patient_age": 50,
  "patient_gender": "MALE",
  "patient_phone": "9876543210",
  "consent_obtained": true,
  "items": [
    {
      "medicine_id": 104,
      "dose_morning": 1.0,
      "dose_afternoon": 0.0,
      "dose_night": 0.0,
      "food_relation": "AFTER_FOOD",
      "is_sos": false
    },
    {
      "medicine_id": 208,
      "dose_morning": 0.0,
      "dose_afternoon": 0.0,
      "dose_night": 1.0,
      "food_relation": "AFTER_FOOD",
      "is_sos": false
    }
  ]
}
```

* **Response: `201 Created` (`EncounterDetailResponse`):**
```json
{
  "encounter_id": "enc_8f7b2c9a-41e3-4f9a-a827-02b4d7c81920",
  "status": "PENDING_REVIEW",
  "created_at": "2026-11-13T08:30:15Z",
  "patient_summary": {
    "name": "रमेश कुमार",
    "age": 50,
    "phone_masked": "XXXXX-43210"
  },
  "mapped_schedule": [
    {
      "slot": "MORNING",
      "slot_hindi": "☀️ सुबह",
      "timing_detail": "नाश्ते के बाद",
      "medicines": [
        {
          "medicine_id": 104,
          "display_name": "टेल्मा 40 (Telma 40)",
          "quantity": 1.0,
          "unit_hindi": "गोली",
          "purpose_hindi": "बीपी (खून का दबाव) सामान्य रखने के लिए",
          "food_icon": "🍽️"
        }
      ]
    },
    {
      "slot": "NIGHT",
      "slot_hindi": "🌙 रात",
      "timing_detail": "खाने के बाद",
      "medicines": [
        {
          "medicine_id": 208,
          "display_name": "ग्लाइकोमेट 500 (Glycomet 500)",
          "quantity": 1.0,
          "unit_hindi": "गोली",
          "purpose_hindi": "शुगर (मधुमेह) नियंत्रण के लिए",
          "food_icon": "🍽️"
        }
      ]
    }
  ],
  "audio_script_preview": "नमस्ते रमेश जी, डॉ. वर्मा क्लीनिक से आपकी दवाइयों का नियम: सुबह नाश्ते के बाद टेल्मा 40 की एक गोली लें, यह बीपी के लिए है। रात को खाने के बाद ग्लाइकोमेट 500 की एक गोली लें, यह शुगर के लिए है। डॉक्टर से पूछे बिना कोई दवा बंद न करें।"
}
```

* **Error Responses:**
  * `422 Unprocessable Entity`: Invalid phone number, missing consent, or empty items array.
  * `400 Bad Request`: Incompatible dosage values (e.g. negative quantities).

---

### 2.3 Verification & 1-Click Approval API

#### `POST /encounters/{encounter_id}/approve`
**Description:** Doctor/RMP 1-click verification gate. Cryptographically signs the encounter, freezes the payload, and enqueues dual-channel dispatch.

* **Request Body (`ApproveEncounterRequest`):**
```json
{
  "clinician_id": "doc_verma_88419",
  "clinician_pin": "4819",
  "action": "APPROVE"
}
```

* **Response: `200 OK` (`ApprovalSuccessResponse`):**
```json
{
  "encounter_id": "enc_8f7b2c9a-41e3-4f9a-a827-02b4d7c81920",
  "status": "APPROVED",
  "approved_at": "2026-11-13T08:31:02Z",
  "audit_trail": {
    "clinician_reg_number": "RMP-UP-88419",
    "payload_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "signature_timestamp": "2026-11-13T08:31:02.104Z"
  },
  "dispatch_jobs": {
    "print_job_id": "prn_001928",
    "print_status": "QUEUED",
    "whatsapp_job_id": "wa_991827",
    "whatsapp_status": "QUEUED"
  }
}
```

* **Error Responses:**
  * `401 Unauthorized`: Invalid clinician PIN or missing authorization.
  * `409 Conflict`: Encounter already approved or cancelled.

---

### 2.4 Print Document Endpoint

#### `GET /encounters/{encounter_id}/print`
**Description:** Renders a clean, high-contrast, black-and-white HTML page with print-specific CSS (`@media print`) sized for A5 sheets or 80mm thermal receipt rolls.

* **Headers:** `Accept: text/html`
* **Response: `200 OK`** (HTML document with zero external asset dependencies, embeddable SVGs, and pre-formatted printable layout).

---

### 2.5 Inbound WhatsApp Webhook (Patient Firewall)

#### `POST /webhooks/whatsapp/inbound`
**Description:** Webhook triggered when a patient sends a message or question to the WhatsApp Business Number. Acts as a safety firewall.

* **Request Body (Meta Webhook Payload snippet):**
```json
{
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "919876543210",
                "id": "wamid.HBgMOTE5ODc2NTQzMjEwFQIAEhgWM0VCMDFEMjEwRTQzNTUyRTI4MEU2MwA=",
                "timestamp": "1731486700",
                "text": {
                  "body": "Kya mai BP ki goli band kar sakta hu?"
                },
                "type": "text"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

* **Automated Firewall Response (Deterministic Outbound Dispatch):**
```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "919876543210",
  "type": "text",
  "text": {
    "body": "नमस्ते रमेश जी, यह क्लीनिक की स्वचालित सूचना सेवा है। सुरक्षा कारणों से यह नंबर चिकित्सा सलाह या सवालों के जवाब नहीं दे सकता। किसी भी बदलाव के लिए सीधे अपने डॉक्टर से संपर्क करें: 011-23456789।"
  }
}
```
