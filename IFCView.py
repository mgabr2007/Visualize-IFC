# You need to install the necessary libraries first
# pip install streamlit ifcopenshell matplotlib

import streamlit as st
import ifcopenshell
import matplotlib.pyplot as plt
import os

# Function to visualize bounding boxes
def visualize_ifc_bounding_boxes(ifc_file):
    fig, ax = plt.subplots()
    products_found = 0
    boxes_plotted = 0

    for ifc_entity in ifc_file.by_type('IfcProduct'):
        products_found += 1
        st.write(f"Found IfcProduct: {ifc_entity}")  # Print out the IfcProduct for debugging
        if ifc_entity.Representation:
            for representation in ifc_entity.Representation.Representations:
                st.write(f"Found Representation: {representation}")  # Print out the Representation for debugging
                if representation.RepresentationType == 'BoundingBox':
                    for item in representation.Items:
                        if hasattr(item, 'Corner') and hasattr(item, 'XDim') and hasattr(item, 'YDim'):
                            x_min, y_min, z_min = item.Corner.Coordinates
                            x_max = x_min + item.XDim
                            y_max = y_min + item.YDim
                            ax.add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=None, edgecolor='r'))
                            boxes_plotted += 1
                        else:
                            st.write("Representation item does not have the expected attributes.")
                        # Additional debugging to print the item's attributes
                        st.write(f"Item attributes: {dir(item)}")

    # Debugging outputs
    st.write(f"Number of IfcProduct entities found: {products_found}")
    st.write(f"Number of bounding boxes plotted: {boxes_plotted}")

    # Check if there were any boxes plotted, if not, scale axes accordingly
    if boxes_plotted == 0:
        st.write("No bounding boxes found, check the IFC file or representation types.")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    ax.set_aspect('equal', 'box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('IFC Model Bounding Boxes Visualization')
    plt.grid(True)
    return fig

# Streamlit app interface
st.title('IFC File Viewer')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])

if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    ifc_file = ifcopenshell.open(uploaded_file.name)
    st.write("File successfully uploaded and read. Visualizing bounding boxes:")
    
    fig = visualize_ifc_bounding_boxes(ifc_file)
    st.pyplot(fig)
    
    # Clean up the uploaded file
    try:
        os.remove(uploaded_file.name)
    except Exception as e:
        st.write(f"Error removing uploaded file: {e}")
