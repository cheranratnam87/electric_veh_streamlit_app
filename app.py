import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('rows.csv')

# Function to visualize model year by selected states
def visualize_model_year_by_selected_states(df, states):
    # Filter the DataFrame for the selected states
    filtered_df = df[df['State'].isin(states)]

    # Group the data by 'State' and 'Model Year', and count the occurrences
    state_year_counts = filtered_df.groupby(['State', 'Model Year']).size().unstack(fill_value=0)

    # Create a stacked bar plot to visualize the number of vehicles by state and model year
    fig, ax = plt.subplots(figsize=(12,7))
    state_year_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title('Number of Vehicles by Selected States and Model Year')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Vehicles')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Model Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    st.pyplot(fig)  # Display the plot in Streamlit

# Sidebar to select states
selected_states = st.sidebar.multiselect('Select states', df['State'].unique())

if selected_states:
    filtered_df = df[df['State'].isin(selected_states)]

    # First visualization: Vehicle trends by make
    make_year_counts = filtered_df.groupby(['Make', 'Model Year']).size().unstack(fill_value=0)
    st.write("Vehicle Trends by Make Over the Years")
    st.line_chart(make_year_counts.T)

    # Second visualization: Number of vehicles by state and model year
    st.write("Number of Vehicles by Selected States and Model Year")
    visualize_model_year_by_selected_states(df, selected_states)
