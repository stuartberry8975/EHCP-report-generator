import streamlit as st
import pandas as pd
import datetime

def load_data(uploaded_file):
    """Load CSV or Excel file into a DataFrame."""
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None

def generate_report(student_data, feedback_data, comparison_data):
    """Generate EHCP review report for each student."""
    report_date = datetime.date.today().strftime("%Y-%m-%d")
    reports = []
    
    for _, student in student_data.iterrows():
        student_name = student['Name']
        ehcp_targets = student.get('EHCP Targets', 'No targets provided')
        feedback = feedback_data[feedback_data['Name'] == student_name]
        grades = comparison_data[comparison_data['Name'] == student_name]
        
        feedback_summary = '\n'.join(feedback['Feedback']) if not feedback.empty else "No feedback available."
        challenges = feedback['Challenges'].dropna().unique()
        key_challenges = ', '.join(challenges) if challenges.any() else "No key challenges noted."
        future_targets = feedback['Suggested Targets'].dropna().unique()
        suggested_targets = ', '.join(future_targets) if future_targets.any() else "No targets suggested."
        
        if not grades.empty:
            school_avg = comparison_data.mean(numeric_only=True)
            student_performance = [f"{subject}: {grades[subject].values[0]} (School Avg: {school_avg[subject]:.2f})" for subject in grades.columns[1:]]
            grade_comparison = '\n'.join(student_performance)
        else:
            grade_comparison = "No grade data available."
        
        report_text = f"""
        **EHCP Review Meeting – {report_date}**
        
        **Student Name:** {student_name}
        
        **EHCP Targets:**
        {ehcp_targets}
        
        **Teacher Feedback:**
        {feedback_summary}
        
        **Key Challenges:**
        {key_challenges}
        
        **Suggested Future Targets:**
        {suggested_targets}
        
        **Grade Comparison:**
        {grade_comparison}
        """
        reports.append(report_text)
    
    return reports

st.title("EHCP Review Report Generator")

student_file = st.file_uploader("Upload Student Data (CSV/Excel)", type=["csv", "xlsx"])
feedback_file = st.file_uploader("Upload Teacher Feedback (CSV/Excel)", type=["csv", "xlsx"])
grades_file = st.file_uploader("Upload Grade Data (CSV/Excel)", type=["csv", "xlsx"])

if st.button("Generate Report"):
    if student_file and feedback_file and grades_file:
        student_data = load_data(student_file)
        feedback_data = load_data(feedback_file)
        comparison_data = load_data(grades_file)
        
        if student_data is not None and feedback_data is not None and comparison_data is not None:
            reports = generate_report(student_data, feedback_data, comparison_data)
            for report in reports:
                st.text_area("Generated Report", report, height=300)
    else:
        st.error("Please upload all required files.")