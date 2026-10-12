"""
test_functions.py
=================
Comprehensive unit test suite for Student Performance Intelligence system.
Covers all 20 required verification points using standard library unittest.
"""

import os
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

from functions import (
    assign_grade,
    calculate_class_statistics,
    calculate_pass_percentage,
    calculate_student_results,
    calculate_subject_summaries,
    compare_groups,
    determine_overall_status,
    determine_subject_result,
    find_lowest_performers,
    find_top_performers,
    load_dataset,
    summarize_attendance,
    validate_dataset,
)


class TestStudentAnalytics(unittest.TestCase):
    """Test suite covering grading, calculations, validation, and analytics."""

    def setUp(self):
        """Prepare reusable valid sample data for testing."""
        self.valid_sample_records = [
            {
                "student_id": "T101",
                "student_name": "Alice Smith",
                "department": "Computer Science",
                "semester": 1,
                "python_marks": 90.0,
                "mathematics_marks": 85.0,
                "statistics_marks": 95.0,
                "attendance_percentage": 90.0,
            },
            {
                "student_id": "T102",
                "student_name": "Bob Jones",
                "department": "Data Science",
                "semester": 1,
                "python_marks": 80.0,
                "mathematics_marks": 75.0,
                "statistics_marks": 85.0,
                "attendance_percentage": 75.0,
            },
            {
                "student_id": "T103",
                "student_name": "Charlie Brown",
                "department": "Computer Science",
                "semester": 2,
                "python_marks": 50.0,
                "mathematics_marks": 35.0,
                "statistics_marks": 45.0,
                "attendance_percentage": 74.9,
            },
            {
                "student_id": "T104",
                "student_name": "Daisy Miller",
                "department": "Data Science",
                "semester": 2,
                "python_marks": 60.0,
                "mathematics_marks": 30.0,
                "statistics_marks": 70.0,
                "attendance_percentage": 65.0,
            },
        ]
        self.sample_df = pd.DataFrame(self.valid_sample_records)

    # 1. Every grade boundary
    def test_01_grade_boundaries(self):
        self.assertEqual(assign_grade(100.0), "A+")
        self.assertEqual(assign_grade(90.0), "A+")
        self.assertEqual(assign_grade(89.99), "A")
        self.assertEqual(assign_grade(80.0), "A")
        self.assertEqual(assign_grade(79.99), "B")
        self.assertEqual(assign_grade(70.0), "B")
        self.assertEqual(assign_grade(69.99), "C")
        self.assertEqual(assign_grade(60.0), "C")
        self.assertEqual(assign_grade(59.99), "D")
        self.assertEqual(assign_grade(50.0), "D")
        self.assertEqual(assign_grade(49.99), "E")
        self.assertEqual(assign_grade(35.0), "E")
        self.assertEqual(assign_grade(34.99), "F")
        self.assertEqual(assign_grade(0.0), "F")
        with self.assertRaises(ValueError):
            assign_grade(-0.1)
        with self.assertRaises(ValueError):
            assign_grade(100.1)

    # 2. Marks exactly at passing threshold
    def test_02_marks_exactly_at_passing_threshold(self):
        self.assertEqual(determine_subject_result(35.0), "Pass")

    # 3. Marks below passing threshold
    def test_03_marks_below_passing_threshold(self):
        self.assertEqual(determine_subject_result(34.99), "Fail")
        self.assertEqual(determine_subject_result(0.0), "Fail")

    # 4. Total and average calculations
    def test_04_total_and_average_calculations(self):
        results = calculate_student_results(self.sample_df)
        # Alice: 90 + 85 + 95 = 270, avg = 90.0
        alice = results.loc[results["student_id"] == "T101"].iloc[0]
        self.assertAlmostEqual(alice["total_marks"], 270.0)
        self.assertAlmostEqual(alice["average_marks"], 90.0)
        self.assertEqual(alice["grade"], "A+")

        # Charlie: 50 + 35 + 45 = 130, avg = 130/3 = 43.333333333333336
        charlie = results.loc[results["student_id"] == "T103"].iloc[0]
        self.assertAlmostEqual(charlie["total_marks"], 130.0)
        self.assertAlmostEqual(charlie["average_marks"], 130.0 / 3.0)
        self.assertEqual(charlie["grade"], "E")

    # 5. Subject pass/fail determination
    def test_05_subject_pass_fail_determination(self):
        results = calculate_student_results(self.sample_df)
        charlie = results.loc[results["student_id"] == "T103"].iloc[0]
        self.assertEqual(charlie["python_result"], "Pass")
        self.assertEqual(charlie["mathematics_result"], "Pass")  # 35 marks is pass
        self.assertEqual(charlie["statistics_result"], "Pass")

        daisy = results.loc[results["student_id"] == "T104"].iloc[0]
        self.assertEqual(daisy["python_result"], "Pass")
        self.assertEqual(daisy["mathematics_result"], "Fail")  # 30 marks is fail
        self.assertEqual(daisy["statistics_result"], "Pass")

    # 6. Overall pass/fail determination
    def test_06_overall_pass_fail_determination(self):
        # All >= 35 -> Passed
        self.assertEqual(determine_overall_status(35.0, 35.0, 35.0), "Passed")
        self.assertEqual(determine_overall_status(90.0, 80.0, 70.0), "Passed")
        # One subject below 35 -> Failed
        self.assertEqual(determine_overall_status(35.0, 34.99, 35.0), "Failed")
        # Two subjects below 35 -> Failed
        self.assertEqual(determine_overall_status(20.0, 30.0, 80.0), "Failed")
        # All three below 35 -> Failed
        self.assertEqual(determine_overall_status(10.0, 20.0, 30.0), "Failed")

    # 7. Attendance exactly at 75%
    def test_07_attendance_exactly_at_75_percent(self):
        results = calculate_student_results(self.sample_df)
        bob = results.loc[results["student_id"] == "T102"].iloc[0]
        self.assertEqual(bob["attendance_status"], "Normal")

    # 8. Attendance below 75%
    def test_08_attendance_below_75_percent(self):
        results = calculate_student_results(self.sample_df)
        charlie = results.loc[results["student_id"] == "T103"].iloc[0]
        self.assertEqual(charlie["attendance_status"], "Low Attendance")

    # 9. Subject averages
    def test_09_subject_averages(self):
        results = calculate_student_results(self.sample_df)
        summaries = calculate_subject_summaries(results)
        # Expected Python average: (90 + 80 + 50 + 60) / 4 = 280 / 4 = 70.0
        self.assertAlmostEqual(summaries["subjects"]["Python"]["mean"], 70.0)
        # Expected Mathematics average: (85 + 75 + 35 + 30) / 4 = 225 / 4 = 56.25
        self.assertAlmostEqual(summaries["subjects"]["Mathematics"]["mean"], 56.25)
        # Expected Statistics average: (95 + 85 + 45 + 70) / 4 = 295 / 4 = 73.75
        self.assertAlmostEqual(summaries["subjects"]["Statistics"]["mean"], 73.75)
        # Highest average subject is Statistics
        self.assertEqual(summaries["highest_average_subjects"], ["Statistics"])

    # 10. Class average
    def test_10_class_average(self):
        results = calculate_student_results(self.sample_df)
        class_stats = calculate_class_statistics(results)
        # Individual averages: Alice 90.0, Bob 80.0, Charlie 43.333333333333336, Daisy 53.333333333333336
        # Sum of averages: 90 + 80 + 43.333333333333336 + 53.333333333333336 = 266.6666666666667
        # Class average: 266.6666666666667 / 4 = 66.66666666666667
        expected_class_avg = (90.0 + 80.0 + (130.0 / 3.0) + (160.0 / 3.0)) / 4.0
        self.assertAlmostEqual(class_stats["class_average"], expected_class_avg)

    # 11. Pass percentage
    def test_11_pass_percentage(self):
        self.assertEqual(calculate_pass_percentage(100, 85), 85.0)
        self.assertEqual(calculate_pass_percentage(4, 3), 75.0)
        self.assertEqual(calculate_pass_percentage(0, 0), 0.0)
        with self.assertRaises(ValueError):
            calculate_pass_percentage(10, 12)
        with self.assertRaises(ValueError):
            calculate_pass_percentage(-5, 2)

    # 12. Top-five ranking
    def test_12_top_five_ranking(self):
        # Create dataset with 6 distinct students
        records = [
            {"student_id": f"S0{i}", "student_name": f"Name {i}", "department": "CS", "semester": 1,
             "python_marks": marks, "mathematics_marks": marks, "statistics_marks": marks,
             "attendance_percentage": 80.0}
            for i, marks in enumerate([50.0, 95.0, 70.0, 85.0, 60.0, 90.0], start=1)
        ]
        df = pd.DataFrame(records)
        top_5 = find_top_performers(df, n=5)
        self.assertEqual(len(top_5), 5)
        # Top performer must be S02 (95.0 marks)
        self.assertEqual(top_5.iloc[0]["student_id"], "S02")
        self.assertEqual(top_5.iloc[1]["student_id"], "S06")  # 90.0
        self.assertEqual(top_5.iloc[2]["student_id"], "S04")  # 85.0
        self.assertEqual(top_5.iloc[3]["student_id"], "S03")  # 70.0
        self.assertEqual(top_5.iloc[4]["student_id"], "S05")  # 60.0

    # 13. Tied student averages
    def test_13_tied_student_averages_and_cutoff(self):
        # Create dataset where 5th and 6th students are tied at cutoff
        records = [
            {"student_id": "S1", "student_name": "A", "department": "CS", "semester": 1,
             "python_marks": 95, "mathematics_marks": 95, "statistics_marks": 95, "attendance_percentage": 80},
            {"student_id": "S2", "student_name": "B", "department": "CS", "semester": 1,
             "python_marks": 90, "mathematics_marks": 90, "statistics_marks": 90, "attendance_percentage": 80},
            {"student_id": "S3", "student_name": "C", "department": "CS", "semester": 1,
             "python_marks": 85, "mathematics_marks": 85, "statistics_marks": 85, "attendance_percentage": 80},
            {"student_id": "S4", "student_name": "D", "department": "CS", "semester": 1,
             "python_marks": 80, "mathematics_marks": 80, "statistics_marks": 80, "attendance_percentage": 80},
            {"student_id": "S5", "student_name": "E", "department": "CS", "semester": 1,
             "python_marks": 75, "mathematics_marks": 75, "statistics_marks": 75, "attendance_percentage": 80},
            {"student_id": "S6", "student_name": "F", "department": "CS", "semester": 1,
             "python_marks": 75, "mathematics_marks": 75, "statistics_marks": 75, "attendance_percentage": 80},
            {"student_id": "S7", "student_name": "G", "department": "CS", "semester": 1,
             "python_marks": 60, "mathematics_marks": 60, "statistics_marks": 60, "attendance_percentage": 80},
        ]
        df = pd.DataFrame(records)
        # S5 and S6 both have average 75.0 at 5th place cutoff -> both must be included (length 6)
        top = find_top_performers(df, n=5)
        self.assertEqual(len(top), 6)
        self.assertEqual(list(top["student_id"]), ["S1", "S2", "S3", "S4", "S5", "S6"])

    # 14. Empty datasets
    def test_14_empty_datasets(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            validate_dataset(empty_df)
        with self.assertRaises(ValueError):
            calculate_student_results(empty_df)
        with self.assertRaises(ValueError):
            calculate_class_statistics(empty_df)
        with self.assertRaises(ValueError):
            calculate_subject_summaries(empty_df)

    # 15. Duplicate IDs
    def test_15_duplicate_ids(self):
        dup_df = self.sample_df.copy()
        dup_df.loc[1, "student_id"] = "T101"  # Duplicate of row 0
        with self.assertRaises(ValueError) as ctx:
            validate_dataset(dup_df)
        self.assertIn("Duplicate student_id", str(ctx.exception))

    # 16. Missing columns
    def test_16_missing_columns(self):
        missing_col_df = self.sample_df.drop(columns=["statistics_marks"])
        with self.assertRaises(ValueError) as ctx:
            validate_dataset(missing_col_df)
        self.assertIn("Missing required columns", str(ctx.exception))

    # 17. Invalid marks
    def test_17_invalid_marks(self):
        # Marks > 100
        invalid_high = self.sample_df.copy()
        invalid_high.loc[0, "python_marks"] = 105.0
        with self.assertRaises(ValueError):
            validate_dataset(invalid_high)

        # Marks < 0
        invalid_low = self.sample_df.copy()
        invalid_low.loc[0, "mathematics_marks"] = -5.0
        with self.assertRaises(ValueError):
            validate_dataset(invalid_low)

        # Non-numeric marks
        records = self.sample_df.to_dict(orient="records")
        records[0]["statistics_marks"] = "Excellent"
        invalid_type = pd.DataFrame(records)
        with self.assertRaises(ValueError):
            validate_dataset(invalid_type)

    # 18. Invalid attendance
    def test_18_invalid_attendance(self):
        invalid_att_high = self.sample_df.copy()
        invalid_att_high.loc[0, "attendance_percentage"] = 105.0
        with self.assertRaises(ValueError):
            validate_dataset(invalid_att_high)

        invalid_att_low = self.sample_df.copy()
        invalid_att_low.loc[0, "attendance_percentage"] = -1.0
        with self.assertRaises(ValueError):
            validate_dataset(invalid_att_low)

    # 19. Invalid semester values
    def test_19_invalid_semester_values(self):
        # Zero semester
        invalid_sem_zero = self.sample_df.copy()
        invalid_sem_zero.loc[0, "semester"] = 0
        with self.assertRaises(ValueError):
            validate_dataset(invalid_sem_zero)

        # Negative semester
        invalid_sem_neg = self.sample_df.copy()
        invalid_sem_neg.loc[0, "semester"] = -2
        with self.assertRaises(ValueError):
            validate_dataset(invalid_sem_neg)

        # Non-integer semester
        records = self.sample_df.to_dict(orient="records")
        records[0]["semester"] = 2.5
        invalid_sem_float = pd.DataFrame(records)
        with self.assertRaises(ValueError):
            validate_dataset(invalid_sem_float)

    # 20. Missing or empty CSV input
    def test_20_missing_or_empty_csv_input(self):
        # Missing file
        with self.assertRaises(FileNotFoundError):
            load_dataset("non_existent_file_xyz_123.csv")

        # Empty file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name

        try:
            with self.assertRaises(ValueError):
                load_dataset(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
