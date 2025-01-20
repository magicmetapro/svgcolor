import streamlit as st
import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re

# Fungsi untuk mengganti warna di file SVG
def change_svg_color(svg_path, selected_paths, new_color):
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
        if 'id' in element.attrib:
            path_id = element.attrib['id']
            # Ganti warna hanya pada path yang dipilih
            if path_id in selected_paths:
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
        for file in uploaded_files:
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
            svg_path = Path(file.name)
            
            # Memuat file SVG untuk menampilkan semua path
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Menyaring elemen path yang memiliki id
            paths = [element.attrib['id'] for element in root.iter('path') if 'id' in element.attrib]
            
            # Jika ada path yang ditemukan, tampilkan checkbox untuk memilih path
            if paths:
                selected_paths = st.multiselect(
                    "Select Paths to Change Color",
                    options=paths,
                    default=paths  # Secara default pilih semua path
                )
            else:
                st.write("No paths with 'id' found in the SVG.")

            # Color picker untuk memilih warna
            selected_color = st.color_picker("Pick a color", "#FF5733")
            
            # Menampilkan preview warna yang dipilih
            st.write("Selected Color Preview:")
            st.markdown(f'<div style="width: 100px; height: 100px; background-color: {selected_color};"></div>', unsafe_allow_html=True)

            # Button untuk menerapkan warna ke path yang dipilih
            if st.button("Apply Color"):
                st.write("Processing...")
                new_svg_path = change_svg_color(svg_path, selected_paths, selected_color)
                # Tampilkan tombol download untuk file SVG yang telah dimodifikasi
                st.download_button(
                    label="Download Modified SVG",
                    data=open(new_svg_path, "rb").read(),
                    file_name=Path(new_svg_path).name,
                    mime="image/svg+xml"
                )
                # Hapus file setelah diproses
                os.remove(new_svg_path)

if __name__ == "__main__":
    main()
