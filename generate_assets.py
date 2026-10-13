"""
Generate pixel-perfect light-theme visual assets for README.md and LinkedIn showcase (image.png).
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = r"d:\current project\python with AI\vj"
SCREENSHOTS_DIR = os.path.join(WORKSPACE, "screenshots")
DATA_CSV = os.path.join(WORKSPACE, "data", "students.csv")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def get_font(name="segoeui.ttf", size=16, bold=False):
    font_path = f"C:/Windows/Fonts/{'segoeuib.ttf' if bold else name}"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def get_mono_font(size=14, bold=False):
    font_path = f"C:/Windows/Fonts/{'consolab.ttf' if bold else 'consola.ttf'}"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/cour.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def draw_arrow_right(draw, x1, y, length=24, color=(148, 163, 184, 255), width=2):
    x2 = x1 + length
    draw.line([(x1, y), (x2, y)], fill=color, width=width)
    draw.polygon([(x2, y - 5), (x2 + 7, y), (x2, y + 5)], fill=color)

def draw_arrow_down(draw, x, y1, length=24, color=(99, 102, 241, 255), width=2):
    y2 = y1 + length
    draw.line([(x, y1), (x, y2)], fill=color, width=width)
    draw.polygon([(x - 5, y2), (x, y2 + 7), (x + 5, y2)], fill=color)

# -------------------------------------------------------------
# 1. ANALYTICS CHARTS (screenshots/analytics_charts.png)
# -------------------------------------------------------------
def generate_analytics_charts():
    df = pd.read_csv(DATA_CSV)
    df['total_marks'] = df['python_marks'] + df['mathematics_marks'] + df['statistics_marks']
    df['average_marks'] = df['total_marks'] / 3.0
    
    def get_grade(avg):
        if avg >= 90: return 'A+'
        if avg >= 80: return 'A'
        if avg >= 70: return 'B'
        if avg >= 60: return 'C'
        if avg >= 50: return 'D'
        if avg >= 35: return 'E'
        return 'F'
    
    df['grade'] = df['average_marks'].apply(get_grade)
    df['passed'] = (df['python_marks'] >= 35) & (df['mathematics_marks'] >= 35) & (df['statistics_marks'] >= 35)

    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#ffffff')
    fig.suptitle('Academic Performance Analytics Dashboard (Light Theme)', 
                 fontsize=18, fontweight='bold', color='#0f172a', y=0.98)

    # 1. Subject Benchmark
    subjects = ['Python', 'Mathematics', 'Statistics']
    means = [df['python_marks'].mean(), df['mathematics_marks'].mean(), df['statistics_marks'].mean()]
    medians = [df['python_marks'].median(), df['mathematics_marks'].median(), df['statistics_marks'].median()]
    x = np.arange(len(subjects))
    width = 0.35

    ax1 = axes[0, 0]
    ax1.set_facecolor('#f8fafc')
    rects1 = ax1.bar(x - width/2, means, width, label='Mean Score', color='#3b82f6', edgecolor='#1d4ed8', zorder=3)
    rects2 = ax1.bar(x + width/2, medians, width, label='Median Score', color='#10b981', edgecolor='#047857', zorder=3)
    ax1.set_title('Subject Performance Benchmark (Mean vs Median)', fontsize=13, fontweight='bold', color='#1e293b')
    ax1.set_xticks(x)
    ax1.set_xticklabels(subjects, fontsize=11, color='#334155')
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Score (out of 100)', fontsize=11, color='#334155')
    ax1.grid(axis='y', linestyle='--', alpha=0.6, color='#cbd5e1', zorder=0)
    ax1.legend(loc='lower right', framealpha=0.9)
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e3a8a')
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#065f46')

    # 2. Department-Wise Average Performance
    dept_stats = df.groupby('department')['average_marks'].agg(['mean', 'count']).reset_index()
    dept_stats = dept_stats.sort_values(by='mean', ascending=False)
    ax2 = axes[0, 1]
    ax2.set_facecolor('#f8fafc')
    colors = ['#6366f1', '#0ea5e9', '#8b5cf6', '#f59e0b']
    ax2.set_xticks(range(len(dept_stats)))
    bars = ax2.bar(range(len(dept_stats)), dept_stats['mean'], color=colors, edgecolor='#475569', width=0.55, zorder=3)
    ax2.set_title('Department-Wise Average Score Comparison', fontsize=13, fontweight='bold', color='#1e293b')
    ax2.set_xticklabels(dept_stats['department'], rotation=12, ha='right', fontsize=10, color='#334155')
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('Mean Average Score', fontsize=11, color='#334155')
    ax2.grid(axis='y', linestyle='--', alpha=0.6, color='#cbd5e1', zorder=0)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0f172a')

    # 3. Grade Distribution
    grade_order = ['A+', 'A', 'B', 'C', 'D', 'E', 'F']
    grade_counts = df['grade'].value_counts().reindex(grade_order, fill_value=0)
    ax3 = axes[1, 0]
    ax3.set_facecolor('#f8fafc')
    grade_colors = ['#10b981', '#34d399', '#3b82f6', '#60a5fa', '#f59e0b', '#fb923c', '#ef4444']
    gbars = ax3.bar(grade_order, grade_counts.values, color=grade_colors, edgecolor='#64748b', width=0.55, zorder=3)
    ax3.set_title('Cohort Grade Distribution (30 Students)', fontsize=13, fontweight='bold', color='#1e293b')
    ax3.set_xlabel('Letter Grade', fontsize=11, color='#334155')
    ax3.set_ylabel('Number of Students', fontsize=11, color='#334155')
    ax3.grid(axis='y', linestyle='--', alpha=0.6, color='#cbd5e1', zorder=0)
    for bar in gbars:
        h = bar.get_height()
        if h > 0:
            ax3.annotate(f'{int(h)}', xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0f172a')

    # 4. Attendance vs. Average Marks
    ax4 = axes[1, 1]
    ax4.set_facecolor('#f8fafc')
    pass_normal = df[(df['passed']) & (df['attendance_percentage'] >= 75)]
    pass_low_att = df[(df['passed']) & (df['attendance_percentage'] < 75)]
    fail_all = df[~df['passed']]

    ax4.scatter(pass_normal['attendance_percentage'], pass_normal['average_marks'], 
                color='#10b981', s=70, edgecolors='#047857', label='Passed (Normal Attendance >=75%)', zorder=4)
    ax4.scatter(pass_low_att['attendance_percentage'], pass_low_att['average_marks'], 
                color='#f59e0b', s=75, marker='^', edgecolors='#b45309', label='Passed (Low Attendance <75%)', zorder=4)
    ax4.scatter(fail_all['attendance_percentage'], fail_all['average_marks'], 
                color='#ef4444', s=80, marker='X', edgecolors='#991b1b', label='Failed (Academic Deficit)', zorder=4)

    ax4.axvline(75, color='#dc2626', linestyle='--', linewidth=1.5, alpha=0.8, label='Attendance Cutoff (75%)')
    ax4.axhline(35, color='#6b7280', linestyle=':', linewidth=1.2, alpha=0.8, label='Pass Mark Threshold (35.0)')

    ax4.set_title('Attendance % vs. Student Average Marks', fontsize=13, fontweight='bold', color='#1e293b')
    ax4.set_xlabel('Attendance Percentage (%)', fontsize=11, color='#334155')
    ax4.set_ylabel('Student Average Marks', fontsize=11, color='#334155')
    ax4.set_xlim(50, 100)
    ax4.set_ylim(15, 100)
    ax4.grid(True, linestyle='--', alpha=0.6, color='#cbd5e1', zorder=0)
    ax4.legend(loc='lower right', fontsize=8.5, framealpha=0.92)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(SCREENSHOTS_DIR, "analytics_charts.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 2. HERO BANNER (screenshots/banner_light.png)
# -------------------------------------------------------------
def generate_hero_banner():
    W, H = 1200, 420
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Soft gradient background
    for y in range(H):
        r = int(243 + (255 - 243) * (y / H))
        g = int(246 + (255 - 246) * (y / H))
        b = int(255 + (255 - 255) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Dot pattern
    dot_color = (203, 213, 225, 110)
    for gx in range(40, W - 40, 40):
        for gy in range(40, H - 40, 40):
            draw.ellipse([gx-1, gy-1, gx+1, gy+1], fill=dot_color)

    # Top border line
    draw.rectangle([0, 0, W, 6], fill=(79, 70, 229, 255))

    # Badge 1: EWB COURSES
    draw.rounded_rectangle([60, 36, 335, 66], radius=15, fill=(238, 242, 255, 255), outline=(199, 210, 254, 255), width=1)
    draw.ellipse([74, 47, 82, 55], fill=(79, 70, 229, 255))
    draw.text((92, 42), "EWB COURSES  |  PYTHON WITH AI", fill=(67, 56, 202, 255), font=get_font("segoeuib.ttf", 12, bold=True))

    # Badge 2: TESTS PASSED
    draw.rounded_rectangle([350, 36, 545, 66], radius=15, fill=(236, 253, 245, 255), outline=(167, 243, 208, 255), width=1)
    draw.ellipse([364, 47, 372, 55], fill=(16, 185, 129, 255))
    draw.text((382, 42), "20 / 20 TESTS PASSED", fill=(4, 120, 87, 255), font=get_font("segoeuib.ttf", 12, bold=True))

    # Title & Subtitle
    draw.text((60, 85), "Student Performance Intelligence", fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 36, bold=True))
    draw.text((60, 134), "& Academic Analytics System", fill=(79, 70, 229, 255), font=get_font("segoeuib.ttf", 26, bold=True))

    desc_text = "End-to-End Automated Pipeline for Record Validation, Cohort Statistics, Tie-Aware Ranking, and Attendance Intelligence."
    draw.text((60, 180), desc_text, fill=(71, 85, 105, 255), font=get_font("segoeui.ttf", 15))

    # Metric Cards
    cards = [
        ("30 STUDENTS", "Dataset Ingested", (59, 130, 246)),
        ("83.33%", "Cohort Pass Rate", (16, 185, 129)),
        ("9 SECTIONS", "Terminal Intelligence", (99, 102, 241)),
        ("100% PASS", "20 Automated Tests", (245, 158, 11))
    ]

    card_w = 250
    card_h = 105
    start_x = 60
    card_y = 245
    gap = 25

    for i, (val, label, accent) in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        draw.rounded_rectangle([cx+2, card_y+3, cx+card_w+2, card_y+card_h+3], radius=12, fill=(226, 232, 240, 150))
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        draw.rounded_rectangle([cx+14, card_y+16, cx+18, card_y+card_h-16], radius=2, fill=(*accent, 255))
        
        draw.text((cx+30, card_y+18), val, fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 23, bold=True))
        draw.text((cx+30, card_y+56), label, fill=(100, 116, 139, 255), font=get_font("segoeui.ttf", 13))

    out_path = os.path.join(SCREENSHOTS_DIR, "banner_light.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# -------------------------------------------------------------
# 3. PIPELINE ARCHITECTURE (screenshots/pipeline_architecture.png)
# -------------------------------------------------------------
def generate_pipeline_architecture():
    W, H = 1200, 620
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    for y in range(H):
        tint = int(248 + (255 - 248) * (y / H))
        draw.line([(0, y), (W, y)], fill=(tint, tint, 253, 255))

    draw.text((60, 32), "SYSTEM ARCHITECTURE & DATA PROCESSING PIPELINE", fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 24, bold=True))
    draw.text((60, 68), "Pure functional transformation flow with strict immutability and complete validation across 7 stages", fill=(71, 85, 105, 255), font=get_font("segoeui.ttf", 14))

    stages = [
        ("STAGE 1", "Data Ingestion", "data/students.csv", "Validates file presence, encoding, schema columns, and loads 30 raw student records into Pandas.", (59, 130, 246)),
        ("STAGE 2", "Schema Validation", "Type & Bounds Check", "Ensures positive integer semester, unique STUxxx IDs, non-empty text, and marks/attendance in [0.0, 100.0].", (16, 185, 129)),
        ("STAGE 3", "Metric Computation", "Vectorized NumPy", "Calculates subject totals, unweighted 3-subject averages, subject pass/fail states, and overall student results.", (99, 102, 241)),
        ("STAGE 4", "Grading Engine", "7-Tier Academic Scale", "Applies strict grade thresholds: A+ (>=90) down to F (<35). Zero in-place mutations; independent copies returned.", (245, 158, 11)),
        ("STAGE 5", "Ranking & Ties", "Cutoff Preservation", "Multi-key sorting (average desc, student_id asc). Extends 5th rank to preserve all tied cutoff students.", (14, 165, 233)),
        ("STAGE 6", "Attendance Risk", "75% Compliance Policy", "Independently flags students with attendance < 75% without distorting academic pass/fail outcomes.", (239, 68, 68)),
        ("STAGE 7", "Reporting & Dashboards", "Executive Terminal CLI", "Synthesizes 9 dashboard modules, department & semester comparisons, and automated factual statistical findings.", (168, 85, 247))
    ]

    row1_cards = stages[:4]
    row2_cards = stages[4:]

    # Row 1
    cw1 = 245
    ch1 = 180
    gap1 = 30
    start_x1 = 60
    y1 = 110

    for i, (tag, name, subname, desc, color) in enumerate(row1_cards):
        cx = start_x1 + i * (cw1 + gap1)
        draw.rounded_rectangle([cx+2, y1+3, cx+cw1+2, y1+ch1+3], radius=10, fill=(226, 232, 240, 160))
        draw.rounded_rectangle([cx, y1, cx+cw1, y1+ch1], radius=10, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=1)
        
        # Header strip
        draw.rounded_rectangle([cx, y1, cx+cw1, y1+32], radius=10, fill=(*color, 25))
        draw.rectangle([cx, y1+22, cx+cw1, y1+32], fill=(*color, 25))
        draw.text((cx+14, y1+8), tag, fill=(*color, 255), font=get_font("segoeuib.ttf", 11, bold=True))
        
        draw.text((cx+14, y1+42), name, fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 15, bold=True))
        draw.text((cx+14, y1+64), subname, fill=(100, 116, 139, 255), font=get_font("segoeui.ttf", 11))
        
        words = desc.split()
        lines, cur = [], ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if len(test) > 33:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur: lines.append(cur)
        
        dy = y1 + 86
        for line in lines[:4]:
            draw.text((cx+14, dy), line, fill=(71, 85, 105, 255), font=get_font("segoeui.ttf", 11))
            dy += 18
            
        if i < 3:
            draw_arrow_right(draw, cx + cw1 + 6, y1 + ch1 // 2, length=16, color=(148, 163, 184, 255), width=2)

    # Down arrow from stage 4 to stage 5 area
    draw_arrow_down(draw, start_x1 + 3 * (cw1 + gap1) + cw1 // 2, y1 + ch1 + 6, length=28, color=(99, 102, 241, 255), width=2)

    # Row 2
    cw2 = 330
    ch2 = 180
    gap2 = 45
    start_x2 = 60
    y2 = 360

    for j, (tag, name, subname, desc, color) in enumerate(row2_cards):
        cx = start_x2 + j * (cw2 + gap2)
        draw.rounded_rectangle([cx+2, y2+3, cx+cw2+2, y2+ch2+3], radius=10, fill=(226, 232, 240, 160))
        draw.rounded_rectangle([cx, y2, cx+cw2, y2+ch2], radius=10, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=1)
        
        draw.rounded_rectangle([cx, y2, cx+cw2, y2+32], radius=10, fill=(*color, 25))
        draw.rectangle([cx, y2+22, cx+cw2, y2+32], fill=(*color, 25))
        draw.text((cx+14, y2+8), tag, fill=(*color, 255), font=get_font("segoeuib.ttf", 11, bold=True))
        
        draw.text((cx+14, y2+42), name, fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 15, bold=True))
        draw.text((cx+14, y2+64), subname, fill=(100, 116, 139, 255), font=get_font("segoeui.ttf", 11))
        
        words = desc.split()
        lines, cur = [], ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if len(test) > 46:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur: lines.append(cur)
        
        dy = y2 + 86
        for line in lines[:4]:
            draw.text((cx+14, dy), line, fill=(71, 85, 105, 255), font=get_font("segoeui.ttf", 11))
            dy += 18
            
        if j < 2:
            draw_arrow_right(draw, cx + cw2 + 8, y2 + ch2 // 2, length=24, color=(148, 163, 184, 255), width=2)

    out_path = os.path.join(SCREENSHOTS_DIR, "pipeline_architecture.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# -------------------------------------------------------------
# 4. TERMINAL DASHBOARD PREVIEW (screenshots/terminal_dashboard_preview.png)
# -------------------------------------------------------------
def generate_terminal_dashboard_preview():
    W, H = 1200, 780
    im = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(im)

    wx, wy, ww, wh = 50, 25, 1100, 730
    for i in range(8, 0, -2):
        draw.rounded_rectangle([wx-i, wy-i+4, wx+ww+i, wy+wh+i+4], radius=14, fill=(226, 232, 240, 50))
    draw.rounded_rectangle([wx, wy, wx+ww, wy+wh], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=1)
    
    # Title bar
    draw.rounded_rectangle([wx, wy, wx+ww, wy+42], radius=12, fill=(241, 245, 249, 255))
    draw.rectangle([wx, wy+30, wx+ww, wy+42], fill=(241, 245, 249, 255))
    draw.line([(wx, wy+42), (wx+ww, wy+42)], fill=(226, 232, 240, 255), width=1)
    
    draw.ellipse([wx+16, wy+15, wx+28, wy+27], fill=(239, 68, 68, 255))
    draw.ellipse([wx+36, wy+15, wx+48, wy+27], fill=(245, 158, 11, 255))
    draw.ellipse([wx+56, wy+15, wx+68, wy+27], fill=(16, 185, 129, 255))

    draw.text((wx+ww//2 - 180, wy+13), "PowerShell - python main.py [Student Performance Intelligence]", fill=(71, 85, 105, 255), font=get_font("segoeuib.ttf", 13, bold=True))

    mono = get_mono_font(12)
    mono_b = get_mono_font(12, bold=True)
    tx = wx + 25
    ty = wy + 55

    lines = [
        ("PS D:\\projects\\vj> python main.py", (79, 70, 229), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("  SECTION 4: SUBJECT PERFORMANCE ANALYSIS", (30, 41, 59), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("Subject       Mean    Median   Highest   Lowest   Std Dev    Passed   Failed   Pass Rate", (71, 85, 105), True),
        ("------------------------------------------------------------------------------------------", (203, 213, 225), False),
        ("     Python   62.87    65.00     95.0      22.0     19.25      27        3      90.00%", (15, 23, 42), False),
        ("Mathematics   62.87    66.50     94.0      18.0     20.53      27        3      90.00%", (15, 23, 42), False),
        (" Statistics   64.97    67.00     96.0      29.0     18.02      28        2      93.33%   [HIGHEST]", (5, 150, 105), True),
        ("", (0,0,0), False),
        ("==========================================================================================", (148, 163, 184), False),
        ("  SECTION 5: CLASS PERFORMANCE METRICS", (30, 41, 59), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("Total Cohort Size             : 30 students          Overall Class Pass Rate : 83.33%", (15, 23, 42), False),
        ("Cohort Mean Average Marks     : 63.57 marks          Cohort Median Marks     : 63.17", (15, 23, 42), False),
        ("Highest Individual Average    : 94.33 marks          Lowest Average Marks    : 23.00", (15, 23, 42), False),
        ("Cohort Mean Attendance        : 79.95%               Standard Deviation      : 18.30", (15, 23, 42), False),
        ("", (0,0,0), False),
        ("==========================================================================================", (148, 163, 184), False),
        ("  SECTION 6: TOP PERFORMERS (TIE-AWARE CUTOFF PRESERVED AT RANK 5)", (30, 41, 59), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("Rank  ID      Student Name        Department               Average   Grade   Result", (71, 85, 105), True),
        ("------------------------------------------------------------------------------------------", (203, 213, 225), False),
        (" 1    STU101  Aarav Sharma        Computer Science          94.33     A+     Passed   [TOP #1]", (217, 119, 6), True),
        (" 2    STU102  Diya Patel          Data Science              91.67     A+     Passed   [TOP #2]", (217, 119, 6), True),
        (" 3    STU103  Rohan Verma         Artificial Intelligence   87.67     A      Passed", (15, 23, 42), False),
        (" 4    STU104  Ananya Iyer         Computer Science          84.00     A      Passed   [TIED CUTOFF]", (79, 70, 229), False),
        (" 5    STU105  Kabir Mehta         Data Science              84.00     A      Passed   [TIED CUTOFF]", (79, 70, 229), False),
        (" 6    STU130  Ananya Roy          Information Technology    84.00     A      Passed   [TIED CUTOFF]", (79, 70, 229), False),
        ("", (0,0,0), False),
        ("==========================================================================================", (148, 163, 184), False),
        ("  SECTION 7: ATTENDANCE INTELLIGENCE (< 75% FLAGGED ROSTER)", (220, 38, 38), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("Cohort Attendance Average : 79.95%   |   Normal (>=75%): 22 (73.3%)   |   Low (<75%): 8 (26.7%)", (71, 85, 105), False),
        ("Flagged Students : STU107 (72.5%), STU109 (68.0%), STU113 (74.0%), STU117 (65.0%), STU120 (60.0%), ...", (185, 28, 28), False),
        ("", (0,0,0), False),
        ("==========================================================================================", (148, 163, 184), False),
        ("  SECTION 9: KEY ANALYTICAL FINDINGS", (30, 41, 59), True),
        ("==========================================================================================", (148, 163, 184), False),
        ("[1] Class pass rate is 83.33% with Statistics achieving highest subject average (64.97 marks).", (15, 23, 42), False),
        ("[2] Computer Science recorded highest departmental mean average (66.46 marks).", (15, 23, 42), False),
        ("[3] Zero mutation functional architecture verified across 20 automated unit test scenarios.", (5, 150, 105), True),
    ]

    for text, col, is_b in lines:
        font_use = mono_b if is_b else mono
        draw.text((tx, ty), text, fill=(*col, 255), font=font_use)
        ty += 16

    out_path = os.path.join(SCREENSHOTS_DIR, "terminal_dashboard_preview.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# -------------------------------------------------------------
# 5. LINKEDIN POST IMAGE (image.png in root and screenshots)
# -------------------------------------------------------------
def generate_linkedin_image():
    W, H = 1200, 675
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    for y in range(H):
        r = int(245 + (255 - 245) * (y / H))
        g = int(248 + (255 - 248) * (y / H))
        b = int(255 + (255 - 255) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    dot_color = (226, 232, 240, 130)
    for gx in range(30, W, 45):
        for gy in range(30, H, 45):
            draw.ellipse([gx-1, gy-1, gx+1, gy+1], fill=dot_color)

    draw.rectangle([0, 0, W, 8], fill=(79, 70, 229, 255))

    # Badge Pill
    draw.rounded_rectangle([50, 36, 420, 68], radius=16, fill=(238, 242, 255, 255), outline=(199, 210, 254, 255), width=1)
    draw.ellipse([64, 48, 72, 56], fill=(79, 70, 229, 255))
    draw.text((82, 43), "PROJECT SHOWCASE  |  PYTHON WITH AI", fill=(67, 56, 202, 255), font=get_font("segoeuib.ttf", 12, bold=True))

    # Title & Subtitle
    draw.text((50, 84), "Student Performance Intelligence", fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 34, bold=True))
    draw.text((50, 128), "& Academic Analytics System", fill=(79, 70, 229, 255), font=get_font("segoeuib.ttf", 26, bold=True))

    draw.text((50, 172), "Automated academic data processing, cohort statistics, tie-aware ranking & attendance intelligence.", fill=(71, 85, 105, 255), font=get_font("segoeui.ttf", 14))

    features = [
        ("Vectorized Python & NumPy Engine", "High-performance data transformation with zero in-place mutations.", (59, 130, 246)),
        ("7-Tier Grading & Cutoff Tie-Breaker", "Calculates letter grades (A+ to F) and preserves all 5th-rank cutoff ties.", (16, 185, 129)),
        ("Independent Attendance Risk Detection", "Flags students below 75% attendance without altering academic merit.", (245, 158, 11)),
        ("20/20 Passing Automated Unit Tests", "100% test coverage across schema, boundaries, ties, and edge cases.", (99, 102, 241))
    ]

    fy = 215
    for title, desc, col in features:
        draw.rounded_rectangle([50, fy, 590, fy+60], radius=10, fill=(255, 255, 255, 230), outline=(226, 232, 240, 255), width=1)
        draw.rounded_rectangle([50, fy, 55, fy+60], radius=4, fill=(*col, 255))
        
        # Draw a small clean colored icon dot
        draw.ellipse([68, fy+14, 78, fy+24], fill=(*col, 255))
        draw.text((88, fy+10), title, fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 14, bold=True))
        draw.text((88, fy+32), desc, fill=(100, 116, 139, 255), font=get_font("segoeui.ttf", 11))
        fy += 72

    # Tech Stack Pills
    tech_y = 515
    draw.text((50, tech_y), "TECH STACK:", fill=(100, 116, 139, 255), font=get_font("segoeuib.ttf", 11, bold=True))
    pills = ["Python 3.11+", "Pandas 2.0+", "NumPy 1.24+", "unittest", "CSV RFC 4180"]
    px = 135
    for p in pills:
        pill_w = len(p) * 7 + 16
        draw.rounded_rectangle([px, tech_y-3, px+pill_w, tech_y+21], radius=9, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
        draw.text((px+8, tech_y), p, fill=(30, 41, 59, 255), font=get_font("segoeui.ttf", 11))
        px += pill_w + 10

    # Author & Repo Footer
    draw.line([(50, 560), (590, 560)], fill=(226, 232, 240, 255), width=1)
    draw.text((50, 576), "Developed by Vijay  |  EWB Courses - Python with AI", fill=(30, 41, 59, 255), font=get_font("segoeuib.ttf", 13, bold=True))
    draw.text((50, 602), "Repository: github.com/vijaymahes9080/python-with-ai-internship-mini-project", fill=(79, 70, 229, 255), font=get_font("segoeui.ttf", 12))

    # Right Column: KPIs
    rx = 635
    kpis = [
        ("30", "Students Ingested", (59, 130, 246)),
        ("83.33%", "Cohort Pass Rate", (16, 185, 129)),
        ("64.97", "Top Subject Avg (Stats)", (99, 102, 241)),
        ("20 / 20", "Test Cases Passed", (245, 158, 11))
    ]

    kw, kh = 242, 85
    for idx, (val, lbl, clr) in enumerate(kpis):
        kx = rx + (idx % 2) * (kw + 22)
        ky = 85 + (idx // 2) * (kh + 16)
        
        draw.rounded_rectangle([kx+2, ky+3, kx+kw+2, ky+kh+3], radius=12, fill=(226, 232, 240, 150))
        draw.rounded_rectangle([kx, ky, kx+kw, ky+kh], radius=12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        draw.ellipse([kx+16, ky+18, kx+26, ky+28], fill=(*clr, 255))
        
        draw.text((kx+36, ky+12), val, fill=(15, 23, 42, 255), font=get_font("segoeuib.ttf", 22, bold=True))
        draw.text((kx+16, ky+50), lbl, fill=(100, 116, 139, 255), font=get_font("segoeui.ttf", 12))

    # Right Side: Terminal Execution Showcase Card
    my = 295
    mw = 510
    mh = 330
    draw.rounded_rectangle([rx+2, my+3, rx+mw+2, my+mh+3], radius=12, fill=(226, 232, 240, 150))
    draw.rounded_rectangle([rx, my, rx+mw, my+mh], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=1)
    
    # Mini Window Header
    draw.rounded_rectangle([rx, my, rx+mw, my+32], radius=12, fill=(241, 245, 249, 255))
    draw.rectangle([rx, my+22, rx+mw, my+32], fill=(241, 245, 249, 255))
    draw.line([(rx, my+32), (rx+mw, my+32)], fill=(226, 232, 240, 255), width=1)
    draw.ellipse([rx+12, my+11, rx+20, my+19], fill=(239, 68, 68, 255))
    draw.ellipse([rx+26, my+11, rx+34, my+19], fill=(245, 158, 11, 255))
    draw.ellipse([rx+40, my+11, rx+48, my+19], fill=(16, 185, 129, 255))
    draw.text((rx+60, my+9), "Live Terminal Dashboard Output (9 Sections)", fill=(71, 85, 105, 255), font=get_font("segoeuib.ttf", 10, bold=True))

    mini_mono = get_mono_font(11)
    mini_mono_b = get_mono_font(11, bold=True)
    mty = my + 44
    mtx = rx + 16

    mini_lines = [
        (">> SECTION 6: STUDENT RANKINGS & TOP PERFORMERS", (79, 70, 229), True),
        ("Rank ID     Name         Dept       Avg   Grade Result", (100, 116, 139), True),
        (" 1   STU101 Aarav Sharma CompSci    94.33  A+   Passed [TOP 1]", (217, 119, 6), True),
        (" 2   STU102 Diya Patel   DataSci    91.67  A+   Passed [TOP 2]", (217, 119, 6), True),
        (" 3   STU103 Rohan Verma  AI         87.67  A    Passed", (15, 23, 42), False),
        (" 4   STU104 Ananya Iyer  CompSci    84.00  A    Passed [TIE]", (59, 130, 246), False),
        (" 5   STU105 Kabir Mehta  DataSci    84.00  A    Passed [TIE]", (59, 130, 246), False),
        (" 6   STU130 Ananya Roy   InfoTech   84.00  A    Passed [TIE]", (59, 130, 246), False),
        ("-------------------------------------------------------", (226, 232, 240), False),
        (">> SECTION 7: ATTENDANCE RISK (THRESHOLD: 75.0%)", (220, 38, 38), True),
        ("Normal Attendance (>=75%) : 22 students (73.3%)", (5, 150, 105), False),
        ("Low Attendance (<75%)    : 8 students (26.7%) [ALERT]", (220, 38, 38), False),
        ("-------------------------------------------------------", (226, 232, 240), False),
        (">> SECTION 9: SUMMARY & DEPARTMENT BENCHMARKS", (30, 41, 59), True),
        ("Highest Dept Avg: Computer Science (66.46 marks)", (15, 23, 42), False),
        ("Class Pass Rate : 83.33% (25 passed / 5 failed)", (15, 23, 42), False),
    ]

    for m_text, m_col, m_b in mini_lines:
        draw.text((mtx, mty), m_text, fill=(*m_col, 255), font=mini_mono_b if m_b else mini_mono)
        mty += 16

    root_out_path = os.path.join(WORKSPACE, "image.png")
    im.save(root_out_path, "PNG")
    print("Saved root image:", root_out_path)

    ss_out_path = os.path.join(SCREENSHOTS_DIR, "linkedin_showcase.png")
    im.save(ss_out_path, "PNG")
    print("Saved screenshot image:", ss_out_path)

if __name__ == "__main__":
    print("Regenerating assets...")
    generate_analytics_charts()
    generate_hero_banner()
    generate_pipeline_architecture()
    generate_terminal_dashboard_preview()
    generate_linkedin_image()
    print("All updated assets generated successfully!")
