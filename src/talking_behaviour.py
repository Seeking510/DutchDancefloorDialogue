import streamlit as st
import plotly.express as px
from src.utils import load_data, COL_TALK_FREQUENCY, COL_TALK_DURATION, COL_TALK_PERCEPTION, TALK_FREQUENCY, TALK_DURATION, TALK_PERCEPTION

def app():
    st.header("Talking Behavior Summary")
    df = load_data()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Conversation Frequency")
        freq_counts = df[COL_TALK_FREQUENCY].value_counts().sort_index()
        fig_freq = px.bar(x=freq_counts.index, y=freq_counts.values, category_orders={"x": TALK_FREQUENCY})
        fig_freq.update_layout(
            xaxis_title="How often people talk",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_freq.update_traces(
            hovertemplate="Frequency: %{x}<br>Participants: %{y}"
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    with col2:
        st.subheader("Conversation Duration")
        duration_counts = df[COL_TALK_DURATION].value_counts().sort_index()
        fig_duration = px.bar(x=duration_counts.index, y=duration_counts.values, category_orders={"x": TALK_DURATION})
        fig_duration.update_layout(
            xaxis_title="How long conversations last",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_duration.update_traces(
            hovertemplate="Duration: %{x}<br>Participants: %{y}"
        )
        st.plotly_chart(fig_duration, use_container_width=True)

    with col3:
        st.subheader("Perception of Talking on Dancefloor")
        perception_counts = df[COL_TALK_PERCEPTION].value_counts().sort_index()
        fig_perception = px.bar(x=perception_counts.index, y=perception_counts.values,
                                category_orders={"x": TALK_PERCEPTION})
        fig_perception.update_layout(
            xaxis_title="How acceptable talking is perceived",
            yaxis_title="Number of Participants",
            hovermode="x"
        )
        fig_perception.update_traces(
            hovertemplate="Perception: %{x}<br>Participants: %{y}"
        )
        st.plotly_chart(fig_perception, use_container_width=True)

    # Add an explanation for people without analytical background
    st.markdown("""
    ### What am I seeing?

    This pages provides insights into how participants interact through conversations at events:

    1. **Conversation Frequency**: Shows how often people engage in conversations on the dancefloor.
    2. **Conversation Duration**: Illustrates the typical length of conversations when they occur.
    3. **Perception of Talking on Dancefloor**: Reflects how acceptable participants find talking on the dancefloor.

    You can hover over any bar in the charts to see more detailed information about the number of participants for each category.
    """)
