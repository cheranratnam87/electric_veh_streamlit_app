import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
def visualize_vehicles_by_make(df, show_top_10=True):
    if show_top_10:
        make_counts = df.groupby('Make').size().nlargest(10)  # Top 10 by default
        title = "Total Number of Vehicles by Top 10 Makes"
    else:
        make_counts = df.groupby('Make').size()  # Show all makes once defaults are changed
        title = "Total Number of Vehicles by Make"
    
    # Create a bar plot with color coding
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=make_counts.index, y=make_counts.values, ax=ax, palette="viridis")

    ax.set_title(title)
    ax.set_xlabel('Make')
    ax.set_ylabel('Total Number of Vehicles')
    
    # Rotate X-axis labels to avoid overlapping
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# Sidebar to select states
all_states = df['State'].unique()
selected_states = st.sidebar.multiselect('Select states', ['Select All'] + list(all_states), default=['Select All'])
if 'Select All' in selected_states:
    selected_states = all_states

# Filter cities based on selected states
filtered_df_for_cities = df[df['State'].isin(selected_states)]
unique_cities = filtered_df_for_cities['City'].unique()

# Sidebar to select City (all cities from selected state(s) are selected by default)
selected_cities = st.sidebar.multiselect('Select City (optional)', ['Select All'] + list(unique_cities), default=['Select All'])
if 'Select All' in selected_cities:
    selected_cities = unique_cities

# Sidebar to select CAFV eligibility
unique_cafv = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique()
selected_cafv = st.sidebar.multiselect('Select CAFV Eligibility (optional)', ['Select All'] + list(unique_cafv), default=['Select All'])
if 'Select All' in selected_cafv:
    selected_cafv = unique_cafv

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
    df['City'].isin(selected_cities) &
    df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(selected_cafv) &
    df['Make'].isin(selected_make) &
    df['Model Year'].isin(selected_model_year)
]

# Determine if default settings are still selected
default_settings = (
    set(selected_states) == set(all_states) and
    set(selected_cities) == set(unique_cities) and
    set(selected_cafv) == set(unique_cafv) and
    set(selected_make) == set(unique_makes) and
    set(selected_model_year) == set(unique_model_years)
)

# If no data is available, display a message
if filtered_df.empty:
    st.write("Oooops ... looks like there is no data with that combination. Be sure a State or States are selected, as that is a requirement to use the dashboards.")
else:
    # First visual: Show top 10 makes by default, or all makes if default settings are modified
    visualize_vehicles_by_make(filtered_df, show_top_10=default_settings)

    # Second visual: Number of vehicles by state, model year, CAFV eligibility, and city
    state_year_counts = filtered_df.groupby(['State', 'Model Year']).size().unstack(fill_value=0)

    # Create a stacked bar plot with color coding
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust the plot size for better mobile experience
    state_year_counts.plot(kind='bar', stacked=True, ax=ax, colormap="viridis")

    ax.set_title('Number of Vehicles by Selected States, Model Year, CAFV Eligibility, and City')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Vehicles')

    # Rotate the x-axis labels to avoid crowding
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    ax.legend(title='Model Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()

    st.pyplot(fig)
