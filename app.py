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

# Add a headline and tagline with hyperlinks
st.title("Electric Vehicle Population Data")
st.markdown("""
**Dashboard Created by [Cheran Ratnam](https://cheranratnam.com/about/)**  
[Website](https://cheranratnam.com/about/) | [LinkedIn](https://www.linkedin.com/in/cheranratnam/)
""")

# Function to visualize the total number of vehicles by "Make"
def visualize_vehicles_by_make(df):
    make_counts = df.groupby('Make').size()

    # Create a bar plot to visualize the number of vehicles by Make
    fig, ax = plt.subplots(figsize=(10, 6))
    make_counts.plot(kind='bar', ax=ax)
    ax.set_title('Total Number of Vehicles by Make')
    ax.set_xlabel('Make')
    ax.set_ylabel('Total Number of Vehicles')
    
    # Rotate X-axis labels to fit more labels without crowding
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# Sidebar to select states
all_states = df['State'].unique()
selected_states = st.sidebar.multiselect('Select states', ['Select All'] + list(all_states), default=['Select All'])
if 'Select All' in selected_states:
    selected_states = all_states

# Sidebar to select CAFV eligibility
unique_cafv = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique()
selected_cafv = st.sidebar.multiselect('Select CAFV Eligibility (optional)', ['Select All'] + list(unique_cafv), default=['Select All'])
if 'Select All' in selected_cafv:
    selected_cafv = unique_cafv

# Sidebar to select City
unique_cities = df['City'].unique()
selected_cities = st.sidebar.multiselect('Select City (optional)', ['Select All'] + list(unique_cities), default=['Select All'])
if 'Select All' in selected_cities:
    selected_cities = unique_cities

# Sidebar to select Make
unique_makes = df['Make'].unique()
selected_make = st.sidebar.multiselect('Select Make', ['Select All'] + list(unique_makes), default=['Select All'])
if 'Select All' in selected_make:
    selected_make = unique_makes

# Sidebar to select Model Year
unique_model_years = df['Model Year'].unique()
selected_model_year = st.sidebar.multiselect('Select Model Year', ['Select All'] + list(unique_model_years), default=['Select All'])
if 'Select All' in selected_model_year:
    selected_model_year = unique_model_years

# Filter the DataFrame based on user selections
filtered_df = df[
    df['State'].isin(selected_states) &
    df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(selected_cafv) &
    df['City'].isin(selected_cities) &
    df['Make'].isin(selected_make) &
    df['Model Year'].isin(selected_model_year)
]

# If no data is available, display a message
if filtered_df.empty:
    st.write("Oooops ... looks like there is no data with that combination. Be sure a State or States are selected, as that is a requirement to use the dashboards.")
else:
    # First visual: Total number of vehicles by Make (with dynamic filtering)
    visualize_vehicles_by_make(filtered_df)

    # Second visual: Number of vehicles by state, model year, CAFV eligibility, and city
    state_year_counts = filtered_df.groupby(['State', 'Model Year']).size().unstack(fill_value=0)

    # Create a stacked bar plot to visualize the number of vehicles by state and model year
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust the plot size for better mobile experience
    state_year_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Number of Vehicles by Selected States, Model Year, CAFV Eligibility, and City')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Vehicles')

    # Rotate the x-axis labels to avoid crowding
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    ax.legend(title='Model Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()

    st.pyplot(fig)
