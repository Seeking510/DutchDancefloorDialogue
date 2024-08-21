
import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import load_data, ROLES, IMPACT_DJ, COL_TALK_FREQUENCY, COL_TALK_DURATION, COL_AGE, COL_GENDER, COL_ATTENDANCE, \
    COL_EXPERIENCE, COL_IMPACT_EXPERIENCE, COL_IMPACT_DJ, COL_IMPACT_ATMOSPHERE, COL_TALK_PERCEPTION, TALK_FREQUENCY,\
    TALK_DURATION


def app():
    st.header("Impact of Talking on Experience, DJ Performance, and Atmosphere")
    df = load_data()

    impact_types = {
        "Personal Experience": COL_IMPACT_EXPERIENCE,
        "DJ Performance": COL_IMPACT_DJ,
        "Event Atmosphere": COL_IMPACT_ATMOSPHERE
    }

    # Create columns for pie charts
    cols = st.columns(3)

    for col, (impact_type, column) in zip(cols, impact_types.items()):
        with col:
            st.subheader(f"Impact on {impact_type}")
            counts = df[column].value_counts()
            fig = px.pie(
                values=counts.values,
                names=counts.index
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent',
                hovertemplate="Impact: %{label}<br>Participants: %{value}<br>Percentage: %{percent}"
            )
            st.plotly_chart(fig, use_container_width=True)
    # Function to create heatmap data
    def create_heatmap_data(impact_column):
        impact_categories = IMPACT_DJ  # Assuming all impact columns have the same categories
        heatmap_data = []
        count_data = []
        for category in impact_categories:
            percentages = []
            counts = []
            for role in ROLES:
                role_data = df[df[f'Role_{role}'] == 1]
                count = role_data[impact_column].value_counts().get(category, 0)
                total = len(role_data)
                percentage = (count / total * 100) if total > 0 else 0
                percentages.append(percentage)
                counts.append(count)
            heatmap_data.append(percentages)
            count_data.append(counts)
        return pd.DataFrame(heatmap_data, columns=ROLES, index=impact_categories), pd.DataFrame(count_data, columns=ROLES, index=impact_categories)

    # Create radio buttons for impact selection
    impact_type = st.radio(
        "Select the type of impact to visualize:",
        list(impact_types.keys())
    )

    # Create and display the heatmap based on the selected impact
    st.subheader(f"Impact on {impact_type} by Role")
    heatmap_data, count_data = create_heatmap_data(impact_types[impact_type])

    # Create a text matrix for annotations
    text_matrix = [[f"{heatmap_data.iloc[i, j]:.1f}%" for j in range(heatmap_data.shape[1])] for i in range(heatmap_data.shape[0])]

    fig_heatmap = px.imshow(heatmap_data,
                            labels=dict(x="Role", y="Perceived Impact", color="Percentage"),
                            x=ROLES,
                            y=IMPACT_DJ,  # This assumes all impact columns have the same categories
                            color_continuous_scale="YlOrRd",
                            text_auto=False)  # Disable automatic text

    # Add percentages as text annotations
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            fig_heatmap.add_annotation(
                x=j,
                y=i,
                text=text_matrix[i][j],
                showarrow=False,
                font=dict(color="black" if heatmap_data.iloc[i, j] < 50 else "white")
            )

    # Update hover template to include counts
    fig_heatmap.update_traces(
        hovertemplate="Role: %{x}<br>Perceived Impact: %{y}<br>Percentage: %{z:.1f}%<br>Count: %{text}<extra></extra>",
        text=count_data.values
    )

    fig_heatmap.update_layout(xaxis_title="Role", yaxis_title=f"Perceived Impact on {impact_type}")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.header("Impact Breakdown by Demographic Factor")

    # Create two columns for the radio buttons
    col1, col2 = st.columns(2)

    # Radio button for selecting demographic factor (in the left column)
    with col1:
        demographic_factor = st.radio(
            "Select breakdown factor:",
            ["Talking Frequency", "Talking Duration", "Attendance Frequency", "Experience", "Age", "Gender"],
            key="demographic_factor_impact"
        )

    # Radio button for selecting impact type (in the right column)
    with col2:
        impact_type = st.radio(
            "Select impact type:",
            list(impact_types.keys()),
            key="impact_type"
        )

    # Map the radio button selection to the corresponding column
    demographic_column_map = {
        "Age": COL_AGE,
        "Gender": COL_GENDER,
        "Attendance Frequency": COL_ATTENDANCE,
        "Experience": COL_EXPERIENCE,
        "Talking Frequency": COL_TALK_FREQUENCY,
        "Talking Duration": COL_TALK_DURATION
    }

    selected_demographic_column = demographic_column_map[demographic_factor]
    selected_impact_column = impact_types[impact_type]

    # Calculate percentages and counts
    impact_data = df.groupby(selected_demographic_column)[selected_impact_column].value_counts().unstack(fill_value=0)
    impact_percentages = impact_data.div(impact_data.sum(axis=1), axis=0) * 100
    impact_counts = impact_data

    # Reset index to make the demographic factor a column
    impact_percentages = impact_percentages.reset_index()
    impact_counts = impact_counts.reset_index()

    # Melt the DataFrames to long format for Plotly
    impact_melted = pd.melt(impact_percentages,
                            id_vars=[selected_demographic_column],
                            value_vars=['Yes, positively', 'No effect', 'Yes, negatively'],
                            var_name='Impact',
                            value_name='Percentage')

    counts_melted = pd.melt(impact_counts,
                            id_vars=[selected_demographic_column],
                            value_vars=['Yes, positively', 'No effect', 'Yes, negatively'],
                            var_name='Impact',
                            value_name='Count')

    # Combine percentage and count data
    impact_melted['Count'] = counts_melted['Count']

    # Create the grouped bar chart
    fig = px.bar(impact_melted,
                 x=selected_demographic_column,
                 y='Percentage',
                 color='Impact',
                 barmode='group',
                 title=f'Impact on {impact_type} by {demographic_factor}',
                 labels={selected_demographic_column: demographic_factor},
                 color_discrete_map={'Yes, positively': '#26A69A',
                                     'No effect': '#FFA726',
                                     'Yes, negatively': '#EF5350'},
                 text='Percentage',
                 hover_data=['Count'])

    # Customize the layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend_title_text='Impact',
        xaxis_title=demographic_factor,
        yaxis_title='Percentage',
        yaxis_range=[0, 100]
    )

    # Add gridlines
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

    # Update traces to show percentages on bars and customize hover template
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='inside',
        hovertemplate='%{x}<br>%{y:.1f}% (%{customdata[0]} responses)<extra></extra>'
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add an explanation for people without analytical background
    st.markdown("""
    ### What am I seeing

    This page analyzes how talking on the dancefloor impacts different aspects:

    1. **Overall Impact**: The pie charts show the general impact on personal experience, DJ performance, and event atmosphere.
    2. **Impact by Role**: The heatmap displays how different roles perceive the impact of talking.
    3. **Impact by Demographic Factor**: The bar chart breaks down the impact based on various factors.

    Hover over charts for more detailed information and se the radio buttons to explore different impacts and breakdown factors.
   """)
