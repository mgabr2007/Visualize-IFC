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

# Function to visualize the count of building components
def visualize_component_count(component_count):
    # Sort the dictionary by values (component count)
    sorted_components = sorted(component_count.items(), key=lambda item: item[1], reverse=True)

    # Unpack the items and prepare data for plotting
    labels, values = zip(*sorted_components)

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_xlabel('Component Types')
    ax.set_ylabel('Count')
    ax.set_title('Count of Different Building Components')
    plt.xticks(rotation=90)  # Rotate labels to prevent overlap
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels

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

    # Visualize component count
    fig = visualize_component_count(component_count)
    st.pyplot(fig)
    
    # Clean up the uploaded file
    try:
        os.remove(uploaded_file.name)
    except Exception as e:
        st.write(f"Error removing uploaded file: {e}")
