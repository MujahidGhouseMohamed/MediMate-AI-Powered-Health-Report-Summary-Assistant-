from fpdf import FPDF

report_text = """
Patient Medical Report

Patient Information:
Name: John A. Smith
Age: 45 years
Gender: Male
Patient ID: P-2025-0786
Date of Report: 12 August 2025
Referring Physician: Dr. Samantha Lee, MD
Hospital/Clinic: Sunrise Multispeciality Hospital

Chief Complaint:
Persistent chest discomfort and shortness of breath for the last 2 weeks.

History of Present Illness (HPI):
The patient reports a dull, aching pain in the chest area, radiating to the left arm, primarily during exertion. Shortness of breath and fatigue occur during mild physical activity. No recent injuries or respiratory infections.

Past Medical History:
- Hypertension (diagnosed 2018)
- Mild hyperlipidemia (diagnosed 2020)
- No history of diabetes
- No known allergies

Family History:
- Father: Coronary artery disease (diagnosed at 58)
- Mother: Hypertension

Medications:
- Amlodipine 5 mg once daily
- Atorvastatin 20 mg once daily

Physical Examination:
Vitals: BP: 148/92 mmHg, HR: 88 bpm, RR: 18/min, Temp: 98.4 °F
General: Alert, oriented, mildly anxious
Cardiac: Slight systolic murmur
Lungs: Clear bilaterally
Extremities: No edema

Investigations:
- ECG: Mild ST depression in leads II, III, aVF
- Troponin-I: Within normal limits
- Lipid Profile: Elevated LDL (165 mg/dL)
- Echocardiography: LVEF 55% (normal range)
- Chest X-ray: No abnormalities

Assessment:
Possible stable angina with underlying hypertension and hyperlipidemia. No acute myocardial infarction detected.

Plan & Recommendations:
1. Aspirin 75 mg daily
2. Continue Amlodipine and Atorvastatin
3. Low-sodium, low-cholesterol diet
4. Moderate exercise after stress testing
5. Treadmill Stress Test within 1 week
6. Follow-up in 2 weeks or earlier if symptoms worsen

Physician’s Signature: ______________
Date: 12 August 2025
"""

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Patient Medical Report', ln=True, align='C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", size=12)
        self.multi_cell(0, 8, body)

pdf = PDF()
pdf.add_page()
pdf.chapter_body(report_text)
pdf.output("patient_report.pdf")

print("PDF generated as patient_report.pdf")
