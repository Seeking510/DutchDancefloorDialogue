import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, COL_TALK_FREQUENCY, COL_TALK_DURATION, COL_AGE, COL_GENDER, COL_ATTENDANCE, \
    COL_EXPERIENCE, COL_IMPACT_EXPERIENCE, COL_IMPACT_DJ, COL_IMPACT_ATMOSPHERE, COL_TALK_PERCEPTION, TALK_FREQUENCY, \
    TALK_DURATION

# Mapping for scores
frequency_map = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 4, 'Always': 6}
duration_map = {'Just a few words': 1, '1-5 minutes': 3, '>5 minutes': 5}

# Weights for frequency and duration
frequency_weight = 0.7
duration_weight = 0.3

# Calculate maximum possible Yapping Factor
max_yapping_factor = (max(frequency_map.values()) * frequency_weight) + (max(duration_map.values()) * duration_weight)

def calculate_normalized_yapping_factor(frequency, duration):
    frequency_score = frequency_map[frequency]
    duration_score = duration_map[duration]

    yapping_factor = (frequency_score * frequency_weight) + (duration_score * duration_weight)
    if frequency == 'Never':
        yapping_factor = 0
    normalized_factor = (yapping_factor / max_yapping_factor) * 100
    return normalized_factor

def calculate_yapping_factor(row):
    return calculate_normalized_yapping_factor(row[COL_TALK_FREQUENCY], row[COL_TALK_DURATION])

def interpret_yapping_factor(user_yapping):
    if user_yapping == 0:
        return "Congratulations! You've achieved monk-like silence. 🧘"
    elif 0 < user_yapping <= 20:
        return "Your silence is a gift to the dancefloor. 🎁"
    elif 20 < user_yapping <= 40:
        return "Low talker alert! You're more about the groove than the chat. 🕺"
    elif 40 < user_yapping <= 60:
        return "The Goldilocks of conversation - not too much, not too little. Or is it? 🤔"
    elif 60 < user_yapping <= 80:
        return "Chatty Cathy, is that you? The music might be missing you! 🎵"
    elif 80 < user_yapping < 100:
        return "We've got a champion yapper here! Your vocals might be competing with the DJ's. 🎤"
    else:  # user_yapping == 100
        return "🏆 Maximum Yapper Achievement Unlocked! You're the life of the party... or are you? 🎉"

def app():
    st.header("Yapping Factor Analysis")
    df = load_data()
    df['YAPPING_FACTOR'] = df.apply(calculate_yapping_factor, axis=1)

    st.write("""
    Welcome to the Yapping Factor Analysis! This dashboard explores how much people talk at rave events 
    and how it relates to various aspects of the experience. The Yapping Factor combines talking frequency 
    and duration into a single measure.
    """)

    # Histogram of Yapping Factor
    st.subheader("Distribution of Yapping Factor")
    fig_hist = px.histogram(df, x='YAPPING_FACTOR', nbins=20)
    fig_hist.update_layout(
        title_text='Distribution of Yapping Factor',
        xaxis_title="Yapping Factor",
        yaxis_title="Number of Participants"
    )
    fig_hist.update_traces(
        hovertemplate="Yapping Factor: %{x:.2f}<br>Count: %{y}"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Main selection for analysis type
    # analysis_type = st.radio(
    #     "Select primary analysis variable:",
    #     ["Yapping Factor", "Talking Frequency", "Talking Duration"]
    # )
    analysis_type = "Yapping Factor"
    # Map the selection to the corresponding column
    analysis_var_map = {
        "Yapping Factor": "YAPPING_FACTOR",
        "Talking Frequency": COL_TALK_FREQUENCY,
        "Talking Duration": COL_TALK_DURATION
    }

    primary_var = analysis_var_map[analysis_type]

    # Secondary variable selection
    secondary_var_type = st.selectbox(
        "Select breakdown variable type:",
        ["Demographics", "Perception of Talking", "Impact of Talking"]
    )

    # Options for secondary variable based on type
    if secondary_var_type == "Demographics":
        secondary_var = st.selectbox(
            "Select demographic variable:",
            [COL_AGE, COL_GENDER, COL_ATTENDANCE, COL_EXPERIENCE]
        )
    elif secondary_var_type == "Perception of Talking":
        secondary_var = COL_TALK_PERCEPTION
    else:  # Impact of Talking
        secondary_var = st.selectbox(
            "Select impact type:",
            [COL_IMPACT_EXPERIENCE, COL_IMPACT_DJ, COL_IMPACT_ATMOSPHERE]
        )

    # Create visualization based on selections
    if primary_var == "YAPPING_FACTOR":
        data = df.groupby(secondary_var)[primary_var].mean().reset_index()
        fig = px.bar(data, x=secondary_var, y=primary_var,
                     title=f"Average {analysis_type} by {secondary_var}")
        fig.update_traces(
            hovertemplate=f"{secondary_var}: %{{x}}<br>{analysis_type}: %{{y:.2f}}"
        )
    else:
        data = df.groupby([secondary_var, primary_var]).size().reset_index(name='count')
        fig = px.bar(data, x=secondary_var, y='count', color=primary_var,
                     title=f"{analysis_type} Distribution by {secondary_var}")
        fig.update_traces(
            hovertemplate=f"{secondary_var}: %{{x}}<br>{primary_var}: %{{color}}<br>Count: %{{y}}"
        )

    # Update layout
    fig.update_layout(xaxis_title=secondary_var, yaxis_title=analysis_type if primary_var == "YAPPING_FACTOR" else "Count")

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Additional insights
    st.subheader("Key Insights")

    if primary_var == "YAPPING_FACTOR":
        avg_value = df[primary_var].mean()
        max_value = df[primary_var].max()
        min_value = df[primary_var].min()

        st.write(f"Average {analysis_type}: {avg_value:.2f}")
        st.write(f"Maximum {analysis_type}: {max_value:.2f}")
        st.write(f"Minimum {analysis_type}: {min_value:.2f}")

    # Allow users to input their own data
    st.header("Calculate Your Own Yapping Factor!")

    user_frequency = st.selectbox("Select your talking frequency:", TALK_FREQUENCY)
    user_duration = st.selectbox("Select your typical talking duration:", TALK_DURATION)

    user_yapping = calculate_normalized_yapping_factor(user_frequency, user_duration)
    st.write(f"Your Normalized Yapping Factor is: {user_yapping:.2f}")

    yapping_interpretation = interpret_yapping_factor(user_yapping)
    st.write(yapping_interpretation)

    # Add explanation for people without analytical background
    st.markdown("""
    ### Understanding the Yapping Factor Analysis

    1. **Yapping Factor**: 
       - This is a measure we've created to quantify how much people talk at rave events.
       - It combines how often people talk (frequency) and how long they talk (duration).
       - The scale goes from 0 to 100.

    2. **Distribution Chart**: 
       - This shows how common different Yapping Factor scores are among participants.
       - The x-axis shows the Yapping Factor score, and the y-axis shows how many people have that score.

    3. **Analysis Charts**:
       - These show how the Yapping Factor relates to other aspects of the rave experience.
       - You can choose what to analyze using the dropdown menus.

    4. **Your Own Yapping Factor**:
       - You can calculate your personal Yapping Factor based on how often and how long you typically talk at raves.
       - The interpretation is just for fun - there's no "right" or "wrong" Yapping Factor!

    This analysis can help event organizers and attendees understand talking behaviors at raves and how they might impact the experience.
    """)