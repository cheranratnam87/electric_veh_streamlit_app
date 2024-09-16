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

# Function to visualize model year by selected states, CAFV eligibility, and city
def visualize_model_year_by_selected_filters(df, states, cafv_eligibility, cities):
    # Apply filters
    filtered_df = df[df['State'].isin(states)]
    
    # Further filter by CAFV eligibility if selected
    if cafv_eligibility:
        filtered_df = filtered_df[filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(cafv_eligibility)]
    
    # Further filter by City if selected
    if cities:
        filtered_df = filtered_df[filtered_df['City'].isin(cities)]

    # Group the data by 'State' and 'Model Year', and count the occurrences
    state_year_counts = filtered_df.groupby(['State', 'Model Year']).size().unstack(fill_value=0)

    # Create a stacked bar plot to visualize the number of vehicles by state and model year
    fig, ax = plt.subplots(figsize=(12,7))
    state_year_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Number of Vehicles by Selected States, Model Year, CAFV Eligibility, and City')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Vehicles')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Model Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    st.pyplot(fig)  # Display the plot in Streamlit

# Sidebar to select states
all_states = df['State'].unique()
selected_states = st.sidebar.multiselect('Select states', all_states, default=all_states)

# Show the CAFV Eligibility filter only after state selection
unique_cafv = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique()  # Correct column name
selected_cafv = st.sidebar.multiselect('Select CAFV Eligibility (optional)', unique_cafv)  # No default selection

# Show the City filter only after state selection
unique_cities = df[df['State'].isin(selected_states)]['City'].unique()  # Get cities from the selected states
selected_cities = st.sidebar.multiselect('Select City (optional)', unique_cities)  # No default selection

# First visualization: Vehicle trends by make
filtered_df = df[df['State'].isin(selected_states)]

if selected_cafv:
    filtered_df = filtered_df[filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(selected_cafv)]

if selected_cities:
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

make_year_counts = filtered_df.groupby(['Make', 'Model Year']).size().unstack(fill_value=0)
st.write("Vehicle Trends by Make Over the Years")
st.line_chart(make_year_counts.T)

# Second visualization: Number of vehicles by state, model year, CAFV eligibility, and city
st.write("Number of Vehicles by Selected States, Model Year, CAFV Eligibility, and City")
visualize_model_year_by_selected_filters(df, selected_states, selected_cafv, selected_cities)
