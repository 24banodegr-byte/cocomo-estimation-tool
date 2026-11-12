PRACTICAL 6 - COCOMO ESTIMATION TOOL
===================================

FILES
- app.py: Streamlit application implementing Basic, Intermediate and Detailed COCOMO 81.
- requirements.txt: Python dependencies.
- Practical_6_Report.docx: ready-to-review practical report.
- outputs/test_case_results.csv: calculated sample outputs.
- screenshots/: sample UI/output preview images for report reference.

HOW TO RUN (Windows / VS Code)
1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Open Terminal and run:
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
4. Browser opens the COCOMO calculator.
5. Enter Project Name, LoC and Mode. Use the tabs to compare all models.
6. In Intermediate and Detailed tabs, choose cost-driver ratings. Nominal is selected by default.
7. For Detailed COCOMO, ensure phase allocations add up to 100%.

MODEL NOTES
- KLOC = LoC / 1000.
- Basic effort = a * (KLOC ** b).
- Intermediate/Detailed effort = a * (KLOC ** b) * EAF.
- EAF = product of 15 COCOMO 81 effort multipliers.
- Development time = 2.5 * (Effort ** d).
- Average team size = Effort / Development Time.
- Productivity = LoC / Effort.
- Detailed phase split in the app is an editable illustrative allocation (default 6/16/24/38/16), not a universal fixed COCOMO coefficient. Use the phase distribution from your class reference if your instructor provided one.

TEST INPUTS
1. Library Management System - 2,000 LoC - Organic.
2. Online Food Ordering System - 30,000 LoC - Semi-detached.
3. Banking System - 100,000 LoC - Embedded.
All sample comparison outputs use EAF = 1.00 (Nominal cost-driver ratings).

IMPORTANT
Review your college's prescribed COCOMO reference tables before submission. Coefficients and cost-driver multipliers in this tool are the classic COCOMO 81 values. Do not claim that sample screenshots are live browser captures; they are sample output previews.
