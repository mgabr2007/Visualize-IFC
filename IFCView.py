import streamlit as st
import ifcopenshell
import pyvista as pv

# Define a function to load and convert an IFC file to a PyVista mesh
def load_ifc_file(file_path):
    ifc_file = ifcopenshell.open(file_path)
    mesh = ifc_file.geometry.mesh()
    vertices = mesh.points
    faces = mesh.indices
    return pv.PolyData(vertices, faces)

# Define the Streamlit app
def main():
    st.title("IFC File Viewer")
    file_path = st.file_uploader("Upload an IFC file", type="ifc")
    if file_path is not None:
        st.write("Loading IFC file...")
        mesh = load_ifc_file(file_path.name)
        st.write("Displaying IFC file...")
        pv.set_plot_theme("document")
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="white")
        plotter.show()
        
if __name__ == "__main__":
    main()
