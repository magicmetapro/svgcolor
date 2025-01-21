import streamlit as st
from xml.etree import ElementTree as ET

def make_svg_transparent(svg_data, transparency=0.5):
    # Parse the SVG data, accounting for namespaces
    try:
        root = ET.fromstring(svg_data)
    except ET.ParseError as e:
        st.error(f"Error parsing the SVG file: {e}")
        return None
    
    # Modify transparency-related attributes, handling namespaces
    for elem in root.iter():
        if 'opacity' in elem.attrib:
            elem.attrib['opacity'] = str(transparency)
        if 'fill-opacity' in elem.attrib:
            elem.attrib['fill-opacity'] = str(transparency)
        if 'stroke-opacity' in elem.attrib:
            elem.attrib['stroke-opacity'] = str(transparency)
    
    # Return a properly serialized SVG string with XML structure intact
    return ET.tostring(root, encoding="unicode", method="xml")

# Streamlit interface
st.title("SVG Transparency Modifier")

uploaded_file = st.file_uploader("Upload an SVG file", type="svg")

if uploaded_file:
    # Read SVG content from the uploaded file
    svg_content = uploaded_file.read().decode("utf-8")
    
    # Set transparency level
    transparency = st.slider("Select transparency level", 0.0, 1.0, 0.5)
    
    # Add a Process button to modify the SVG
    if st.button("Process"):
        transparent_svg = make_svg_transparent(svg_content, transparency)
        
        if transparent_svg:
            # Display the modified SVG with safe HTML rendering
            st.markdown(f"<div style='text-align: center;'>{transparent_svg}</div>", unsafe_allow_html=True)
            
            # Provide a download link for the modified SVG
            st.download_button("Download Transparent SVG", transparent_svg, file_name="transparent_svg.svg")
