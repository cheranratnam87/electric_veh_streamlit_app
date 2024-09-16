import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URL of the data file
url = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD'

# Load your dataset from the URL
@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# Function to visualize model year by selected states and CAFV eligibility
def visualize_model_year_by_selected_states_and_cafv(df, states, cafv_eligibility):
    # Filter the DataFrame for the selected states and CAFV Eligibility
    filtered_df = df[df['State'].isin(states) & df['CAFV Eligibility'].isin(cafv_eligibility)]

    # Group the data by 'State' and 'Model Year', and count the occurrences
    state_year_counts = filtered_df.groupby(['State', 'Model Year']).size().unstack(fill_value=0)

    # Create a stacked bar plot to visualize the number of vehicles by state and model year
    fig, ax = plt.subplots(figsize=(12,7))
    state_year_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Number of Vehicles by Selected States, Model Year, and CAFV Eligibility')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Vehicles')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Model Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    st.pyplot(fig)  # Display the plot in Streamlit

# Sidebar to select states
selected_states = st.sidebar.multiselect('Select states', df['State'].unique())

if selected_states:
    # Sidebar to select CAFV eligibility (after selecting state)
    unique_cafv = df['CAFV Eligibility'].unique()  # Get unique values in CAFV Eligibility column
    selected_cafv = st.sidebar.multiselect('Select CAFV Eligibility', unique_cafv, default=unique_cafv)

    # Filter the data based on selected states and CAFV eligibility
    filtered_df = df[df['State'].isin(selected_states) & df['CAFV Eligibility'].isin(selected_cafv)]

    # First visualization: Vehicle trends by make
    make_year_counts = filtered_df.groupby(['Make', 'Model Year']).size().unstack(fill_value=0)
    st.write("Vehicle Trends by Make Over the Years")
    st.line_chart(make_year_counts.T)

    # Second visualization: Number of vehicles by state, model year, and CAFV eligibility
    st.write("Number of Vehicles by Selected States, Model Year, and CAFV Eligibility")
    visualize_model_year_by_selected_states_and_cafv(df, selected_states, selected_cafv)
