# Required libraries: streamlit, ifcopenshell, matplotlib
# You might need to install them using pip if you haven't already.

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

# Function to visualize the count of building components as a bar chart
def visualize_component_count_bar_chart(component_count):
    labels, values = zip(*sorted(component_count.items(), key=lambda item: item[1], reverse=True))
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_xlabel('Component Types')
    ax.set_ylabel('Count')
    ax.set_title('Count of Different Building Components')
    plt.xticks(rotation=90)
    plt.tight_layout()
    return fig

# Function to visualize the count of building components as a pie chart
def visualize_component_count_pie_chart(component_count):
    labels, sizes = zip(*component_count.items())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.tight_layout()
    return fig

# Streamlit app interface
st.title('IFC File Component Counter')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])

if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    ifc_file = ifcopenshell.open(uploaded_file.name)
    st.write("File successfully uploaded and read. Counting building components:")

    component_count = count_building_components(ifc_file)

    # Display counts of components
    st.write("Counts of Building Components:")
    for component, count in component_count.items():
        st.write(f"{component}: {count}")

    # Visualize component count as a bar chart
    st.write("Bar Chart of Building Components:")
    fig_bar = visualize_component_count_bar_chart(component_count)
    st.pyplot(fig_bar)

    # Visualize component count as a pie chart
    st.write("Pie Chart of Building Components:")
    fig_pie = visualize_component_count_pie_chart(component_count)
    st.pyplot(fig_pie)
    
    # Clean up the uploaded file
    os.remove(uploaded_file.name)
