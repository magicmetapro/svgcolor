import streamlit as st
from xml.etree import ElementTree as ET

def make_svg_transparent(svg_path, output_path, transparency=0.5):
    # Parse the SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Modify transparency-related attributes
    for elem in root.iter():
        if "opacity" in elem.attrib:
            elem.attrib["opacity"] = str(transparency)
        if "fill-opacity" in elem.attrib:
            elem.attrib["fill-opacity"] = str(transparency)
        if "stroke-opacity" in elem.attrib:
            elem.attrib["stroke-opacity"] = str(transparency)
    
    # Save the modified SVG to a new file
    tree.write(output_path)
    return output_path

# Streamlit interface
st.title("SVG Transparency Modifier")

uploaded_file = st.file_uploader("Upload an SVG file", type="svg")

if uploaded_file:
    # Save the uploaded file temporarily
    input_path = "input.svg"
    output_path = "output_transparent.svg"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # Set transparency level
    transparency = st.slider("Select transparency level", 0.0, 1.0, 0.5)
    
    # Modify SVG transparency
    transparent_svg = make_svg_transparent(input_path, output_path, transparency)
    
    # Display the modified SVG
    st.subheader("Modified SVG with Transparency")
    st.image(transparent_svg)
    
    # Provide a download link
    with open(transparent_svg, "rb") as f:
        st.download_button("Download Transparent SVG", f, file_name="transparent_svg.svg")
