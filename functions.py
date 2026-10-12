"""
functions.py
============
Student Performance Intelligence and Academic Analytics
Reusable data-processing, validation, and analytical calculations.

Author: Student (EWB Courses - Python with AI)
Dataset: Synthetic Academic Records
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
import numpy as np
import pandas as pd

REQUIRED_COLUMNS: List[str] = [
    "student_id",
    "student_name",
    "department",
    "semester",
    "python_marks",
    "mathematics_marks",
    "statistics_marks",
    "attendance_percentage",
]

SUBJECT_COLUMNS: Dict[str, str] = {
    "python_marks": "Python",
    "mathematics_marks": "Mathematics",
    "statistics_marks": "Statistics",
}

PASS_MARK: float = 35.0
ATTENDANCE_THRESHOLD: float = 75.0


def resolve_dataset_path(filepath: Union[str, Path, None] = None) -> Path:
    """
    Resolves dataset path relative to the project directory or current working directory.
    """
    if filepath is None:
        return Path(__file__).resolve().parent / "data" / "students.csv"

    path_obj = Path(filepath)
    if path_obj.exists():
        return path_obj.resolve()

    relative_to_module = (Path(__file__).resolve().parent / path_obj).resolve()
    if relative_to_module.exists():
        return relative_to_module

    return path_obj.resolve()


def load_dataset(filepath: Union[str, Path, None] = None) -> pd.DataFrame:
    """
    Loads student dataset CSV using Pandas.
    Resolves relative paths robustly and verifies file existence and content.
    """
    resolved_path = resolve_dataset_path(filepath)

    if not resolved_path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {resolved_path}")

    try:
        df = pd.read_csv(resolved_path)
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty and contains no header or data.")
    except Exception as exc:
        raise ValueError(f"Failed to parse CSV file: {exc}")

    if df.empty:
        raise ValueError("The loaded dataset contains no records.")

    return df


def validate_dataset(df: pd.DataFrame, raise_exception: bool = True) -> Tuple[bool, List[str]]:
    """
    Validates dataset integrity:
    - Required columns
    - No duplicate student IDs
    - No missing or null values
    - Non-empty strings in text fields
    - Positive integer semester values
    - Numeric subject marks in [0, 100]
    - Numeric attendance in [0, 100]
    - Non-empty dataset
    """
    errors: List[str] = []

    if not isinstance(df, pd.DataFrame):
        errors.append(f"Input must be a pandas DataFrame, got {type(df).__name__}.")
        if raise_exception:
            raise TypeError(errors[-1])
        return False, errors

    if df.empty:
        errors.append("Dataset is empty.")
        if raise_exception:
            raise ValueError(errors[-1])
        return False, errors

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")

    if missing_cols:
        if raise_exception:
            raise ValueError("; ".join(errors))
        return False, errors

    # Check null / NaN values
    null_counts = df[REQUIRED_COLUMNS].isna().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if not cols_with_nulls.empty:
        errors.append(f"Columns containing missing/null values: {cols_with_nulls.to_dict()}")

    # Check duplicate student IDs
    if df["student_id"].duplicated().any():
        duplicate_ids = df.loc[df["student_id"].duplicated(), "student_id"].tolist()
        errors.append(f"Duplicate student_id values detected: {duplicate_ids}")

    # Check non-empty strings in text columns
    text_cols = ["student_id", "student_name", "department"]
    for col in text_cols:
        blank_mask = df[col].astype(str).str.strip() == ""
        if blank_mask.any():
            errors.append(f"Column '{col}' contains empty or blank strings at rows: {df.index[blank_mask].tolist()}")

    # Check semester (positive integers)
    try:
        semester_numeric = pd.to_numeric(df["semester"], errors="coerce")
        if semester_numeric.isna().any():
            errors.append("Column 'semester' contains non-numeric values.")
        else:
            is_integer = np.all(np.equal(np.mod(semester_numeric.to_numpy(), 1), 0))
            is_positive = np.all(semester_numeric.to_numpy() > 0)
            if not is_integer or not is_positive:
                errors.append("Column 'semester' must contain positive integers.")
    except Exception as exc:
        errors.append(f"Error checking semester column: {exc}")

    # Check subject marks in [0, 100]
    for col in SUBJECT_COLUMNS.keys():
        marks_num = pd.to_numeric(df[col], errors="coerce")
        if marks_num.isna().any():
            errors.append(f"Column '{col}' contains non-numeric values.")
        else:
            arr = marks_num.to_numpy(dtype=float)
            if np.any(arr < 0.0) or np.any(arr > 100.0):
                errors.append(f"Column '{col}' contains marks outside permitted range [0, 100].")

    # Check attendance percentage in [0, 100]
    att_num = pd.to_numeric(df["attendance_percentage"], errors="coerce")
    if att_num.isna().any():
        errors.append("Column 'attendance_percentage' contains non-numeric values.")
    else:
        att_arr = att_num.to_numpy(dtype=float)
        if np.any(att_arr < 0.0) or np.any(att_arr > 100.0):
            errors.append("Column 'attendance_percentage' values outside permitted range [0, 100].")

    if errors:
        if raise_exception:
            raise ValueError("; ".join(errors))
        return False, errors

    return True, []


def assign_grade(average: float) -> str:
    """
    Assigns an academic letter grade based on the student average marks.

    Grading Scale:
      90 <= average <= 100 : A+
      80 <= average < 90  : A
      70 <= average < 80  : B
      60 <= average < 70  : C
      50 <= average < 60  : D
      35 <= average < 50  : E
      average < 35        : F
    """
    if not isinstance(average, (int, float, np.number)) or np.isnan(average):
        raise TypeError("Average mark must be a valid numeric value.")

    if average < 0.0 or average > 100.0:
        raise ValueError(f"Average mark {average} is outside permitted range [0, 100].")

    if average >= 90.0:
        return "A+"
    elif average >= 80.0:
        return "A"
    elif average >= 70.0:
        return "B"
    elif average >= 60.0:
        return "C"
    elif average >= 50.0:
        return "D"
    elif average >= 35.0:
        return "E"
    else:
        return "F"


def determine_subject_result(mark: float) -> str:
    """
    Determines whether a mark meets the passing threshold (>= 35).
    """
    if not isinstance(mark, (int, float, np.number)) or np.isnan(mark):
        raise TypeError("Subject mark must be a valid numeric value.")

    if mark < 0.0 or mark > 100.0:
        raise ValueError(f"Subject mark {mark} is outside permitted range [0, 100].")

    return "Pass" if mark >= PASS_MARK else "Fail"


def determine_overall_status(python_mark: float, math_mark: float, stats_mark: float) -> str:
    """
    Determines overall academic result.
    A student passes overall only if all three subjects meet the pass mark (>= 35).
    """
    for subject_name, m in [("Python", python_mark), ("Mathematics", math_mark), ("Statistics", stats_mark)]:
        if not isinstance(m, (int, float, np.number)) or np.isnan(m):
            raise TypeError(f"{subject_name} mark must be a valid numeric value.")
        if m < 0.0 or m > 100.0:
            raise ValueError(f"{subject_name} mark {m} is outside permitted range [0, 100].")

    if python_mark >= PASS_MARK and math_mark >= PASS_MARK and stats_mark >= PASS_MARK:
        return "Passed"
    return "Failed"


def calculate_pass_percentage(total_students: int, passed_students: int) -> float:
    """
    Calculates pass percentage safely.
    """
    if not isinstance(total_students, (int, np.integer)) or not isinstance(passed_students, (int, np.integer)):
        raise TypeError("Student counts must be integers.")

    if total_students < 0 or passed_students < 0:
        raise ValueError("Student counts cannot be negative.")

    if passed_students > total_students:
        raise ValueError("Passed students cannot exceed total students.")

    if total_students == 0:
        return 0.0

    return float((passed_students / total_students) * 100.0)


def calculate_student_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates student totals, averages, grades, subject pass/fail,
    overall status, and attendance flags. Returns a new DataFrame.
    """
    validate_dataset(df)
    res = df.copy()

    # Convert subject marks to numeric array for NumPy computations
    sub_keys = list(SUBJECT_COLUMNS.keys())
    marks_matrix = res[sub_keys].to_numpy(dtype=float)

    # Use NumPy for vector calculations
    res["total_marks"] = np.sum(marks_matrix, axis=1)
    res["average_marks"] = np.mean(marks_matrix, axis=1)

    # Subject pass/fail determinations
    res["python_result"] = np.where(res["python_marks"] >= PASS_MARK, "Pass", "Fail")
    res["mathematics_result"] = np.where(res["mathematics_marks"] >= PASS_MARK, "Pass", "Fail")
    res["statistics_result"] = np.where(res["statistics_marks"] >= PASS_MARK, "Pass", "Fail")

    # Overall academic result: Passed if and only if all 3 subjects >= PASS_MARK
    all_passed = (
        (res["python_marks"] >= PASS_MARK)
        & (res["mathematics_marks"] >= PASS_MARK)
        & (res["statistics_marks"] >= PASS_MARK)
    )
    res["academic_result"] = np.where(all_passed, "Passed", "Failed")

    # Grade assignment demonstrating natural loop over calculated averages
    assigned_grades: List[str] = []
    for avg in res["average_marks"]:
        assigned_grades.append(assign_grade(avg))
    res["grade"] = assigned_grades

    # Attendance status: attendance below 75% flagged as 'Low Attendance'
    res["attendance_status"] = np.where(
        res["attendance_percentage"] < ATTENDANCE_THRESHOLD, "Low Attendance", "Normal"
    )

    return res


def calculate_subject_summaries(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates subject statistics using NumPy and Pandas:
    Mean, Highest, Lowest, Median, Std Dev, Number passed, Number failed, Pass percentage.
    Identifies the subject(s) with highest average mark, handling ties.
    """
    if df.empty:
        raise ValueError("Cannot calculate subject summaries for an empty DataFrame.")

    subject_data: Dict[str, Dict[str, Any]] = {}
    highest_avg = -1.0
    top_subjects: List[str] = []

    for col_key, display_name in SUBJECT_COLUMNS.items():
        if col_key not in df.columns:
            raise ValueError(f"Column '{col_key}' not found in DataFrame.")

        marks_array = df[col_key].to_numpy(dtype=float)
        mean_val = float(np.mean(marks_array))
        median_val = float(np.median(marks_array))
        max_val = float(np.max(marks_array))
        min_val = float(np.min(marks_array))
        std_val = float(np.std(marks_array, ddof=0))  # Population std dev of the cohort

        passed_count = int(np.sum(marks_array >= PASS_MARK))
        failed_count = int(np.sum(marks_array < PASS_MARK))
        pass_pct = calculate_pass_percentage(len(marks_array), passed_count)

        subject_data[display_name] = {
            "mean": mean_val,
            "highest": max_val,
            "lowest": min_val,
            "median": median_val,
            "std_dev": std_val,
            "passed": passed_count,
            "failed": failed_count,
            "pass_percentage": pass_pct,
        }

        # Track top subject average (handling ties)
        if mean_val > highest_avg:
            highest_avg = mean_val
            top_subjects = [display_name]
        elif np.isclose(mean_val, highest_avg, atol=1e-5):
            top_subjects.append(display_name)

    return {
        "subjects": subject_data,
        "highest_average_subjects": top_subjects,
        "highest_average_value": highest_avg,
    }


def calculate_class_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates class-level performance metrics:
    - Total students
    - Number passing all 3 subjects
    - Number failing at least 1 subject
    - Class pass percentage
    - Class average (mean of individual student averages)
    - Average attendance
    - Highest, lowest, median, and standard deviation of student averages.
    """
    if df.empty:
        raise ValueError("Cannot calculate class statistics for an empty DataFrame.")

    if "average_marks" not in df.columns or "academic_result" not in df.columns:
        df = calculate_student_results(df)

    averages = df["average_marks"].to_numpy(dtype=float)
    attendance = df["attendance_percentage"].to_numpy(dtype=float)

    total_students = len(df)
    passed_all_count = int(np.sum(df["academic_result"] == "Passed"))
    failed_any_count = total_students - passed_all_count
    class_pass_pct = calculate_pass_percentage(total_students, passed_all_count)

    class_mean_avg = float(np.mean(averages))
    highest_avg = float(np.max(averages))
    lowest_avg = float(np.min(averages))
    median_avg = float(np.median(averages))
    std_avg = float(np.std(averages, ddof=0))
    mean_attendance = float(np.mean(attendance))

    return {
        "total_students": total_students,
        "passed_all_count": passed_all_count,
        "failed_any_count": failed_any_count,
        "class_pass_percentage": class_pass_pct,
        "class_average": class_mean_avg,
        "average_attendance": mean_attendance,
        "highest_average": highest_avg,
        "lowest_average": lowest_avg,
        "median_average": median_avg,
        "std_dev_average": std_avg,
    }


def find_top_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Finds top performers ordered by average marks descending, with student_id ascending
    as tie-breaker. Includes all students tied at the n-th place cutoff.
    """
    if df.empty:
        raise ValueError("Cannot find top performers in an empty DataFrame.")

    if "average_marks" not in df.columns:
        df = calculate_student_results(df)

    sorted_df = df.sort_values(
        by=["average_marks", "student_id"],
        ascending=[False, True]
    ).reset_index(drop=True)

    if len(sorted_df) <= n:
        return sorted_df

    cutoff_avg = sorted_df.iloc[n - 1]["average_marks"]
    # Include all tied at or above cutoff
    top_df = sorted_df[sorted_df["average_marks"] >= cutoff_avg].reset_index(drop=True)
    return top_df


def find_lowest_performers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies the lowest-performing student or students (including ties).
    """
    if df.empty:
        raise ValueError("Cannot find lowest performers in an empty DataFrame.")

    if "average_marks" not in df.columns:
        df = calculate_student_results(df)

    min_avg = df["average_marks"].min()
    lowest_df = df[df["average_marks"] == min_avg].sort_values(by="student_id").reset_index(drop=True)
    return lowest_df


def summarize_attendance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates attendance metrics:
    - Overall average attendance
    - Count and list of students below 75%
    - Count and list of students at or above 75%
    """
    if df.empty:
        raise ValueError("Cannot summarize attendance for an empty DataFrame.")

    att_arr = df["attendance_percentage"].to_numpy(dtype=float)
    avg_att = float(np.mean(att_arr))

    low_att_df = df[df["attendance_percentage"] < ATTENDANCE_THRESHOLD]
    adequate_att_df = df[df["attendance_percentage"] >= ATTENDANCE_THRESHOLD]

    cols = ["student_id", "student_name", "department", "attendance_percentage"]
    available_cols = [c for c in cols if c in df.columns]

    return {
        "average_attendance": avg_att,
        "low_attendance_count": len(low_att_df),
        "adequate_attendance_count": len(adequate_att_df),
        "low_attendance_students": low_att_df[available_cols].to_dict(orient="records"),
        "adequate_attendance_students": adequate_att_df[available_cols].to_dict(orient="records"),
    }


def compare_groups(df: pd.DataFrame, group_col: str = "department") -> pd.DataFrame:
    """
    Compares student performance grouped by department or semester.
    Includes group size, average student performance, passed/failed counts,
    and pass percentage.
    """
    if df.empty:
        raise ValueError("Cannot compare groups for an empty DataFrame.")

    if group_col not in df.columns:
        raise ValueError(f"Group column '{group_col}' not found in DataFrame.")

    if "average_marks" not in df.columns or "academic_result" not in df.columns:
        df = calculate_student_results(df)

    records: List[Dict[str, Any]] = []
    # Demonstrating explicit loop over grouped data
    for group_name, group_df in df.groupby(group_col, sort=True):
        count = len(group_df)
        avg_score = float(np.mean(group_df["average_marks"].to_numpy(dtype=float)))
        passed_count = int(np.sum(group_df["academic_result"] == "Passed"))
        failed_count = count - passed_count
        pass_pct = calculate_pass_percentage(count, passed_count)

        records.append({
            group_col: group_name,
            "student_count": count,
            "average_marks": round(avg_score, 2),
            "passed_count": passed_count,
            "failed_count": failed_count,
            "pass_percentage": round(pass_pct, 2),
        })

    return pd.DataFrame(records)


def generate_analysis_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Synthesizes the complete end-to-end analytical summary for the dashboard.
    """
    processed_df = calculate_student_results(df)
    class_stats = calculate_class_statistics(processed_df)
    subject_stats = calculate_subject_summaries(processed_df)
    attendance_stats = summarize_attendance(processed_df)
    top_students = find_top_performers(processed_df, n=5)
    lowest_students = find_lowest_performers(processed_df)
    dept_comparison = compare_groups(processed_df, group_col="department")
    sem_comparison = compare_groups(processed_df, group_col="semester")

    # Generate objective findings without speculative claims
    findings: List[str] = []
    findings.append(
        f"The class recorded an overall pass rate of {class_stats['class_pass_percentage']:.2f}% "
        f"({class_stats['passed_all_count']} of {class_stats['total_students']} students passing all three subjects)."
    )
    findings.append(
        f"The overall class average across all students is {class_stats['class_average']:.2f} marks, "
        f"with a median average of {class_stats['median_average']:.2f} and standard deviation of {class_stats['std_dev_average']:.2f}."
    )
    
    top_subs = ", ".join(subject_stats["highest_average_subjects"])
    top_sub_val = subject_stats["highest_average_value"]
    findings.append(
        f"Subject performance shows {top_subs} having the highest mean score at {top_sub_val:.2f} marks."
    )

    findings.append(
        f"Attendance analysis identifies {attendance_stats['low_attendance_count']} students "
        f"({(attendance_stats['low_attendance_count'] / class_stats['total_students'] * 100):.1f}%) "
        f"falling below the 75% attendance threshold, while {attendance_stats['adequate_attendance_count']} students maintained adequate attendance."
    )

    # Department findings
    best_dept_row = dept_comparison.sort_values(by="average_marks", ascending=False).iloc[0]
    findings.append(
        f"Across departments, {best_dept_row['department']} achieved the highest group average of "
        f"{best_dept_row['average_marks']:.2f} marks across {best_dept_row['student_count']} students."
    )

    return {
        "processed_df": processed_df,
        "class_stats": class_stats,
        "subject_stats": subject_stats,
        "attendance_stats": attendance_stats,
        "top_students": top_students,
        "lowest_students": lowest_students,
        "dept_comparison": dept_comparison,
        "sem_comparison": sem_comparison,
        "findings": findings,
    }
