import streamlit as st

def app():
    st.title("Dutch Dancefloor Dialogue Dashboard")

    st.markdown("""
    <div style="padding: 1em; border-left: 5px solid #2196F3; margin-bottom: 1em;">
        <strong>Welcome to the Dutch Dancefloor Dialogue Dashboard!</strong><br>
        Explore insights into rave culture and behavior, with a focus on talking on the dancefloor.
    </div>
    """, unsafe_allow_html=True)

    st.write("""
    This application provides a comprehensive analysis of various aspects of the rave scene. 
    Use the sidebar to navigate through different sections and gain valuable insights into 
    dancefloor dynamics and participant behaviors.
    """)

    st.header("Dashboard Sections:")

    sections = [
        ("1. Demographics", "Get an overview of survey participants, including age distribution, gender breakdown, and experience levels."),
        ("2. Talking Behavior", "Analyze conversation frequency, duration, and perception on the dancefloor."),
        ("3. Impact Analysis", "Explore how talking affects the overall experience, DJ performance, and event atmosphere."),
        ("4. Quiet Importance", "Understand the relationship between the importance of a quiet environment and likelihood of intervention."),
        ("5. Yapping Factor", "Take a deep dive into talking behavior patterns with our custom 'Yapping Factor' analysis.")
    ]

    for title, description in sections:
        st.markdown(f"""
        <div padding: 1em; border-radius: 5px; margin-bottom: 1em; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
            <strong>{title}</strong><br>
            {description}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    ### How to Use This Dashboard

    1. **Navigate**: Use the sidebar on the left to switch between different analysis sections.
    2. **Interact**: Many charts and graphs are interactive. Hover over data points for more information.
    3. **Filter**: Some sections allow you to filter data. Experiment with different options to dive deeper into the analysis.
    4. **Insights**: Look for key insights and summaries provided below the visualizations.
    5. **Your Input**: In the Yapping Factor section, you can calculate your own score!

    Enjoy exploring the data and uncovering insights about rave culture and behavior!
    """)