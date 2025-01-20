import streamlit as st
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Fungsi untuk mengubah warna SVG
def change_svg_color(svg_path, new_color):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Iterasi setiap elemen untuk menemukan dan mengganti warna
    for element in root.iter():
        if 'style' in element.attrib:
            element.attrib['style'] = element.attrib['style'].replace('#000000', new_color)  # Default color
        if 'fill' in element.attrib:
            element.attrib['fill'] = element.attrib['fill'].replace('#000000', new_color)  # Default color
    
    # Simpan file SVG yang telah diperbarui
    new_svg_path = svg_path.stem + f"_modified{svg_path.suffix}"
    tree.write(new_svg_path)
    return new_svg_path

# Streamlit app untuk batch mengubah warna SVG
def main():
    st.title("SVG Color Batch Changer with Preview")
    
    # Upload multiple SVG files
    uploaded_files = st.file_uploader("Upload SVG Files", type="svg", accept_multiple_files=True)
    if uploaded_files:
        # Color picker to choose the new color
        selected_color = st.color_picker("Pick a color", "#FF5733")
        
        # Create CSS filter effect preview
        css_filter = f"filter: hue-rotate({selected_color})"
        st.write("CSS Filter:")
        st.code(css_filter, language='css')

        st.write("Selected Color Preview:")
        st.markdown(f'<div style="width: 100px; height: 100px; background-color: {selected_color};"></div>', unsafe_allow_html=True)
        
        # Button for color conversion
        if st.button("Apply Color"):
            st.write("Processing...")
            output_files = []
            
            # Process each uploaded SVG file
            for file in uploaded_files:
                # Save the uploaded file temporarily
                with open(file.name, "wb") as f:
                    f.write(file.getbuffer())
                svg_path = Path(file.name)
                new_svg_path = change_svg_color(svg_path, selected_color)
                output_files.append(new_svg_path)
            
            # Display modified files for download
            for output_file in output_files:
                output_file_name = Path(output_file).name  # Correct way to extract the file name
                st.download_button(
                    label=f"Download {output_file_name}",
                    data=open(output_file, "rb").read(),
                    file_name=output_file_name,
                    mime="image/svg+xml"
                )
                os.remove(output_file)

if __name__ == "__main__":
    main()
