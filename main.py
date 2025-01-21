import streamlit as st
from xml.etree import ElementTree as ET

def make_svg_transparent(svg_path, transparency=0.5):
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
    
    # Serialize the SVG back to a string
    return ET.tostring(root, encoding="unicode")

# Streamlit interface
st.title("SVG Transparency Modifier")

uploaded_file = st.file_uploader("Upload an SVG file", type="svg")

if uploaded_file:
    # Read the uploaded SVG
    input_svg = uploaded_file.read().decode("utf-8")
    
    # Modify SVG transparency
    transparency = st.slider("Select transparency level", 0.0, 1.0, 0.5)
    transparent_svg = make_svg_transparent(uploaded_file, transparency)
    
    # Display the modified SVG using Markdown
    st.markdown(f"<div style='text-align: center;'>{transparent_svg}</div>", unsafe_allow_html=True)
    
    # Provide a download link
    st.download_button("Download Transparent SVG", transparent_svg, file_name="transparent_svg.svg")
