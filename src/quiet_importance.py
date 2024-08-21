import streamlit as st
import plotly.express as px
from src.utils import load_data, COL_AGE, COL_GENDER, COL_ATTENDANCE, \
    COL_EXPERIENCE, COL_QUIET_IMPORTANCE, COL_LIKELIHOOD_INTERVENE

def app():
    df = load_data()
    st.header("Overall Relationship: Quiet Environment Importance vs Intervention Likelihood")

    heatmap_data = df.groupby([COL_QUIET_IMPORTANCE, COL_LIKELIHOOD_INTERVENE]).size().unstack(fill_value=0)

    # Ensure all values from 1 to 5 are present in both axes
    for i in range(1, 6):
        if i not in heatmap_data.index:
            heatmap_data.loc[i] = 0
        if i not in heatmap_data.columns:
            heatmap_data[i] = 0

    # Sort the index and columns
    heatmap_data = heatmap_data.sort_index().sort_index(axis=1)

    # Transpose the data to swap x and y axes
    heatmap_data = heatmap_data.T

    # Calculate percentages
    heatmap_percentages = heatmap_data.div(heatmap_data.sum().sum()) * 100

    # Create the heatmap
    fig = px.imshow(heatmap_data,
                    labels=dict(x="Importance of Quiet Environment", y="Likelihood of Intervention", color="Count"),
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    color_continuous_scale="YlOrRd",
                    aspect="auto")

    # Update layout
    fig.update_layout(
        title="Heatmap: Quiet Environment Importance vs Intervention Likelihood",
        xaxis_title="Importance of Quiet Environment",
        yaxis_title="Likelihood of Intervention",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        yaxis=dict(tickmode='linear', tick0=1, dtick=1)
    )

    # Add text annotations with count and percentage
    for y in heatmap_data.index:
        for x in heatmap_data.columns:
            count = heatmap_data.loc[y, x]
            percentage = heatmap_percentages.loc[y, x]
            fig.add_annotation(
                x=x, y=y,
                text=f"{count}<br>",
                showarrow=False,
                font=dict(color="black" if count < heatmap_data.max().max() / 2 else "white")
            )

    # Update hover template
    fig.update_traces(
        hovertemplate="Importance: %{x}<br>Likelihood: %{y}<br>Count: %{z}<br>Percentage: %{text:.1f}%<extra></extra>",
        text=heatmap_percentages.values
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    avg_importance = df[COL_QUIET_IMPORTANCE].mean()
    avg_likelihood = df[COL_LIKELIHOOD_INTERVENE].mean()
    st.write(f"Average Importance of Quiet Environment: {avg_importance:.2f}")
    st.write(f"Average Likelihood of Intervention: {avg_likelihood:.2f}")

    st.header("Quiet Environment Importance vs Intervention Likelihood by Demographic Factor")

    # Radio button for selecting demographic factor
    demographic_factor = st.radio(
        "Select demographic factor for grouping:",
        ["Age", "Gender", "Attendance Frequency", "Experience"]
    )

    # Map the radio button selection to the corresponding column
    demographic_column_map = {
        "Age": COL_AGE,
        "Gender": COL_GENDER,
        "Attendance Frequency": COL_ATTENDANCE,
        "Experience": COL_EXPERIENCE
    }

    selected_demographic_column = demographic_column_map[demographic_factor]

    # Function to calculate average intervention likelihood
    def avg_intervention_likelihood(group):
        return group[COL_LIKELIHOOD_INTERVENE].mean()

    # Prepare data for the grouped bar chart
    grouped_data = df.groupby([COL_QUIET_IMPORTANCE, selected_demographic_column]).apply(
        avg_intervention_likelihood).unstack()

    # Create the grouped bar chart
    fig = px.bar(grouped_data,
                 barmode='group',
                 labels={'value': 'Average Likelihood of Intervention',
                         'index': 'Importance of Quiet Environment'},
                 title=f'Average Likelihood of Intervention by Quiet Environment Importance and {demographic_factor}')

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Importance of Quiet Environment',
        yaxis_title='Average Likelihood of Intervention',
        legend_title=demographic_factor,
        xaxis={'tickmode': 'linear', 'tick0': 1, 'dtick': 1}
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="Importance: %{x}<br>Average Likelihood: %{y:.2f}<br>%{fullData.name}<extra></extra>"
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add explanation for people without analytical background
    st.markdown("""
    ### What am I seeing?

    This page examines the relationship between the importance of a quiet environment and the likelihood of intervention.

    1. **Heatmap**: 
       - The x-axis shows how important a quiet environment is to participants (1 = not important, 5 = very important).
       - The y-axis shows how likely participants are to intervene if a conversation it's disturbing to them (1 = unlikely, 5 = very likely).
       - Darker colors indicate more participants in that category.
       - Hover over cells to see exact counts and percentages.

    2. **Average Values**:
       - These show the overall tendency of participants regarding quiet environment importance and intervention likelihood.

    3. **Grouped Bar Chart**:
       - This breaks down the relationship by demographic factors.
       - The x-axis shows the importance of a quiet environment.
       - The y-axis shows the average likelihood of intervention.
       - Different colors represent different demographic groups.
       - Use the radio button to explore different demographic factors.

    """)