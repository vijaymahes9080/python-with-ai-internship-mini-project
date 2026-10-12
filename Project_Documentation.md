# Student Performance Intelligence and Academic Analytics
## EWB Courses | Python with AI | Comprehensive Course Assessment Documentation

---

### 1. Project Title
**Project Title**: Student Performance Intelligence and Academic Analytics  
**Course**: EWB Courses — Python with AI  
**Assignment Type**: Individual End-to-End Course Project  
**Student Name**: `[Student Name Placeholder]`  
**Student Roll / ID**: `[Student Roll Number Placeholder]`  
**Academic Batch / Cohort**: `[Cohort Details Placeholder]`  
**Submission Date**: October 2026  

---

### 2. Objective
In contemporary academic institutions, raw examination marks and attendance logs are often siloed across spreadsheets, making it challenging for educators to identify students requiring academic intervention or attendance support in a timely manner.

The objective of this project is to develop an automated, reproducible, and robust command-line intelligence pipeline in Python that processes raw student academic records. Specifically, the system:
- Ingests and rigorously validates raw student CSV records.
- Calculates individual metrics (totals, averages, letter grades, subject-level pass/fail outcomes, overall academic results, and attendance indicators).
- Computes cohort-wide statistical distributions using NumPy (means, medians, standard deviations, and range extremes).
- Generates ranking tables with consistent tie-breaking policies and cutoff extensions.
- Evaluates attendance compliance against institutional thresholds.
- Conducts cross-departmental and semester-based comparative performance analyses.
- Formulates automated, data-driven analytical findings without subjective speculation.

---

### 3. Technologies Used
The project is built strictly using standard, robust Python libraries without unnecessary framework overhead:

| Technology | Version / Specification | Role in the Application |
|---|---|---|
| **Python** | 3.11+ | Core programming language providing procedural, functional, and object-oriented paradigms. |
| **Pandas** | 2.0+ / 3.0+ | Tabular data manipulation, CSV ingestion, row/column slicing, boolean indexing, grouping, and aligned report formatting. |
| **NumPy** | 1.24+ / 2.0+ | High-performance numerical computations, array aggregations (`mean`, `median`, `std`, `min`, `max`), and vectorized condition evaluation (`np.where`). |
| **CSV Format** | RFC 4180 standard | Portable structured text data storage for raw academic inputs. |
| **unittest** | Python Standard Library | Automated testing framework verifying grade thresholds, edge boundaries, calculations, validation rules, and error conditions. |
| **Pathlib** | Python Standard Library | Cross-platform file path resolution ensuring script execution from any directory. |

---

### 4. Dataset Description
The system operates on a synthetic educational dataset stored at `data/students.csv`.

- **Total Records**: 30 fictional student records.
- **Dataset Nature**: 100% synthetic data generated for educational analytics demonstration; contains no real-world personally identifiable information (PII).

#### Schema Specifications:
| Column Name | Data Type | Permitted Range / Format | Description |
|---|---|---|---|
| `student_id` | String | Format `STUxxx` (Unique, non-empty) | Unique primary identifier for each student. |
| `student_name` | String | Non-empty string | Full name of the student. |
| `department` | String | Categorical string | Department (`Computer Science`, `Data Science`, `Artificial Intelligence`, `Information Technology`). |
| `semester` | Integer | Positive integer (`1`, `2`, `3`, `4`) | Current enrolled semester. |
| `python_marks` | Float / Numeric | `0.0` to `100.0` | Marks obtained in Python Programming. |
| `mathematics_marks` | Float / Numeric | `0.0` to `100.0` | Marks obtained in Applied Mathematics. |
| `statistics_marks` | Float / Numeric | `0.0` to `100.0` | Marks obtained in Probability & Statistics. |
| `attendance_percentage` | Float / Numeric | `0.0` to `100.0` | Overall lecture attendance percentage. |

The dataset incorporates diverse academic performance levels:
- High achievers qualifying for A+ and A grades.
- Mid-range and marginal passing students.
- Students failing 1 subject, 2 subjects, and all 3 subjects.
- Attendance compliance both above (>= 75%) and below (< 75%) institutional thresholds.
- Intentional score ties at critical ranking cutoff thresholds to test tie-breaking logic.

---

### 5. Implementation
The application adheres to a modular, sequential processing pipeline:
$$\text{Load} \longrightarrow \text{Validate} \longrightarrow \text{Inspect} \longrightarrow \text{Calculate} \longrightarrow \text{Analyze} \longrightarrow \text{Summarize} \longrightarrow \text{Report}$$

#### Pipeline Stages:
1. **Stage A: Load (`functions.load_dataset`)**
   - Resolves file paths dynamically using `pathlib.Path` relative to the project root, enabling execution regardless of the working directory.
   - Reads CSV data into a Pandas DataFrame, catching `FileNotFoundError`, empty files, or parse errors.

2. **Stage B: Validate (`functions.validate_dataset`)**
   - Enforces data integrity checks:
     - Detection of missing mandatory columns.
     - Uniqueness check on `student_id`.
     - Rejection of null, NaN, or whitespace-only fields.
     - Positive integer check on `semester`.
     - Range validation `[0.0, 100.0]` on all subject marks and attendance percentages.
   - Raises informative, actionable `ValueError` exceptions upon detecting invalid records.

3. **Stage C: Inspect (`main.py` Section 2)**
   - Previews DataFrame structure: shape dimensions, column data types, missing value tallies, and the first 5 records.

4. **Stage D: Calculate (`functions.calculate_student_results`)**
   - Computes total marks ($\sum \text{marks}$) and student average marks ($\frac{1}{3} \sum \text{marks}$) using NumPy matrix vectorization.
   - Evaluates subject pass/fail status ($\text{mark} \ge 35.0$).
   - Evaluates overall result: a student is `"Passed"` if and only if all three subjects satisfy the passing mark ($\ge 35.0$).
   - Assigns letter grades using clean conditional statements:
     - $90 \le \text{avg} \le 100 \implies \text{A+}$
     - $80 \le \text{avg} < 90 \implies \text{A}$
     - $70 \le \text{avg} < 80 \implies \text{B}$
     - $60 \le \text{avg} < 70 \implies \text{C}$
     - $50 \le \text{avg} < 60 \implies \text{D}$
     - $35 \le \text{avg} < 50 \implies \text{E}$
     - $\text{avg} < 35 \implies \text{F}$
   - Flags attendance compliance: $\text{attendance} < 75.0\% \implies \text{"Low Attendance"}$, otherwise $\text{"Normal"}$.

5. **Stage E: Analyze (`functions.calculate_subject_summaries`, `compare_groups`)**
   - Applies NumPy mathematical functions (`np.mean`, `np.median`, `np.std(ddof=0)`, `np.max`, `np.min`).
   - Groups records by `department` and `semester` using Pandas `.groupby()`, computing cohort counts, group means, and pass percentages.

6. **Stage F: Summarize & Rank (`functions.find_top_performers`, `find_lowest_performers`)**
   - Ranks students descending by average mark, resolving ties using `student_id` ascending.
   - Extends the top-5 ranking table dynamically to include all students tied at the 5th place cutoff score.

7. **Stage G: Report (`main.py`)**
   - Formats and displays 9 clear, tabular terminal sections with full numerical precision preserved during calculations and formatted to standard decimal places for output.

---

### 6. Key Features
- **Zero-Data Loss Architecture**: Input DataFrames are never mutated in-place; analytical transformations return fresh copies.
- **Strict Boundary Handling**: Exact grade boundary and passing mark tests (e.g., 35.0 vs 34.99).
- **Tie-Aware Ranking**: Prevents arbitrary exclusion of students tied at ranking cutoffs.
- **Attendance Decoupling**: Academic pass/fail determination remains independent of attendance flags while clearly highlighting attendance risks.
- **Objective Narrative Generation**: Automatically constructs statistical summaries without unsupported speculative claims.
- **Automated Verification**: Complete 20-test `unittest` suite covering calculation fidelity and error paths.

---

### 7. Output / Screenshots
The application produces a structured, 9-section terminal report upon running `python main.py`.

#### Genuine Terminal Output Excerpts:
```text
====================================================================================
  SECTION 4: SUBJECT PERFORMANCE ANALYSIS
====================================================================================
Subject     Mean  Median Highest Lowest Std Dev  Passed  Failed Pass Rate
     Python 62.87 65.00  95.0    22.0   19.25   27      3       90.00%   
Mathematics 62.87 66.50  94.0    18.0   20.53   27      3       90.00%   
 Statistics 64.97 67.00  96.0    29.0   18.02   28      2       93.33%   

Subject with Highest Average : Statistics (64.97 marks)

====================================================================================
  SECTION 5: CLASS PERFORMANCE METRICS
====================================================================================
Total Cohort Size             : 30 students
Passed All Subjects           : 25 students
Failed at Least One Subject   : 5 students
Overall Class Pass Rate       : 83.33%
Cohort Mean Average Marks     : 63.57
Cohort Median Average Marks   : 63.17
Highest Individual Average    : 94.33
Lowest Individual Average     : 23.00
Standard Deviation of Averages: 18.30
Cohort Mean Attendance        : 79.95%

====================================================================================
  SECTION 6: STUDENT RANKINGS & OUTSTANDING PERFORMERS
====================================================================================
Top Performers (including tied cutoffs at 5th position):
------------------------------------------------------------------------------------
 Rank ID     Name         Department              Average Grade Result
1     STU101 Aarav Sharma        Computer Science 94.33   A+    Passed
2     STU102   Diya Patel            Data Science 91.67   A+    Passed
3     STU103  Rohan Verma Artificial Intelligence 87.67    A    Passed
4     STU104  Ananya Iyer        Computer Science 84.00    A    Passed
5     STU105  Kabir Mehta            Data Science 84.00    A    Passed
6     STU130   Ananya Roy  Information Technology 84.00    A    Passed
```

#### How the Student Can Add Screenshots:
1. Run `python main.py` in PowerShell or Windows Terminal.
2. Capture screenshots of sections 1–3, 4–6, and 7–9.
3. Save the images to the `screenshots/` directory (e.g., `screenshots/terminal_dashboard.png`).
4. Run `python -m unittest discover -s tests -v` and save a screenshot of the 20 passing unit tests as `screenshots/unit_tests.png`.
5. Embed the images into this document using standard markdown: `![Dashboard Overview](screenshots/terminal_dashboard.png)`.

---

### 8. Final Outcome
The application successfully delivers an end-to-end analytical solution satisfying all assignment specifications:
- Ingests 30 synthetic student records.
- Accurately determines individual and cohort statistics.
- Validates data integrity and stops gracefully upon encountering corrupted data.
- Passes all 20 automated unit tests (covering grade boundaries, attendance thresholds, subject statistics, rankings, ties, and invalid input rejection).
- Executed and validated in Python 3.11 with Pandas and NumPy.

---

### 9. Challenges & Learning
1. **Pandas 3.0 Strict Dtype Handling**:
   - *Technical Challenge*: In recent versions of Pandas (e.g., Pandas 3.0+), assigning non-numeric values directly to strongly typed float/int columns using `.loc` raises `LossySetitemError` and `TypeError` before user validation logic can process it.
   - *Resolution*: Constructing negative test DataFrames directly from record dictionaries or applying `.astype(object)` ensured that data-type anomalies reach the validator for appropriate handling.
2. **Cutoff Ties in Ranking**:
   - *Technical Challenge*: Standard slicing (`head(5)`) inadvertently excludes students who achieve the exact same average mark as the 5th place student.
   - *Resolution*: Implemented dynamic cutoff threshold logic: after sorting by average descending, the score of the $n$-th student is extracted, and all students with an average $\ge$ the cutoff are included.
3. **Floating-Point Precision and Display Rounding**:
   - *Technical Challenge*: Premature rounding can cause downstream statistical skew in standard deviation or group averages.
   - *Resolution*: Kept full floating-point precision throughout all intermediate calculations and rounded strictly during final terminal presentation.

*Student Self-Reflection Placeholder*:
> `[Student should add personal reflections on concepts learned during the EWB Python with AI course, such as modular function design, NumPy vectorization, or unit testing workflows.]`

---

### 10. GitHub Repository & Submission Checklist
- **Repository Name**: `student-performance-intelligence`
- **GitHub URL**: `https://github.com/[Your-Username]/student-performance-intelligence` *(Replace with your GitHub repository link)*

#### Submission Steps for Student:
1. Initialize or confirm local Git repository:
   ```powershell
   git status
   ```
2. Create a new public repository named `student-performance-intelligence` on GitHub.
3. Add the remote and push code:
   ```powershell
   git remote add origin https://github.com/[Your-Username]/student-performance-intelligence.git
   git branch -M main
   git push -u origin main
   ```
4. Verify all files (`main.py`, `functions.py`, `data/students.csv`, `tests/test_functions.py`, `README.md`, `Project_Documentation.md`) appear on GitHub.
5. Paste the GitHub repository URL into the EWB Course submission form.
