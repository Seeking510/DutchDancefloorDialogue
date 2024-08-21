import streamlit as st
import plotly.express as px
from src.utils import load_data, COL_AGE, COL_GENDER, COL_ATTENDANCE, COL_EXPERIENCE


def app():
    st.header("Demographic Summary")
    df = load_data()

    # Calculate total number of participants
    total_participants = len(df)
    st.subheader(f"Total Participants: {total_participants}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Age Distribution")
        age_counts = df[COL_AGE].value_counts().sort_index()
        fig_age = px.bar(x=age_counts.index, y=age_counts.values)
        fig_age.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_age.update_traces(
            hovertemplate="Age Group: %{x}<br>Participants: %{y}"
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        st.subheader("Gender Distribution")
        gender_counts = df[COL_GENDER].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title=f"Total: {total_participants}"
        )
        fig_gender.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="Gender: %{label}<br>Participants: %{value}<br>Percentage: %{percent}"
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    with col3:
        st.subheader("Attendance Frequency")
        attendance_counts = df[COL_ATTENDANCE].value_counts()
        fig_attendance = px.pie(
            values=attendance_counts.values,
            names=attendance_counts.index,
            title=f"Total: {total_participants}"
        )
        fig_attendance.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="Frequency: %{label}<br>Participants: %{value}<br>Percentage: %{percent}"
        )
        st.plotly_chart(fig_attendance, use_container_width=True)

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Years of Experience")
        experience_counts = df[COL_EXPERIENCE].value_counts().sort_index()
        fig_experience = px.bar(x=experience_counts.index, y=experience_counts.values)
        fig_experience.update_layout(
            xaxis_title="Years of Experience",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_experience.update_traces(
            hovertemplate="Experience: %{x} years<br>Participants: %{y}"
        )
        st.plotly_chart(fig_experience, use_container_width=True)

    with col5:
        st.subheader("Roles in Rave Scene")
        roles = ['Role_Attendee/Raver', 'Role_DJ', 'Role_Producer', 'Role_Event organizer', 'Role_Club staff',
                 'Role_Other']
        role_counts = df[roles].sum().sort_values(ascending=False)
        fig_roles = px.bar(x=role_counts.index, y=role_counts.values)
        fig_roles.update_layout(
            xaxis_title="Role",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_roles.update_traces(
            hovertemplate="Role: %{x}<br>Participants: %{y}"
        )
        st.plotly_chart(fig_roles, use_container_width=True)

    # Add an explanation for people without analytical background
    st.markdown("""
    ### What am I seeing?

    This page provides a summary of our survey participants:

    1. **Age Distribution**: Shows how many participants are in each age group.
    2. **Gender Distribution**: Displays the proportion of participants by gender.
    3. **Attendance Frequency**: Illustrates how often participants attend raves/electronic music events.
    4. **Years of Experience**: Indicates the years of experience among participants.
    5. **Roles in Rave Scene**: Highlights the various roles participants play in the rave community.

    You can hover over any part of the charts to see more detailed information.
    """)