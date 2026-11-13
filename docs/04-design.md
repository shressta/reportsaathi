# Design Specification & UI Architecture: ReportSaathi

Based on [docs/01-problem.md](01-problem.md), [docs/02-research.md](02-research.md), and [docs/03-scope.md](03-scope.md).

---

## 1. Core Flow Screen Inventory & State Matrix

The core flow (**"The Clinician-Verified Intake & Audio Handoff"**) consists of 5 dedicated screens/touchpoints:
* **Screen 1:** Prescription Quick-Entry Screen *(Clinic Assistant / Compounder)*
* **Screen 2:** Clinician Verification & 1-Click Sign-off Screen *(Doctor / Pharmacist)*
* **Screen 3:** Dispatch & Handoff Confirmation Screen *(Clinic Output Console)*
* **Screen 4:** Physical Visual Intake Slip *(Printed Handheld Artifact for Patient)*
* **Screen 5:** WhatsApp Audio & Visual Intake Card *(Patient Mobile Touchpoint)*

---

### Screen 1: Prescription Quick-Entry Screen
**Role:** Point-of-care data ingestion interface designed for a busy clinic assistant or pharmacist counter to input prescribed medications and patient mobile number in under 30 seconds.

```
┌────────────────────────────────────────────────────────┐
│ [ReportSaathi] नया मरीज (New Patient)          क्लीनिक ID: 402│
├────────────────────────────────────────────────────────┤
│ मरीज का मोबाइल नंबर (WhatsApp Number)                 │
│ [+91] [ 98765 43210                     ] [✓ वैध]     │
│ [x] मरीज ने WhatsApp पर ऑडियो प्राप्त करने की सहमति दी │
├────────────────────────────────────────────────────────┤
│ दवा जोड़ें (Add Medicine)                             │
│ [ Telma 40 (Telmisartan 40mg)                     ▼ ]  │
│ समय: (•) 1-0-0 [सुबह]  ( ) 0-0-1 [रात]  ( ) 1-0-1      │
│ भोजन: (•) नाश्ते के बाद  ( ) खाली पेट  ( ) खाने से पहले │
│ [+ दवा सूची में जोड़ें]                                │
├────────────────────────────────────────────────────────┤
│ चुनी गई दवाइयां (2):                                   │
│ 1. Telma 40mg  | ☀️ सुबह (नाश्ते बाद) 1 गोली   [संपादित]│
│ 2. Glycomet 500| 🌙 रात (खाने बाद) 1 गोली     [हटाएं]  │
├────────────────────────────────────────────────────────┤
│ [  सत्यापन के लिए डॉक्टर को भेजें (Send to Doctor)  →  ]│
└────────────────────────────────────────────────────────┘
```

* **Default State:**
  * Clean form with focused 10-digit mobile number input.
  * Search-as-you-type drug field with dropdown showing top 300 Indian formulations.
  * Pre-selected sensible defaults: Frequency `1-0-0` (सुबह) and Meal relation `नाश्ते के बाद` (After breakfast).
  * Verbal consent checkbox pre-ticked as standard operating procedure.
  * List of added medicines displays below in high-contrast summary chips with edit/remove buttons.
* **Empty State:**
  * Clean slate.
  * Medicine list shows an illustration-free, clear prompt: *"कोई दवा नहीं जोड़ी गई है। ऊपर से दवा खोजकर '+ दवा सूची में जोड़ें' पर टैप करें।"* (No medicines added yet. Search above to add.)
  * Primary submit button (*सत्यापन के लिए डॉक्टर को भेजें*) is visibly disabled (`opacity: 0.4`, `cursor: not-allowed`).
* **Loading State:**
  * While typing in the medicine search bar, a discreet inline spinner appears inside the input box (*"दवाइयां खोजी जा रही हैं..."*).
  * Local fuzzy search responds under 50ms from offline cached pharmacopeia.
  * When submitting to Doctor, the primary button displays a spinning indicator and text: *"डॉक्टर की स्क्रीन पर भेजा जा रहा है..."* (Submitting to doctor's screen).
* **Error State:**
  * *Invalid Mobile:* If phone number is <10 digits or contains non-numeric characters, input border turns deep red (`#DC2626`, 2px stroke), with clear Hindi error below: *"कृपया 10 अंकों का सही मोबाइल नंबर दर्ज करें।"*
  * *Unlisted Medicine:* If staff types a drug not in the top 300 list, an inline prompt offers: *"सूची में नहीं मिला। क्या आप इसे मैन्युअली जोड़ना चाहते हैं?"* (Add custom generic).
  * *Zero Medicines on Submit:* Shakes the medicine search box with an amber banner: *"आगे बढ़ने के लिए कम से कम एक दवा जोड़ना अनिवार्य है।"*

---

### Screen 2: Clinician Verification & 1-Click Sign-off Screen
**Role:** Doctor's or Head Pharmacist's high-speed verification screen (<15 seconds review time) ensuring full clinical accountability under NMC Telemedicine Practice Guidelines 2020.

```
┌────────────────────────────────────────────────────────┐
│ डॉक्टर सत्यापन (Doctor Verification)     मरीज: 98765 43210 │
├───────────────────────────┬────────────────────────────┤
│ मूल पर्ची इनपुट           │ मरीज को जाने वाला ड्राफ्ट   │
│ (Clinic Input)            │ (Patient Hindi Draft)      │
│                           │                            │
│ • Telma 40mg (OD - PC)    │ ☀️ सुबह नाश्ते के बाद      │
│   1-0-0                   │   टेल्मा 40 (बीपी की दवा)  │
│                           │   👉 1 गोली                │
│ • Glycomet 500mg (OD - PC)│                            │
│   0-0-1                   │ 🌙 रात खाने के बाद         │
│                           │   ग्लाइकोमेट (शुगर की दवा) │
│                           │   👉 1 गोली                │
├───────────────────────────┴────────────────────────────┤
│ 🔊 ऑडियो सारांश पूर्वावलोकन (Audio Script):             │
│ "चाचाजी, सुबह नाश्ते के बाद बीपी की 1 गोली टेल्मा 40...│
├────────────────────────────────────────────────────────┤
│ [ ← सुधार करें (Edit) ]   [ ✓ अनुमोदित करें और भेजें ]   │
└────────────────────────────────────────────────────────┘
```

* **Default State:**
  * 2-column comparison layout (or vertical split on tablet/mobile).
  * Left: Raw clinical input (`Telma 40mg - OD - PC`).
  * Right: Generated Hindi visual card and lay-language purpose (*"बीपी की दवा"*).
  * Audio script preview expandable at the bottom.
  * Prominent, high-contrast green primary button: *"✓ अनुमोदित करें और भेजें (Approve & Send)"*.
* **Empty State:**
  * Displays when no patients are in the review queue: *"सत्यापन के लिए कोई पर्ची लंबित नहीं है।"* (Queue clear). Shows a friendly green check badge: *"सभी मरीज निपटाए जा चुके हैं।"*
* **Loading State:**
  * Rule engine takes <200ms to map clinical codes to Hindi visual slots.
  * If regenerating audio preview: A pulsing waveform bar appears with text: *"ऑडियो सारांश तैयार किया जा रहा है..."*
  * During 1-click approval: Primary button locks, turns teal with a spinner: *"पर्ची लॉक की जा रही है और प्रिंटर पर भेजी जा रही है..."* (Cryptographically signing audit log).
* **Error State:**
  * *Dosing Conflict Flag:* If a dangerous combination or duplicate dosing is detected (e.g. two ACE/ARBs entered), an amber warning banner highlights the card: *"⚠️ ध्यान दें: एक जैसी दो दवाइयां दर्ज हैं। कृपया खुराक जांच लें।"*
  * *Transmission Timeout:* If server fails to record sign-off: Red modal: *"इंटरनेट कनेक्शन धीमा है। पर्ची स्थानीय रूप से सुरक्षित है। 'पुनः प्रयास करें' पर टैप करें।"* (Retry button).

---

### Screen 3: Dispatch & Handoff Confirmation Screen
**Role:** Desk output status console confirming physical print generation and WhatsApp API message transmission.

```
┌────────────────────────────────────────────────────────┐
│ पर्ची सफलतापूर्वक तैयार हुई (Handoff Success)          │
├────────────────────────────────────────────────────────┤
│ [✓] डॉक्टर द्वारा सत्यापित (Dr. Verma, Reg: RMP-88419)  │
│                                                        │
│ 🖨️ प्रिंटर स्थिति: [ A5 पर्ची प्रिंट हो गई ]            │
│ 📲 WhatsApp डिलीवरी: [ भेजा गया (Sent ✓✓) ]           │
│    मरीज का नंबर: +91 98765 43210                       │
├────────────────────────────────────────────────────────┤
│ क्या मरीज को पर्ची हाथ में दे दी गई है?                │
│ [ 🖨️ दोबारा प्रिंट करें ]    [ + अगले मरीज की पर्ची दर्ज करें ]│
└────────────────────────────────────────────────────────┘
```

* **Default State:**
  * Green success badge with registered doctor's name and registration number.
  * Dual delivery status indicators:
    * `🖨️ प्रिंटर: प्रिंट सफल (A5 Slip Printed)`
    * `📲 WhatsApp: संदेश पहुंच गया (Delivered ✓✓)`
  * Large primary action: *"+ अगले मरीज की पर्ची दर्ज करें (Next Patient)"* (resets form to Screen 1).
  * Secondary button: *"🖨️ दोबारा प्रिंट करें (Reprint Slip)"*.
* **Empty State:**
  * Not applicable (Screen only renders upon completed verification of Screen 2).
* **Loading State:**
  * While WhatsApp webhook acknowledges receipt: Amber pulsing badge: *"WhatsApp पर भेजा जा रहा है..."*
  * While sending raw postscript to desk printer: *"प्रिंटर से संपर्क किया जा रहा है..."*
* **Error State:**
  * *Printer Jam / Offline:* Red status icon next to printer: *"प्रिंटर ऑफलाइन है या कागज खत्म है। पर्ची स्क्रीन पर देखें या 'प्रिंटर पुनः जांचें' पर टैप करें।"*
  * *WhatsApp Number Unregistered:* Amber warning: *"इस नंबर पर WhatsApp सक्रिय नहीं है। मरीज को केवल प्रिंटेड पर्ची सौंपें और ऑडियो सुनाएं।"* (Fallback guidance).

---

### Screen 4: Physical Visual Intake Slip (Printed Patient Artifact)
**Role:** High-contrast A5 sheet or thermal receipt handed directly to the patient to pin on their wall or place in their medicine box.

```
┌────────────────────────────────────────────────────────┐
│ 🏥 डॉ. वर्मा क्लीनिक • स्वास्थ्य साथी पर्ची              │
│ मरीज: रमेश कुमार (50 वर्ष)     दिनांक: 13-Nov-2026      │
├────────────────────────────────────────────────────────┤
│ समय व खुराक         दवा का नाम और विवरण       कितनी गोली │
├────────────────────────────────────────────────────────┤
│ ☀️ सुबह             टेल्मा 40 (Telma 40)        ┌─────┐│
│    (नाश्ते के बाद)   बीपी सामान्य रखने के लिए    │  1  ││
│    🍽️               नीले रंग का रैपर           │गोली ││
│                                                └─────┘│
├────────────────────────────────────────────────────────┤
│ 🌙 रात              ग्लाइकोमेट 500 (Glycomet)   ┌─────┐│
│    (खाने के बाद)    शुगर नियंत्रण के लिए        │  1  ││
│    🍽️               सफेद रंग की गोली           │गोली ││
│                                                └─────┘│
├────────────────────────────────────────────────────────┤
│ ⚠️ जरूरी सलाह: डॉक्टर से पूछे बिना कोई दवा बंद न करें।   │
│ आपातकालीन फोन: 011-23456789 • क्लीनिक समय: 9 AM - 6 PM│
└────────────────────────────────────────────────────────┘
```

* **Default State:**
  * High-contrast black-on-white layout designed for cheap thermal rolls or basic mono laser A5 prints.
  * Giant visual icons: ☀️ (Morning Sun), 🌤️ (Midday), 🌙 (Night Moon), 🍽️ (Meal plate).
  * Bold numerical quantities inside stark boxes (`1 गोली`).
  * Hindi lay-purpose stated clearly beside the English brand name.
  * Clinic emergency contact at the base.
* **Empty State:**
  * Never printed empty (blocked upstream by Screen 1 validation).
* **Loading State:**
  * Client-side print dialog preview.
* **Error State:**
  * Faded toner / paper truncation avoided by strict 1-page fixed dimension geometry (no page 2 overflow possible).

---

### Screen 5: WhatsApp Audio & Visual Intake Card (Patient Touchpoint)
**Role:** The end-user interface for the 50-year-old solo patient on their low-cost Android phone. Uses native WhatsApp chat bubbles for zero app installation and zero learning curve.

```
┌────────────────────────────────────────────────────────┐
│ 👨‍⚕️ डॉ. वर्मा क्लीनिक (ReportSaathi)          ⋮  📞 │
├────────────────────────────────────────────────────────┤
│ [11:45 AM]                                             │
│ ┌────────────────────────────────────────────────────┐ │
│ │ नमस्ते रमेश जी, डॉ. वर्मा क्लीनिक से आपकी दवाएं:   │ │
│ │                                                    │ │
│ │ ┌────────────────────────────────────────────────┐ │ │
│ │ │  ▶  ılıııııııııııııııııııııı  0:42             │ │ │
│ │ │  🔊 अपनी भाषा में सुनें (Tap to Listen)        │ │ │
│ │ └────────────────────────────────────────────────┘ │ │
│ │                                                    │ │
│ │ ☀️ सुबह (नाश्ते बाद): टेल्मा 40 - 1 गोली          │ │
│ │ 🌙 रात (खाने बाद): ग्लाइकोमेट 500 - 1 गोली         │ │
│ │                                                    │ │
│ │ [ 🖼️ दवा समय-पत्रक फोटो देखें (View Chart) ]       │ │
│ │                                          11:45 ✓✓  │ │
│ └────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

* **Default State:**
  * Delivered inside the familiar WhatsApp conversation window.
  * Prominent native audio player card with green circular Play button (`▶`).
  * Duration clearly marked: `0:42 • अपनी भाषा में सुनें`.
  * Concise Hindi summary below audio bubble for literate family members.
  * Attached high-resolution image of the Visual Intake Chart (Screen 4).
* **Empty State:**
  * First-time welcome greeting with clinic verification badge.
* **Loading State:**
  * Standard WhatsApp media download progress circle. Audio file size is compressed to <180KB (OGG Opus) ensuring download in <2 seconds on 2G/3G networks.
* **Error State:**
  * *Audio Download Failure:* Native WhatsApp retry arrow (`↓`).
  * *Inadvertent Patient Query:* If patient replies with medical questions (e.g., *"क्या मैं दवा बंद कर दूं?"*), automated non-diagnostic auto-reply fires: *"नमस्ते, यह एक स्वचालित सूचना सेवा है। किसी भी चिकित्सीय सलाह या बदलाव के लिए सीधे अपने डॉक्टर से संपर्क करें: 011-23456789।"* (Strict "Never" safety guardrail).

---

## 2. Review of Reference UIs & Comparative Analysis

Screenshots of the 5 reference interfaces are archived in [docs/references/](file:///c:/Users/ADMIN/reportsaathi/docs/references/).

```
docs/references/
├── ref-01-diagnostic-lab-table.png      (Diagnostic Lab App Table)
├── ref-02-online-pharmacy-app.png       (Online Pharmacy Checkout)
├── ref-03-whatsapp-vernacular-voice.png (WhatsApp Hindi Voice Interface)
├── ref-04-cowin-abha-vernacular-ui.png  (Govt ABHA/CoWIN Vernacular UI)
└── ref-05-visual-schedule-intake-card.png (Visual Icon Intake Chart)
```

### Reference 1: Diagnostic Lab Apps (Tata 1mg / Dr. Lal PathLabs)
*Screenshot: `docs/references/ref-01-diagnostic-lab-table.png`*

* **What to Borrow:**
  * Clean two-tone card containers with clear section borders.
  * Clear numerical representation of values with standard metric units.
* **What to Avoid:**
  * **Catastrophizing "Red Alert" Badges:** Alarming red labels like *"HIGH ALERT"* or *"POOR CONTROL"* on borderline values trigger acute cyberchondria in older patients living alone.
  * **Commercial Upselling & Spam:** Banners pitching ₹999 cardiac packages or tele-consultation add-ons create deep distrust.
  * **Dense English Tables:** 8pt technical terminology (*"Hexokinase method"*, *"CHOD-PAP"*) that alienates non-English speakers.

---

### Reference 2: Online Pharmacy Apps (PharmEasy / Apollo 24|7)
*Screenshot: `docs/references/ref-02-online-pharmacy-app.png`*

* **What to Borrow:**
  * **Dosage Chips:** Discrete rounded chips showing timing and food relationship (`1 Tablet Daily (OD)`, `After Breakfast`).
  * Medication naming convention that clearly separates Brand Name (`Telma 40`) from Active Salt (`Telmisartan 40mg`).
* **What to Avoid:**
  * **Aggressive Generic Substitution Prompts:** Popups encouraging patients to swap prescribed drugs for private-label generics confuse older patients and violate doctor trust.
  * **E-Commerce Friction:** Shopping carts, crossed-out MRP discounts, wallet cashbacks, and delivery countdown timers that detract from clinical safety.

---

### Reference 3: WhatsApp Audio Messaging (Elderly Household Benchmark)
*Screenshot: `docs/references/ref-03-whatsapp-vernacular-voice.png`*

* **What to Borrow:**
  * **The Giant Play Button & Audio Waveform:** Zero learning curve. In India, 95%+ of smartphone users aged 50+ instinctively know how to tap the green WhatsApp play button.
  * **Zero App Download Friction:** Delivering advice inside an app the patient already opens 10 times a day eliminates app store drops and login failures.
  * **Official Verified Business Header:** Clinic name, doctor photo, and green verified badge provide immediate reassurance.
* **What to Avoid:**
  * **Unstructured Text Clutter:** Long, unformatted text messages that get buried under family forwards.
  * **Two-Way Conversational Uncertainty:** Open chat boxes where patients ask diagnostic questions that an AI cannot legally answer.

---

### Reference 4: Government Public Health Vernacular UI (CoWIN / ABHA)
*Screenshot: `docs/references/ref-04-cowin-abha-vernacular-ui.png`*

* **What to Borrow:**
  * **Large, High-Contrast Form Inputs:** 52px+ height input fields with bold 18px text and high-contrast borders that are easy to target with older or unsteady fingers.
  * **Bilingual Microcopy:** Pairing English terms with Devanagari (*"मोबाइल नंबर (Mobile Number)"*, *"सत्यापित (Verified)"*) to avoid confusion across compounders and patients.
  * **Prominent Verification Badges:** Clear green checkmarks confirming doctor authorization.
* **What to Avoid:**
  * **Rigid Bureaucratic Stiff Hindi:** Overly complex administrative vocabulary (*"प्रमाणीकरण"*, *"पंजीकरण सं."*) that intimidates semi-literate users.
  * **Session Timeout Traps:** Government portals frequently log users out after 2 minutes, wiping filled forms.

---

### Reference 5: High-Contrast Visual Intake Sticker / Chart (Elderly Benchmark)
*Screenshot: `docs/references/ref-05-visual-schedule-intake-card.png`*

* **What to Borrow:**
  * **Universal Time-of-Day Icons:** Bright Sun ☀️ for morning, Midday Sun 🌤️ for afternoon, Moon 🌙 for night. Completely bypasses language literacy.
  * **Bold Quantity Callout:** Giant numerical quantity inside a dedicated badge (`1 गोली`), impossible to misread.
  * **Meal Plate Relationship Icon:** 🍽️ with clear Hindi relation (*"नाश्ते के बाद"* vs *"खाली पेट"*).
* **What to Avoid:**
  * **Cursive Handwriting:** Never allow handwritten annotations; everything must be machine-rendered in clean, bold Devanagari typography.
  * **Delicate Thin Borders:** Thin 0.5px hairline dividers get washed out on cheap thermal printers; use solid 1.5px to 2px strokes.

---

## 3. Design Direction for Low-Cost Android & Older Vernacular Users

### 3.1 Layout Architecture
* **Single-Column Vertical Stacking:** Low-cost Android devices (Redmi A series, Realme C series, Galaxy M04) have screen widths between **360px and 390px**. Multi-column layouts cause awkward word-wrapping and horizontal scrolling. Every critical element stacks vertically.
* **Strict Visual Anchoring (Top-to-Bottom):**
  1. Header: Clinic name + Verified Doctor badge.
  2. Hero Action: Audio Playback Card (WhatsApp) or Time Slot Card (Print/Web).
  3. Body: Drug items grouped by Time of Day (☀️ Morning first, 🌙 Night last).
  4. Footer: Emergency contact and standard safety disclaimer.
* **Progressive Disclosure:** Advanced details (manufacturer, chemical formulation, batch) are tucked behind a secondary "विवरण देखें (Details)" tap; primary view shows only **Name, Purpose, Timing, and Dose**.

---

### 3.2 Typography & Devanagari Optimization
* **Font Family:** System-native `Noto Sans Devanagari` paired with `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto` for Latin numerals and brand names.
* **The "Matra" Line-Height Rule:**
  * *Critical Rule:* Latin typography defaults to `line-height: 1.2` to `1.3`. In Devanagari, upper matras (e.g. `े`, `ै`, `ी`, `ं`) and lower matras (e.g. `ु`, `ू`, `ृ`) get clipped by standard line-heights!
  * **All Devanagari text must use a minimum `line-height: 1.55` to `1.65`** to prevent diacritic clipping.
* **Type Scale Hierarchy (Optimized for Presbyopia):**
  * **Hero Number (Dose Quantity):** `32px` / Bold `700` (e.g., **1**, **½**).
  * **Screen Titles / Time Slot Names:** `22px`–`24px` / Bold `700` (*"सुबह"*, *"रात"*).
  * **Medicine Names:** `18px`–`20px` / SemiBold `600` (*"टेल्मा 40"*).
  * **Lay Purpose & Regimen Instructions:** `16px` / Regular `400`–`500` (*"नाश्ते के बाद, बीपी के लिए"*).
  * **Disclaimers & Metadata:** `13px`–`14px` / Regular `400` (never drop below 13px anywhere).
* **Zero Faux-Bold:** Devanagari conjunct characters (युक्ताक्षर, such as `क्त`, `स्ट`, `ण्ड`) turn into illegible ink-blobs when software applies artificial bolding. Use true font weights (`font-weight: 600` or `700`).

---

### 3.3 Colour Palette & Contrast (WCAG AAA)
Low-cost Android screens use budget TN/IPS LCD panels with poor peak brightness (250–350 nits) and narrow viewing angles. When used in harsh Indian outdoor sunlight, subtle grays completely disappear.

| Role | Colour Name | Hex Code | Contrast on White | Usage |
| :--- | :--- | :--- | :---: | :--- |
| **Surface** | Stark White | `#FFFFFF` | N/A | Clean background for maximum LCD luminance. |
| **Primary Text** | Midnight Slate | `#0F172A` | **15.8 : 1** (AAA) | All headings, medicine names, and quantities. |
| **Secondary Text**| Deep Charcoal | `#334155` | **9.6 : 1** (AAA) | Instructions, meal timing, and clinic address. |
| **Morning Brand** | Solar Amber | `#D97706` | **4.8 : 1** (AA UI) | Morning slot icon ☀️, border accent, and tags. |
| **Night Brand** | Midnight Indigo | `#1E40AF` | **8.5 : 1** (AAA) | Night slot icon 🌙 and evening medicine cards. |
| **Safety / Success**| Clinical Green | `#16A34A` | **5.2 : 1** (AA UI) | Verified checkmarks, audio play button (`#00A884`). |
| **Critical Warning**| Crimson Red | `#DC2626` | **5.9 : 1** (AA UI) | Emergency contact, allergy alerts, error states. |

* **Prohibited:** Never use light gray text (`#94A3B8` or `#CBD5E1`) for any words or labels. Placeholders must use `#64748B` or higher.

---

### 3.4 Spacing & Touch Geometry (Motor-Friendly)
Older adults experience age-related tremors, joint stiffness, and reduced fine motor control:
* **Minimum Touch Target:** `56px` height for all primary action buttons (exceeds Android Material 48dp minimum).
* **Touch Target Separation:** Minimum `12px` to `16px` margin between adjacent interactive elements to eliminate mis-taps.
* **Full-Width Action Buttons:** Main call-to-action buttons span 100% of the screen width with rounded `8px` corners.
* **No Swipe Gestures:** Zero swipe-to-delete, pull-to-refresh, or horizontal carousels. All interactions are explicit single-tap actions.

---

### 3.5 Tone of Voice & Vernacular Register
* **Colloquial Hindustani (Not Sanskritized Hindi):**
  * *Say:* *"बीपी (खून का दबाव)"* — *Never:* *"अधिवृक्क रक्तचाप"*
  * *Say:* *"शुगर (मधुमेह)"* — *Never:* *"प्रमेह विकार"*
  * *Say:* *"नाश्ते के बाद 1 गोली लें"* — *Never:* *"प्रातःकाल अल्पाहार उपरांत एक वटिका ग्रहण करें"*
* **Respectful & Reassuring:**
  * Uses culturally respectful elder honorifics (*"नमस्ते रमेश जी"*, *"चाचाजी"*).
  * Direct, active voice: *"यह गोली रोज सुबह लें"* (Take this pill every morning).
* **Strict Non-Diagnostic Guardrail in Tone:**
  * Explains the **purpose of the pill** as instructed by the doctor, never diagnoses the underlying pathology.
  * Always anchors accountability to the treating clinician: *"यह समय-पत्रक आपके डॉक्टर डॉ. वर्मा के निर्देशानुसार तैयार किया गया है।"*
