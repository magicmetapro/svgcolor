import streamlit as st
import cairosvg
import os
import zipfile
import tempfile

def convert_svg_to_eps(svg_file_path, output_dir):
    """
    Convert an SVG file to EPS and save it in the specified output directory.
    The output file retains the same name as the SVG file but with an .eps extension.
    """
    # Extract file name without extension
    base_name = os.path.splitext(os.path.basename(svg_file_path))[0]
    eps_file_path = os.path.join(output_dir, f"{base_name}.eps")
    # Convert SVG to EPS
    cairosvg.svg2eps(url=svg_file_path, write_to=eps_file_path)
    return eps_file_path

def main():
    st.title("Bulk SVG to EPS Converter")
    st.write("Upload one or more SVG files to convert them to EPS format. All files will retain their original names with `.eps` extensions.")

    # File uploader for multiple SVG files
    uploaded_files = st.file_uploader("Choose SVG files", type="svg", accept_multiple_files=True)

    if uploaded_files:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as tmp_dir:
            eps_files = []

            # Process each uploaded SVG file
            for uploaded_file in uploaded_files:
                # Save uploaded SVG to a temporary file
                svg_file_path = os.path.join(tmp_dir, uploaded_file.name)
                with open(svg_file_path, "wb") as svg_file:
                    svg_file.write(uploaded_file.read())

                # Convert SVG to EPS
                eps_file_path = convert_svg_to_eps(svg_file_path, tmp_dir)
                eps_files.append(eps_file_path)

            # Create a ZIP file with all converted EPS files
            zip_file_path = os.path.join(tmp_dir, "converted_eps_files.zip")
            with zipfile.ZipFile(zip_file_path, "w") as zipf:
                for eps_file in eps_files:
                    zipf.write(eps_file, os.path.basename(eps_file))

            # Provide the ZIP file for download
            with open(zip_file_path, "rb") as zipf:
                st.download_button(
                    label="Download All EPS Files as ZIP",
                    data=zipf,
                    file_name="converted_eps_files.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
