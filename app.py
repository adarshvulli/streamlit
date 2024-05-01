import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import plotly.graph_objects as go
# Fake API Key placeholder, replace with your actual OpenAI API key

OPEN_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxzxxxxxxxxx"
# print(st.secrets)

# client = OpenAI(api_key=st.secrets["global"]["OPENAI_API_KEY"])
client = OpenAI(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxzxxxxxxxxx")


from statsmodels.tsa.statespace.sarimax import SARIMAX

  # This should print out the contents of your secrets

# Function to load data from CSV
def load_data():
    # Load data from uploaded CSV
    df = pd.read_csv('/Users/jarvis/Library/CloudStorage/OneDrive-IndianaUniversity/sem2/Mangmentacess/peopleanalytics/employee_data.csv')
    df['Date'] = pd.date_range(start='2021-01-01', periods=len(df), freq='D')
    df.set_index('Date', inplace=True)
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    return df

data = load_data()

# Define the chat with RAG page
def chat_with_rag():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.header("Chat with RAG")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


# 3D scatter plot page
def scatter_plot_3d():
    st.header("Attrition Rate among departments of different ages")
    fig = go.Figure(data=[go.Scatter3d(
        x=data['Age'],
        y=data['Department'],
        z=data['Attrition'],
        mode='markers',
        hovertemplate='<b>Age</b>: %{x} <br> <b>Department</b>: %{y} <br> <b>Attrition</b>: %{z}',
        marker=dict(
            size=12,
            color=data['Age'],
            colorscale='Viridis',
            opacity=0.8
        )
    )])

    fig.update_layout(
        scene=dict(
            xaxis=dict(title={'text': 'Age', 'font_size': 18, 'font_family': 'Courier New'}),
            yaxis=dict(title={'text': 'Department', 'font_size': 18, 'font_family': 'Courier New'}),
            zaxis=dict(title={'text': 'Attrition', 'font_size': 18, 'font_family': 'Courier New'}),
            xaxis_tickfont=dict(color='black'),
            yaxis_tickfont=dict(color='black'),
            zaxis_tickfont=dict(color='black'),
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            zaxis_showgrid=False,
        ),
        plot_bgcolor='#E6E6E6',
        paper_bgcolor='#E6E6E6',
    )

    st.plotly_chart(fig)



# Define the data visualizations page
def data_visualizations():
    st.title('Employee Data Visualizations')

    # Display various plots using Plotly Express
    fig_age = px.histogram(data.reset_index(), x='JobSatisfaction')
    fig_gender = px.pie(data.reset_index(), names='Gender')
    fig_years = px.histogram(data.reset_index(), x='YearsAtCompany', nbins=10)
    fig_satisfaction = px.histogram(data.reset_index(), x='JobLevel')
    fig_dept = px.histogram(data.reset_index(), x='Department')


    st.header("Job Satisfaction Levels")
    st.plotly_chart(fig_age)
    st.header("Gender Distribution")
    st.plotly_chart(fig_gender)
    st.header("Years at Company Distribution")
    st.plotly_chart(fig_years)
    st.header("Job Levels")
    st.plotly_chart(fig_satisfaction)
    st.header("Employees per Department")
    st.plotly_chart(fig_dept)

    scatter_plot_3d()



# Define the attrition forecast page using SARIMAX
def attrition_forecast():
    st.header("Attrition Forecast")
    daily_data = data['Attrition'].resample('D').sum()
    model = SARIMAX(daily_data, order=(1, 0, 0), seasonal_order=(1, 1, 0, 12))
    results = model.fit(disp=0)
    forecast = results.get_forecast(steps=30)
    predicted_attrition = forecast.predicted_mean
    predicted_attrition_df = predicted_attrition.to_frame().reset_index()
    predicted_attrition_df.columns = ['Date', 'Predicted Attrition']
    fig = px.line(predicted_attrition_df, x='Date', y='Predicted Attrition')
    st.plotly_chart(fig)

# Define home page
def home_page():
    st.header('Welcome to the Employee Data Visualization App',divider='rainbow')
    st.write("Navigate using the sidebar to explore different functionalities.")

    st.subheader("This app provides insights into the employee data of a company.")
    st.write("Adarsh Vulli - Spring 2024")



# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Choose a page:', ['Home', 'Data Visualizations', 'Attrition Forecast', 'Chat with RAG'])

# Render the appropriate page
if page == 'Home':
    home_page()
elif page == 'Data Visualizations':
    data_visualizations()
elif page == 'Attrition Forecast':
    attrition_forecast()
elif page == 'Chat with RAG':
    chat_with_rag()

























