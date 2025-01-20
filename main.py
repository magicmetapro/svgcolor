import streamlit as st
import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re

# Fungsi untuk mengganti warna di file SVG
def change_svg_color(svg_path, new_color):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Menangani namespace SVG jika ada
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Regex untuk menemukan berbagai format warna
    color_patterns = [
        r'#[0-9a-fA-F]{6}',        # Hex warna (#RRGGBB)
        r'rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)',  # RGB (rgb(255, 255, 255))
        r'rgba\((\d{1,3}), (\d{1,3}), (\d{1,3}), ([0-9\.]+)\)',  # RGBA (rgba(255, 255, 255, 1))
        r'\b[a-zA-Z]+\b',  # Nama warna (red, blue, etc.)
    ]
    
    # Fungsi untuk mengganti warna berdasarkan format
    def replace_color_in_string(input_string, new_color):
        for pattern in color_patterns:
            input_string = re.sub(pattern, new_color, input_string)
        return input_string

    # Iterasi setiap elemen dan ganti atribut warna yang relevan
    for element in root.iter('path'):  # Hanya iterasi untuk elemen <path>
        # Jika ada atribut 'id', kita dapat mengakses atau memanipulasinya jika diperlukan
        if 'id' in element.attrib:
            path_id = element.attrib['id']
            # Ganti atribut 'fill' atau 'stroke' jika ada
            if 'fill' in element.attrib:
                element.attrib['fill'] = replace_color_in_string(element.attrib['fill'], new_color)
            if 'stroke' in element.attrib:
                element.attrib['stroke'] = replace_color_in_string(element.attrib['stroke'], new_color)
            if 'style' in element.attrib:
                element.attrib['style'] = replace_color_in_string(element.attrib['style'], new_color)

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
