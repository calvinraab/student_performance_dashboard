import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("student_data.csv")  # Ensure the dataset is saved as CSV

st.title("📊 Student Performance Dashboard")
st.write("This dashboard provides insights into student quiz performance across different subjects, majors, and grades.")

# Sidebar filters
st.sidebar.header("Filters")
selected_quizzes = st.sidebar.multiselect("Select Quizzes", df["Quiz ID"].unique())
selected_subjects = st.sidebar.multiselect("Select Subjects", df["Subject"].unique())
selected_majors = st.sidebar.multiselect("Select Majors", df["Major"].unique())
selected_grades = st.sidebar.multiselect("Select Grade", df["Grade of Student"].unique())
selected_universities = st.sidebar.multiselect("Select Universities", df["University"].unique())

# Filter data
filtered_df = df.copy()
if selected_quizzes:
    filtered_df = filtered_df[filtered_df["Quiz ID"].isin(selected_quizzes)]
if selected_subjects:
    filtered_df = filtered_df[filtered_df["Subject"].isin(selected_subjects)]
if selected_majors:
    filtered_df = filtered_df[filtered_df["Major"].isin(selected_majors)]
if selected_grades:
    filtered_df = filtered_df[filtered_df["Grade of Student"].isin(selected_grades)]
if selected_universities:
    filtered_df = filtered_df[filtered_df["University"].isin(selected_universities)]

# Summary Statistics
correctness_rate = filtered_df["Correct"].mean() * 100
num_students = filtered_df["Student ID"].nunique()
st.write(f"### Summary Statistics")
st.write(f"- **Overall Correctness Rate:** {correctness_rate:.2f}%")
st.write(f"- **Total Students Analyzed:** {num_students}")

# Layout for visualizations
col1, col2 = st.columns(2)

# Correctness by Subject
with col1:
    st.write("### Correctness by Subject")
    subject_correctness = filtered_df.groupby("Subject")["Correct"].mean() * 100
    fig, ax = plt.subplots()
    subject_correctness.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Correctness (%)")
    st.pyplot(fig)

# Correctness by Major
with col2:
    st.write("### Correctness by Major")
    major_correctness = filtered_df.groupby("Major")["Correct"].mean() * 100
    fig, ax = plt.subplots()
    major_correctness.plot(kind="bar", ax=ax, color="orange")
    ax.set_ylabel("Correctness (%)")
    st.pyplot(fig)

# Performance Over Time & Performance by University side by side
col3, col4 = st.columns(2)

# Performance Over Time
with col3:
    st.write("### Performance Over Time")
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    daily_performance = filtered_df.groupby("Date")["Correct"].mean() * 100
    fig, ax = plt.subplots()
    daily_performance.plot(ax=ax, linestyle="--", marker="o", color="blue")
    ax.set_ylabel("Correctness (%)")
    ax.set_title("Correctness Over Time")
    st.pyplot(fig)

# Performance by University
with col4:
    st.write("### Performance by University")
    university_performance = filtered_df.groupby("University")["Correct"].mean() * 100
    fig, ax = plt.subplots()
    university_performance.plot(kind="bar", ax=ax, color="purple")
    ax.set_ylabel("Correctness (%)")
    ax.set_title("Correctness by University")
    st.pyplot(fig)



# Display filtered dataset
st.write("### Filtered Dataset")
st.dataframe(filtered_df)

# Download filtered data
st.write("### Download Filtered Data")
st.download_button("Download CSV", filtered_df.to_csv(index=False), "filtered_data.csv", "text/csv")
