import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout="wide", page_title="Employee Attrition Dashboard")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('employee.csv')

data = load_data()

# Sidebar filter
st.sidebar.title("Filter Data")
department = st.sidebar.multiselect("Select Department", options=data['Department'].unique(), default=data['Department'].unique())
overtime = st.sidebar.multiselect("Overtime Status", options=data['OverTime'].unique(), default=data['OverTime'].unique())

filtered_data = data[(data['Department'].isin(department)) & (data['OverTime'].isin(overtime))]

# Main dashboard
st.title("🚀 Employee Attrition Insights")

# Summary stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Employees", len(filtered_data))
with col2:
    attr_rate = filtered_data['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100
    st.metric("Attrition Rate", f"{attr_rate:.2f}%")
with col3:
    avg_income = filtered_data['MonthlyIncome'].mean()
    st.metric("Avg. Monthly Income", f"${avg_income:,.0f}")

# Tabs for visualization
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Attrition Insights", "📉 Income & Satisfaction"])

# Tab 1 — Overview
with tab1:
    st.subheader("Attrition Status Distribution")
    fig1 = px.pie(filtered_data, names='Attrition', color='Attrition',
                  color_discrete_map={'Yes': '#FF6347', 'No': '#4682B4'},
                  title="Active vs Exiting Employees")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Gender Distribution by Attrition")
    fig2 = px.histogram(filtered_data, x="Gender", color="Attrition", barmode="group",
                        color_discrete_map={'Yes': '#FF6347', 'No': '#4682B4'})
    st.plotly_chart(fig2, use_container_width=True)

# Tab 2 — Attrition Insights
with tab2:
    st.subheader("Boxplot: Age vs Monthly Income by Attrition")
    fig3 = px.box(filtered_data, x='Attrition', y='MonthlyIncome', points='all', color='Attrition',
                  color_discrete_map={'Yes': '#FF6347', 'No': '#4682B4'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Attrition by Job Role")
    attr_by_job = filtered_data[filtered_data['Attrition'] == 'Yes'].groupby('JobRole').size().reset_index(name='Attrition Count')
    fig4 = px.bar(attr_by_job, x='Attrition Count', y='JobRole', orientation='h',
                  color='Attrition Count', color_continuous_scale='Reds')
    st.plotly_chart(fig4, use_container_width=True)

# Tab 3 — Income & Satisfaction
with tab3:
    st.subheader("Satisfaction vs Attrition (Scatter)")
    fig5 = px.scatter(filtered_data, x='EnvironmentSatisfaction', y='JobSatisfaction',
                      color='Attrition', size='MonthlyIncome', symbol='Gender',
                      color_discrete_map={'Yes': '#FF6347', 'No': '#4682B4'},
                      title="Environment vs Job Satisfaction")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Correlation Heatmap (Numerical Columns)")
    corr_data = filtered_data.select_dtypes(include=['int64', 'float64'])
    corr = corr_data.corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("© 2025 Employee Attrition Dashboard — Customized with ❤️ using Streamlit")
