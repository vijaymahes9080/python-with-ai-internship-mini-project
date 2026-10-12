"""
main.py
=======
Student Performance Intelligence and Academic Analytics
Terminal Dashboard & Execution Pipeline

EWB Courses | Python with AI | End-to-End Assignment
"""

import sys
from pathlib import Path
import pandas as pd

from functions import (
    calculate_class_statistics,
    calculate_student_results,
    calculate_subject_summaries,
    compare_groups,
    find_lowest_performers,
    find_top_performers,
    generate_analysis_summary,
    load_dataset,
    resolve_dataset_path,
    summarize_attendance,
    validate_dataset,
)

LINE_WIDTH = 84


def print_header(title: str, section_num: int) -> None:
    """Prints a styled terminal section header."""
    print()
    print("=" * LINE_WIDTH)
    print(f"  SECTION {section_num}: {title.upper()}")
    print("=" * LINE_WIDTH)


def print_sub_header(title: str) -> None:
    """Prints a secondary separator."""
    print("-" * LINE_WIDTH)
    print(f"  {title}")
    print("-" * LINE_WIDTH)


def main() -> None:
    """Main execution pipeline for the academic intelligence system."""
    # Ensure wide display for tabular outputs
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 1000)
    pd.set_option("display.colheader_justify", "left")

    dataset_path = resolve_dataset_path()

    print("\n" + "#" * LINE_WIDTH)
    print("   STUDENT PERFORMANCE INTELLIGENCE AND ACADEMIC ANALYTICS")
    print("   EWB Courses | Python with AI — Terminal Dashboard")
    print("#" * LINE_WIDTH)

    # ---------------------------------------------------------
    # SECTION 1: PROJECT OVERVIEW
    # ---------------------------------------------------------
    print_header("Project Overview", 1)
    print(f"Project Title     : Student Performance Intelligence and Academic Analytics")
    print(f"Environment       : Python {sys.version.split()[0]} with NumPy & Pandas")
    print(f"Dataset Location  : {dataset_path}")
    print("Dataset Status    : Synthetic educational benchmark (30 fictional records)")
    print(
        "Disclaimer        : All student names, IDs, and records are fictional and synthetically"
    )
    print(
        "                    generated strictly for educational demonstration."
    )

    # STAGE A: LOAD
    try:
        raw_df = load_dataset(dataset_path)
    except Exception as exc:
        print(f"\n[CRITICAL ERROR] Failed to load dataset: {exc}")
        sys.exit(1)

    # STAGE B: VALIDATE
    try:
        is_valid, validation_errors = validate_dataset(raw_df, raise_exception=True)
        validation_status = "PASSED (Integrity verified across all schema constraints)"
    except ValueError as exc:
        print(f"\n[VALIDATION FAILED] Integrity check stopped: {exc}")
        sys.exit(1)

    # ---------------------------------------------------------
    # SECTION 2: DATASET INSPECTION
    # ---------------------------------------------------------
    print_header("Dataset Inspection", 2)
    print(f"Dimensions        : {raw_df.shape[0]} rows x {raw_df.shape[1]} columns")
    print(f"Columns           : {', '.join(raw_df.columns)}")
    print(f"Validation Status : {validation_status}")
    print("\nColumn Data Types & Missing Values:")
    inspection_summary = pd.DataFrame({
        "Column Name": raw_df.columns,
        "Data Type": [str(t) for t in raw_df.dtypes],
        "Missing Values": raw_df.isna().sum().values,
        "Sample Value": [str(raw_df.iloc[0][c]) for c in raw_df.columns],
    })
    print(inspection_summary.to_string(index=False))

    print("\nFirst 5 Records (Raw Input Preview):")
    print("-" * LINE_WIDTH)
    print(raw_df.head(5).to_string(index=False))

    # STAGE D & E: CALCULATE & ANALYZE
    processed_df = calculate_student_results(raw_df)

    # ---------------------------------------------------------
    # SECTION 3: INDIVIDUAL PERFORMANCE TABLE
    # ---------------------------------------------------------
    print_header("Individual Student Performance Table", 3)
    display_cols = [
        "student_id",
        "student_name",
        "department",
        "total_marks",
        "average_marks",
        "grade",
        "academic_result",
        "attendance_percentage",
        "attendance_status",
    ]

    formatted_display = processed_df[display_cols].copy()
    formatted_display["total_marks"] = formatted_display["total_marks"].map(lambda x: f"{x:.1f}")
    formatted_display["average_marks"] = formatted_display["average_marks"].map(lambda x: f"{x:.2f}")
    formatted_display["attendance_percentage"] = formatted_display["attendance_percentage"].map(lambda x: f"{x:.1f}%")

    # Rename for cleaner table display
    formatted_display.columns = [
        "ID",
        "Student Name",
        "Department",
        "Total",
        "Average",
        "Grade",
        "Result",
        "Attendance",
        "Att. Status",
    ]
    print(formatted_display.to_string(index=False))

    # ---------------------------------------------------------
    # SECTION 4: SUBJECT PERFORMANCE
    # ---------------------------------------------------------
    print_header("Subject Performance Analysis", 4)
    subject_summary = calculate_subject_summaries(processed_df)
    sub_records = []
    for sub_name, stats in subject_summary["subjects"].items():
        sub_records.append({
            "Subject": sub_name,
            "Mean": f"{stats['mean']:.2f}",
            "Median": f"{stats['median']:.2f}",
            "Highest": f"{stats['highest']:.1f}",
            "Lowest": f"{stats['lowest']:.1f}",
            "Std Dev": f"{stats['std_dev']:.2f}",
            "Passed": stats["passed"],
            "Failed": stats["failed"],
            "Pass Rate": f"{stats['pass_percentage']:.2f}%",
        })

    sub_df = pd.DataFrame(sub_records)
    print(sub_df.to_string(index=False))
    print()
    top_subs = ", ".join(subject_summary["highest_average_subjects"])
    print(
        f"Subject with Highest Average : {top_subs} ({subject_summary['highest_average_value']:.2f} marks)"
    )

    # ---------------------------------------------------------
    # SECTION 5: CLASS PERFORMANCE
    # ---------------------------------------------------------
    print_header("Class Performance Metrics", 5)
    class_stats = calculate_class_statistics(processed_df)
    print(f"Total Cohort Size             : {class_stats['total_students']} students")
    print(f"Passed All Subjects           : {class_stats['passed_all_count']} students")
    print(f"Failed at Least One Subject   : {class_stats['failed_any_count']} students")
    print(f"Overall Class Pass Rate       : {class_stats['class_pass_percentage']:.2f}%")
    print(f"Cohort Mean Average Marks     : {class_stats['class_average']:.2f}")
    print(f"Cohort Median Average Marks   : {class_stats['median_average']:.2f}")
    print(f"Highest Individual Average    : {class_stats['highest_average']:.2f}")
    print(f"Lowest Individual Average     : {class_stats['lowest_average']:.2f}")
    print(f"Standard Deviation of Averages: {class_stats['std_dev_average']:.2f}")
    print(f"Cohort Mean Attendance        : {class_stats['average_attendance']:.2f}%")

    # ---------------------------------------------------------
    # SECTION 6: STUDENT RANKING
    # ---------------------------------------------------------
    print_header("Student Rankings & Outstanding Performers", 6)
    top_5_students = find_top_performers(processed_df, n=5)
    print(f"Top Performers (including tied cutoffs at 5th position):")
    print("-" * LINE_WIDTH)
    rank_display = top_5_students[[
        "student_id",
        "student_name",
        "department",
        "average_marks",
        "grade",
        "academic_result",
    ]].copy()
    rank_display["Rank"] = range(1, len(rank_display) + 1)
    rank_display["average_marks"] = rank_display["average_marks"].map(lambda x: f"{x:.2f}")
    rank_display = rank_display[["Rank", "student_id", "student_name", "department", "average_marks", "grade", "academic_result"]]
    rank_display.columns = ["Rank", "ID", "Name", "Department", "Average", "Grade", "Result"]
    print(rank_display.to_string(index=False))

    print("\nLowest-Performing Student(s):")
    print("-" * LINE_WIDTH)
    lowest_students = find_lowest_performers(processed_df)
    lowest_display = lowest_students[[
        "student_id",
        "student_name",
        "department",
        "average_marks",
        "grade",
        "academic_result",
    ]].copy()
    lowest_display["average_marks"] = lowest_display["average_marks"].map(lambda x: f"{x:.2f}")
    lowest_display.columns = ["ID", "Name", "Department", "Average", "Grade", "Result"]
    print(lowest_display.to_string(index=False))

    # ---------------------------------------------------------
    # SECTION 7: ATTENDANCE INTELLIGENCE
    # ---------------------------------------------------------
    print_header("Attendance Intelligence", 7)
    att_summary = summarize_attendance(processed_df)
    total_stu = class_stats["total_students"]
    print(f"Cohort Average Attendance    : {att_summary['average_attendance']:.2f}%")
    print(
        f"Students with Normal (>= 75%): {att_summary['adequate_attendance_count']} "
        f"({(att_summary['adequate_attendance_count'] / total_stu * 100):.1f}%)"
    )
    print(
        f"Students with Low (< 75%)    : {att_summary['low_attendance_count']} "
        f"({(att_summary['low_attendance_count'] / total_stu * 100):.1f}%)"
    )

    print("\nStudents Flagged for Low Attendance (< 75%):")
    if att_summary["low_attendance_students"]:
        low_att_df = pd.DataFrame(att_summary["low_attendance_students"])
        low_att_df["attendance_percentage"] = low_att_df["attendance_percentage"].map(lambda x: f"{x:.1f}%")
        low_att_df.columns = ["ID", "Student Name", "Department", "Attendance"]
        print(low_att_df.to_string(index=False))
    else:
        print("None. All students met or exceeded attendance criteria.")

    # ---------------------------------------------------------
    # SECTION 8: GROUP COMPARISON
    # ---------------------------------------------------------
    print_header("Group Comparisons", 8)
    print("Department-Wise Performance Comparison:")
    dept_df = compare_groups(processed_df, group_col="department")
    dept_df.columns = ["Department", "Count", "Mean Average", "Passed", "Failed", "Pass Rate (%)"]
    print(dept_df.to_string(index=False))

    print("\nSemester-Wise Performance Comparison:")
    sem_df = compare_groups(processed_df, group_col="semester")
    sem_df.columns = ["Semester", "Count", "Mean Average", "Passed", "Failed", "Pass Rate (%)"]
    print(sem_df.to_string(index=False))

    # ---------------------------------------------------------
    # SECTION 9: AUTOMATED FINDINGS
    # ---------------------------------------------------------
    print_header("Analytical Findings", 9)
    summary_data = generate_analysis_summary(raw_df)
    for idx, finding in enumerate(summary_data["findings"], start=1):
        print(f"[{idx}] {finding}")

    print("\n" + "=" * LINE_WIDTH)
    print("   END OF ACADEMIC ANALYTICS DASHBOARD REPORT")
    print("=" * LINE_WIDTH + "\n")


if __name__ == "__main__":
    main()
