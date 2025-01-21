import streamlit as st
import cairosvg
import tempfile
import shutil

def convert_svg_to_eps(svg_file):
    """Convert SVG file to EPS using cairosvg"""
    # Create a temporary file for the EPS output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".eps") as tmp_eps_file:
        # Convert SVG to EPS and save it to the temporary file
        cairosvg.svg2eps(url=svg_file, write_to=tmp_eps_file.name)
        return tmp_eps_file.name

def main():
    st.title("SVG to EPS Converter")
    
    st.write("Upload your SVG file to convert it to EPS format.")

    # File uploader for SVG file
    uploaded_file = st.file_uploader("Choose an SVG file", type="svg")
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as tmp_svg_file:
            tmp_svg_file.write(uploaded_file.read())
            svg_file_path = tmp_svg_file.name
        
        # Convert the SVG to EPS
        eps_file_path = convert_svg_to_eps(svg_file_path)

        # Provide a download link for the EPS file
        with open(eps_file_path, "rb") as eps_file:
            st.download_button(
                label="Download EPS file",
                data=eps_file,
                file_name="converted_image.eps",
                mime="application/postscript"
            )

        # Clean up temporary files
        os.remove(svg_file_path)
        os.remove(eps_file_path)

if __name__ == "__main__":
    main()
