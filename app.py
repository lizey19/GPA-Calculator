import streamlit as st
import pandas as pd

# --- Page setup ---
st.set_page_config(page_title="GPA & CGPA Calculator", layout="centered")

st.title("🎓 GPA & CGPA Calculator")
st.write("Easily calculate your Semester GPA and Overall CGPA")

# --- Semester GPA Section ---
st.header("📘 1st Semester GPA Calculation")

num_courses = st.number_input("Enter number of courses in 1st semester:", min_value=1, max_value=15, step=1)

course_data = []

for i in range(int(num_courses)):
    st.subheader(f"Course {i+1}")
    course_name = st.text_input(f"Course Name {i+1}", key=f"name_{i}")
    credit_hours = st.number_input(f"Credit Hours for {course_name or 'Course ' + str(i+1)}", 1, 5, step=1, key=f"ch_{i}")
    grade = st.selectbox(f"Grade for {course_name or 'Course ' + str(i+1)}", 
                         ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'], 
                         key=f"grade_{i}")
    course_data.append({"Course": course_name, "Credit Hours": credit_hours, "Grade": grade})

# Convert to DataFrame
df = pd.DataFrame(course_data)

# Grade points mapping
grade_points = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}

# --- GPA Calculation ---
if st.button("Calculate GPA"):
    df["Grade Points"] = df["Grade"].map(grade_points)
    df["Quality Points"] = df["Grade Points"] * df["Credit Hours"]

    total_quality_points = df["Quality Points"].sum()
    total_credits = df["Credit Hours"].sum()

    gpa = total_quality_points / total_credits if total_credits > 0 else 0

    st.success(f"📘 Your 1st Semester GPA: **{gpa:.2f}**")
    st.dataframe(df)

# --- CGPA Section ---
st.header("📊 Calculate Overall CGPA")
prev_semesters = st.number_input("Enter number of previous semesters (before 1st semester):", 0, 10, 0)

if prev_semesters > 0:
    total_prev_gpa = 0
    total_prev_credits = 0

    for s in range(int(prev_semesters)):
        st.subheader(f"Previous Semester {s+1}")
        gpa_prev = st.number_input(f"GPA for Semester {s+1}", 0.0, 4.0, step=0.01, key=f"gpa_prev_{s}")
        credits_prev = st.number_input(f"Credit Hours for Semester {s+1}", 1, 25, step=1, key=f"ch_prev_{s}")
        total_prev_gpa += gpa_prev * credits_prev
        total_prev_credits += credits_prev

    if st.button("Calculate Overall CGPA"):
        # Ensure total_quality_points and total_credits exist
        if "total_quality_points" not in locals():
            st.warning("Please calculate your 1st semester GPA first!")
        else:
            total_points = total_prev_gpa + total_quality_points
            total_all_credits = total_prev_credits + total_credits
            cgpa = total_points / total_all_credits if total_all_credits > 0 else 0
            st.success(f"🎯 Your Overall CGPA: **{cgpa:.2f}**")

st.caption("Developed with ❤️ using Streamlit")

