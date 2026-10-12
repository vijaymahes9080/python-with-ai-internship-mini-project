# Student Performance Intelligence and Academic Analytics

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B%20%7C%203.0%2B-150458.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24%2B%20%7C%202.0%2B-013243.svg)](https://numpy.org/)
[![Tests](https://img.shields.io/badge/Tests-20%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()

An end-to-end Python analytics and intelligence system developed for **EWB Courses | Python with AI**. The application automates academic record validation, student grading, statistical cohort analysis, tie-aware ranking, attendance tracking, and cross-departmental benchmarking.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Objective](#objective)
3. [Key Features](#key-features)
4. [Technologies Used](#technologies-used)
5. [Directory Structure](#directory-structure)
6. [Dataset Schema](#dataset-schema)
7. [Grading & Evaluation Rules](#grading--evaluation-rules)
8. [Installation & Setup (Windows)](#installation--setup-windows)
9. [Running the Application](#running-the-application)
10. [Running Automated Tests](#running-automated-tests)
11. [Understanding the Analytical Output](#understanding-the-analytical-output)
12. [Documentation Links](#documentation-links)
13. [Synthetic Data & Privacy Statement](#synthetic-data--privacy-statement)
14. [Known Limitations](#known-limitations)
15. [GitHub Publication Guide](#github-publication-guide)
16. [EWB Final Submission Checklist](#ewb-final-submission-checklist)

---

## Project Overview
The **Student Performance Intelligence and Academic Analytics** system processes raw academic scorecards from CSV files, evaluates individual subject mastery, assigns letter grades, computes class-wide distributions (mean, median, standard deviation, extremes), and outputs an executive-level, structured terminal dashboard.

---

## Objective
To replace fragmented spreadsheet calculations with a reliable, reproducible Python processing pipeline that:
- Ingests and validates student data against strict schema constraints.
- Calculates subject and cohort analytics with high numerical precision.
- Flags attendance concerns without distorting academic merit evaluations.
- Identifies top performers fairly using multi-tier tie-breaking and cutoff extensions.
- Generates data-backed statistical findings for academic coordinators.

---

## Key Features
- **Rigorous Data Validation**: Validates schema presence, uniqueness of IDs, positive integer semesters, non-null values, and marks/attendance ranges `[0, 100]`.
- **Pure Functional Pipeline**: Raw DataFrames are never mutated in-place; all transformations return independent copies.
- **Precision Numerical Operations**: Vectorized calculations powered by NumPy (`np.mean`, `np.median`, `np.std(ddof=0)`).
- **Tie-Aware Top Performer Ranking**: Slices top performers by average marks descending, with student ID ascending tie-breaker, and preserves all students tied at the 5th-place cutoff.
- **Attendance Intelligence**: Highlights students below the 75% attendance threshold independently of academic pass/fail status.
- **Cross-Group Comparisons**: Evaluates performance by academic Department and Semester.
- **Automated Findings Generation**: Produces factual analytical commentary directly derived from processed metrics.

---

## Technologies Used
- **Language**: Python 3.11+
- **Data Manipulation**: Pandas (tabulation, grouping, filtering)
- **Numerical Computing**: NumPy (vector operations, standard deviation, median)
- **Testing**: Python standard library `unittest` (20 automated unit test scenarios)
- **Data Storage**: Comma-Separated Values (CSV)

---

## Directory Structure
```text
student-performance-intelligence/
├── main.py                     # Application entry point and terminal dashboard
├── functions.py                # Reusable analytical, validation, and calculation functions
├── data/
│   └── students.csv            # Synthetic educational dataset (30 records)
├── tests/
│   └── test_functions.py       # 20 automated unit tests using unittest
├── reports/
│   └── README.md               # Guide for optional generated reports and exports
├── screenshots/
│   └── README.md               # Instructions for adding genuine UI screenshots
├── README.md                   # Repository overview and execution guide
├── Project_Documentation.md    # Complete 10-section EWB coursework submission document
├── requirements.txt            # Minimal package dependencies (pandas, numpy)
└── .gitignore                  # Python, environment, and OS ignore rules
```

---

## Dataset Schema
The synthetic dataset is located at `data/students.csv`.

| Field Name | Type | Allowed Range | Description |
|---|---|---|---|
| `student_id` | String | Unique (`STUxxx`) | Unique identifier for each student |
| `student_name` | String | Non-empty | Full name of the student |
| `department` | String | Non-empty | Academic department name |
| `semester` | Integer | Positive integer | Enrolled semester (e.g., 1–4) |
| `python_marks` | Numeric | 0.0 – 100.0 | Python Programming marks |
| `mathematics_marks` | Numeric | 0.0 – 100.0 | Applied Mathematics marks |
| `statistics_marks` | Numeric | 0.0 – 100.0 | Statistics marks |
| `attendance_percentage`| Numeric | 0.0 – 100.0 | Lecture attendance percentage |

---

## Grading & Evaluation Rules

### 1. Subject Pass Mark
A student passes a subject if and only if:
$$\text{Subject Mark} \ge 35.0$$

### 2. Overall Academic Result
A student achieves an overall **"Passed"** status if and only if all three subjects are passed ($\ge 35.0$). If any subject score is $< 35.0$, the student's status is **"Failed"**.

### 3. Letter Grade Scale (Based on 3-Subject Average)
| Student Average Mark | Letter Grade |
|---|---|
| $90.0 \le \text{Average} \le 100.0$ | **A+** |
| $80.0 \le \text{Average} < 90.0$ | **A** |
| $70.0 \le \text{Average} < 80.0$ | **B** |
| $60.0 \le \text{Average} < 70.0$ | **C** |
| $50.0 \le \text{Average} < 60.0$ | **D** |
| $35.0 \le \text{Average} < 50.0$ | **E** |
| $\text{Average} < 35.0$ | **F** |

### 4. Attendance Policy
- **Low Attendance**: Attendance $< 75.0\%$
- **Normal Attendance**: Attendance $\ge 75.0\%$  
*(Note: Attendance is reported independently and does not alter the academic pass/fail outcome).*

---

## Installation & Setup (Windows)

### 1. Clone or Open the Repository
```powershell
cd "d:\current project\python with AI\vj"
```

### 2. Create a Virtual Environment
```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment
```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Running the Application
To run the terminal intelligence dashboard:
```powershell
python main.py
```

The script executes the 7-stage processing pipeline (**Load → Validate → Inspect → Calculate → Analyze → Summarize → Report**) and prints the 9-section dashboard.

---

## Running Automated Tests
Run the complete automated unit test suite with verbose reporting:
```powershell
python -m unittest discover -s tests -v
```

### Verification Checklist Covered by the 20 Tests:
1. Every grade boundary (`A+`, `A`, `B`, `C`, `D`, `E`, `F`)
2. Exact passing mark (`35.0` $\implies$ Pass)
3. Below passing threshold (`34.99`, `0.0` $\implies$ Fail)
4. Total marks and 3-subject average precision
5. Subject-level pass/fail outcomes
6. Overall cohort pass/fail logic
7. Exact 75% attendance threshold (`75.0%` $\implies$ Normal)
8. Below 75% attendance threshold (`74.9%` $\implies$ Low Attendance)
9. Subject averages comparison with NumPy
10. Cohort class average calculation
11. Pass percentage calculation with edge protections
12. Top-five ranking ordering
13. Cutoff tie-handling (preserves all tied students)
14. Rejection of empty datasets
15. Rejection of duplicate student IDs
16. Rejection of missing required columns
17. Rejection of invalid / out-of-range marks
18. Rejection of invalid attendance percentages
19. Rejection of invalid semester values (0, negative, non-integer)
20. Rejection of missing or empty CSV files

---

## Understanding the Analytical Output
The application outputs nine comprehensive sections:
1. **Section 1: Project Overview**: System metadata, environment versions, dataset paths, and synthetic disclaimer.
2. **Section 2: Dataset Inspection**: Row/column counts, schema types, missing-value check, and first 5 records.
3. **Section 3: Individual Performance Table**: Per-student summary containing ID, Name, Department, Total, Average, Grade, Result, and Attendance.
4. **Section 4: Subject Performance**: Subject mean, median, extremes, standard deviation, pass/fail counts, and top-performing subject identification.
5. **Section 5: Class Performance**: Cohort-wide metrics including pass rate, mean average, median, standard deviation, and attendance average.
6. **Section 6: Student Rankings**: Top performers (with cutoff tie extensions) and lowest-performing student(s).
7. **Section 7: Attendance Intelligence**: Cohort attendance distribution and flagged student roster.
8. **Section 8: Group Comparisons**: Department-wise and Semester-wise performance tables.
9. **Section 9: Analytical Findings**: Automated, factual analytical summary points.

---

## Documentation Links
- [EWB Project Full Documentation](file:///d:/current%20project/python%20with%20AI/vj/Project_Documentation.md)
- [Reports Directory Guide](file:///d:/current%20project/python%20with%20AI/vj/reports/README.md)
- [Screenshots Directory Guide](file:///d:/current%20project/python%20with%20AI/vj/screenshots/README.md)

---

## Synthetic Data & Privacy Statement
All student names, identifiers, department assignments, marks, and attendance values contained in `data/students.csv` are **100% fictional and synthetically generated** for educational demonstration in the EWB Courses curriculum. No real student data, institutional records, or personally identifiable information (PII) are used or stored.

---

## Known Limitations
- The system currently processes structured CSV files adhering to the documented schema; semi-structured Excel sheets (.xlsx) require pre-conversion to CSV.
- Statistical measures assume a closed cohort population (`ddof=0` for cohort standard deviation).
- The terminal dashboard requires a terminal window width of at least 85 characters for optimal alignment without line wraps.

---

## GitHub Publication Guide
To publish this repository under the suggested repository name `student-performance-intelligence`:

1. Check local Git status:
   ```powershell
   git status
   ```
2. Stage and commit all files:
   ```powershell
   git add .
   git commit -m "feat: complete student performance intelligence and academic analytics project"
   ```
3. Create a new repository named `student-performance-intelligence` on your GitHub account.
4. Link remote and push:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/student-performance-intelligence.git
   git push -u origin main
   ```

---

## EWB Final Submission Checklist
- [x] Synthetic dataset containing 30 valid student records.
- [x] All 8 required CSV columns present with valid constraints.
- [x] Modular `functions.py` with type hints, docstrings, and input immutability.
- [x] Meaningful integration of Pandas and NumPy.
- [x] Executive terminal dashboard `main.py` presenting all 9 sections.
- [x] Full test suite `tests/test_functions.py` with 20 passing unit tests.
- [x] Comprehensive 10-section `Project_Documentation.md`.
- [x] Production-ready `README.md` with complete Windows PowerShell instructions.
- [x] Clean `.gitignore` and minimal `requirements.txt`.
- [x] Repository staged and prepared for GitHub submission.
