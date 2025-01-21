import streamlit as st
from PIL import Image
import cairosvg
from io import BytesIO

def convert_svg_to_eps(svg_data):
    # Convert SVG data to EPS format using cairosvg
    eps_output = BytesIO()
    cairosvg.svg2eps(bytestring=svg_data, write_to=eps_output)
    eps_output.seek(0)
    return eps_output

def main():
    st.title("SVG to EPS Converter")

    # File uploader for SVG files
    uploaded_file = st.file_uploader("Upload an SVG file", type="svg")

    if uploaded_file is not None:
        # Display the uploaded SVG file
        st.subheader("Uploaded SVG")
        st.image(uploaded_file, caption="Uploaded SVG", use_column_width=True)

        # Convert SVG to EPS
        try:
            svg_data = uploaded_file.read()
            eps_file = convert_svg_to_eps(svg_data)

            # Provide a download link for the EPS file
            st.success("SVG successfully converted to EPS!")
            st.download_button(
                label="Download EPS file",
                data=eps_file,
                file_name="converted.eps",
                mime="application/postscript",
            )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    main()
