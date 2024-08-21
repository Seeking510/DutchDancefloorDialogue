import streamlit as st

def app():
    st.title("Dutch Dancefloor Dialogue Dashboard")

    st.header("What's inside?")

    sections = [
        ("📊 Demographics", "Get an overview of survey participants' age, gender, and experience."),
        ("💬 Talking Behavior", "Analyze dancefloor conversation frequency, duration, and perception."),
        ("🎭 Impact Analysis", "Explore how talking affects the overall experience, DJ performance, and event atmosphere."),
        ("🤫 Quiet Importance", "Understand the relationship between the importance of a quiet environment and likelihood of intervention."),
        ("🗣️ Yapping Factor", "Deep dive into **Yapping Factor** analysis.")
    ]

    for title, description in sections:
        st.markdown(f"""
        <div style="padding: 0.5em; border-radius: 5px; margin-bottom: 0.5em; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
            <strong>{title}</strong><br>
            {description}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    ### What Can you do?

    1. **Navigate**: 👈 Use sidebar
    2. **Interact**: 🖱️ Hover for details
    3. **Filter**: 🔍 Refine your view
    4. **Insights**: 💡 Check summaries
    5. **Participate**: 🧮 Calculate your Yapping Factor!
    """)