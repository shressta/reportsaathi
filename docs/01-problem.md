Problem statement

A Hindi-speaking patient around 50, living alone, leaves the clinic with blood reports, scan reports and a prescription full of terms he can’t read, and nobody to explain them. He is left to guess what the results mean and how to take his medicines, which risks wrong dosing, missed follow-ups, and either needless fear or false reassurance.

Option A: Paper and people (little or no software)

Hindi explainer cards for the 20 to 30 most common tests (CBC, sugar, lipid, thyroid, kidney, liver), plus Hindi medicine-label stickers. The clinic or pharmacy hands them out, and a trained staff member spends two minutes walking the patient through his own report.

Assumptions

The common tests cover most of what patients actually receive.
Clinic or pharmacy staff will do the walkthrough, and someone pays for their time.
The patient can read Hindi (not just speak it).
A generic card is useful without knowing his specific values.

Medical risk: A generic card can falsely reassure (“normal range is X”) when his result is borderline for his age or condition. Staff may overstep into interpretation. Scans can’t be covered this way.

Legal risk: Lowest of the three. Staff must not diagnose or advise on dosage. Content should be reviewed and signed off by a doctor. Printed cards don’t involve patient data.

Option B: Photo-to-Hindi explainer (WhatsApp bot or app)

The patient photographs the report or prescription. OCR plus an LLM produces a plain-language Hindi explanation, with voice output.

Assumptions

He has a smartphone and will use it for this, alone, without help.
OCR works on messy phone photos of Indian lab formats and handwritten prescriptions.
The model never misreads a drug name, dose or value.
He will follow “see your doctor” warnings instead of treating the output as an answer.
Hindi voice output sounds natural and understandable to him.

Medical risk: Highest. Misread handwriting or a hallucinated explanation can lead to a wrong dose or a missed serious result. Scans are especially dangerous, since interpreting them is a specialist task. People also over-trust confident output.

Legal risk: Highest. Software that interprets results may be treated as medical device software under Indian regulation. You’d handle sensitive health data, so the Digital Personal Data Protection Act 2023 applies (consent, storage, breach duties). Liability if someone is harmed is unclear. Get a lawyer before launch.

Option C: Doctor-approved summary at the clinic

AI drafts a Hindi summary and a medicine schedule, and the clinic’s doctor or pharmacist reviews it before the patient leaves. It is printed or sent as a voice note.

Assumptions

A clinic will adopt it, and the doctor can review in under a minute.
Clinics see this as saving time or improving care, not as extra liability.
The patient trusts something that comes from his own doctor.
You can build the workflow without disrupting how the clinic already runs.

Medical risk: Lower than B, because a human checks the output. The main risk is rubber-stamping, where a busy doctor approves without really reading it.

Legal risk: Medium. The clinician stays responsible, so clinics may resist. You still handle patient data (DPDP applies), and you’d need clear terms on who is liable for the draft versus the approval.

What I’d test first

Before building anything, I’d validate the part I couldn’t confirm: talk to 10 to 15 patients like him and ask what they did the last time. If most say “I asked the pharmacist” or “a neighbor read it,” Option A may already be good enough, and you’d be competing with a free, trusted workaround. Option A is also the cheapest way to learn whether the pain is real before you commit to software.

I’d also leave scans out of any first version. They’re the hardest to explain safely and the most likely to cause harm if wrong.

I’m not a lawyer, so treat the legal points as things to verify, not conclusions.