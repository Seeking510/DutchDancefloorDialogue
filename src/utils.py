import streamlit as st
import pandas as pd

# Define column names
COL_AGE = "How old are you?"
COL_GENDER = "Gender identity"
COL_ATTENDANCE = "How often do you attend raves/electronic music events?"
COL_EXPERIENCE = "Years of experience in the rave scene"
COL_PRIMARY_ROLE = "What is your primary role in the rave scene?"

COL_TALK_FREQUENCY = "How often do you engage in conversations on the dancefloor?"
COL_TALK_REASON = "If you talk on the dancefloor, what's the primary reason?"
COL_TALK_DURATION = "How long do your dancefloor conversations typically last?"
COL_TALK_PERCEPTION = "Do you perceive talking on the dancefloor as:"

COL_COVID_CHANGE = "Have you noticed a change in dancefloor talking behavior since the COVID-19 pandemic?"
COL_TALKING_FACTORS = "What factors do you think contribute to increased talking on the dancefloor? (Select all that apply)"

COL_QUIET_IMPORTANCE = "How important is it to you to have a quiet dancefloor environment?"
COL_LIKELIHOOD_INTERVENE = "How likely are you to ask others to stop talking if it's disturbing your experience?"

COL_IMPACT_EXPERIENCE = "Do you think talking on the dancefloor affects your own experience?"
COL_IMPACT_DJ = "Do you think talking on the dancefloor affects DJ's performance?"
COL_IMPACT_ATMOSPHERE = "Do you think talking on the dancefloor affects overall event atmosphere?"

# Define custom orders
AGE_ORDER = ['18-24', '25-34', '35-44+']
GENDER_ORDER = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
ATTENDANCE_ORDER = ['Weekly', 'Monthly', 'Every few months']
EXPERIENCE_ORDER = ['0-3', '4-7', '8+']

# Column levels
ROLES = ['Attendee/Raver', 'DJ', 'Producer', 'Event organizer', 'Club staff', 'Other']
TALK_FREQUENCY = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
TALK_REASON = ['Socializing with friends', 'Meeting new people', 'Commenting on the music/performance', 'Other']
TALK_DURATION = ['Just a few words', '1-5 minutes', '>5 minutes']
TALK_PERCEPTION = ['Completely acceptable', 'Somewhat acceptable', 'Neutral', 'Somewhat unacceptable',
                   'Completely unacceptable']

COVID_CHANGE = ['Yes, more talking', 'Yes, less talking', 'No change', 'Unsure']
TALKING_FACTORS = ['Desire for social connection', 'Influence of alcohol or substances', 'Social anxiety',
                   'Changing social norms',
                   'Venue layout (lack of dedicated socializing areas)']

IMPACT_EXPERIENCE = ['Yes, positively', 'Yes, negatively', 'No effect']
IMPACT_DJ = ['Yes, positively', 'Yes, negatively', 'No effect']
IMPACT_ATMOSPHERE = ['Yes, positively', 'Yes, negatively', 'No effect']

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/Dancefloor_taliking.csv')

    # Convert categorical columns to ordered categories
    for col in [COL_AGE, COL_GENDER, COL_ATTENDANCE, COL_EXPERIENCE, COL_TALK_FREQUENCY,
                COL_TALK_DURATION, COL_TALK_PERCEPTION, COL_COVID_CHANGE,
                COL_IMPACT_EXPERIENCE, COL_IMPACT_DJ, COL_IMPACT_ATMOSPHERE]:
        df[col] = pd.Categorical(df[col], categories=get_order(col), ordered=True)

    return df


# Helper function to get the appropriate order for a given column
def get_order(column):
    if column == COL_EXPERIENCE:
        return EXPERIENCE_ORDER
    elif column == COL_AGE:
        return AGE_ORDER
    elif column == COL_GENDER:
        return GENDER_ORDER
    elif column == COL_ATTENDANCE:
        return ATTENDANCE_ORDER
    elif column == COL_TALK_FREQUENCY:
        return TALK_FREQUENCY
    elif column == COL_TALK_DURATION:
        return TALK_DURATION
    elif column == COL_TALK_PERCEPTION:
        return TALK_PERCEPTION
    elif column == COL_COVID_CHANGE:
        return COVID_CHANGE
    elif column == COL_IMPACT_EXPERIENCE:
        return IMPACT_EXPERIENCE
    elif column == COL_IMPACT_DJ:
        return IMPACT_DJ
    elif column == COL_IMPACT_ATMOSPHERE:
        return IMPACT_ATMOSPHERE
    else:
        raise ValueError('No column')

