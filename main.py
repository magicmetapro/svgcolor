import streamlit as st
import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re

# Fungsi untuk mengganti warna di file SVG
def change_svg_color(svg_path, path_colors):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
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
            if path_id in path_colors:
                new_color = path_colors[path_id]
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
    st.title("SVG Color Batch Changer with Individual Path Color Selection")

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
            
            # Jika ada path yang ditemukan, tampilkan color picker untuk masing-masing path
            if paths:
                path_colors = {}
                for path_id in paths:
                    # Menemukan atribut warna yang sudah ada (fill atau stroke)
                    color = None
                    for element in root.iter('path'):
                        if 'id' in element.attrib and element.attrib['id'] == path_id:
                            if 'fill' in element.attrib:
                                color = element.attrib['fill']
                            elif 'stroke' in element.attrib:
                                color = element.attrib['stroke']
                            break
                    # Jika tidak ada warna, gunakan warna default
                    if color is None:
                        color = '#000000'  # default to black
                    
                    # Tampilkan color picker untuk masing-masing path
                    selected_color = st.color_picker(f"Select color for {path_id}", color)
                    path_colors[path_id] = selected_color

            else:
                st.write("No paths with 'id' found in the SVG.")

            # Button untuk menerapkan warna ke path yang dipilih
            if st.button("Apply Colors"):
                st.write("Processing...")
                new_svg_path = change_svg_color(svg_path, path_colors)
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
