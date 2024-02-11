# You need to install the necessary libraries first
# pip install streamlit ifcopenshell matplotlib

import streamlit as st
import ifcopenshell
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Function to count building components
def count_building_components(ifc_file):
    component_count = defaultdict(int)

    for ifc_entity in ifc_file.by_type('IfcProduct'):
        entity_type = ifc_entity.is_a()
        component_count[entity_type] += 1
    
    return component_count

# Function to visualize the count of building components as a pie chart
def visualize_component_count_pie_chart(component_count):
    # Prepare data for plotting
    labels = list(component_count.keys())
    sizes = list(component_count.values())
    
    # Make sure the pie chart fits well into the figure area
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()  # Adjust layout to prevent clipping of labels

    return fig

# Streamlit app interface
st.title('IFC File Component Counter')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])

if uploaded_file is not None:
    # Save uploaded file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Open IFC file with ifcopenshell
    ifc_file = ifcopenshell.open(uploaded_file.name)
    st.write("File successfully uploaded and read. Counting building components:")

    # Count building components
    component_count = count_building_components(ifc_file)
    st.write(component_count)  # Show the count of components in the Streamlit app

    # Visualize component count as a bar chart
    st.write("Bar Chart of Building Components:")
    fig_bar = visualize_component_count(component_count)
    st.pyplot(fig_bar)

    # Visualize component count as a pie chart
    st.write("Pie Chart of Building Components:")
    fig_pie = visualize_component_count_pie_chart(component_count)
    st.pyplot(fig_pie)
    
    # Clean up the uploaded file
    try:
        os.remove(uploaded_file.name)
    except Exception as e:
        st.write(f"Error removing uploaded file: {e}")
