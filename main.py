import streamlit as st
from io import BytesIO
import cairosvg

# Fungsi untuk mengonversi SVG ke EPS
def convert_svg_to_eps(svg_data):
    eps_output = BytesIO()
    cairosvg.svg2eps(bytestring=svg_data, write_to=eps_output)
    eps_output.seek(0)
    return eps_output

# Streamlit App
def main():
    st.title("SVG to EPS Converter")

    # File uploader untuk file SVG
    uploaded_file = st.file_uploader("Upload an SVG file", type="svg")
    if uploaded_file is not None:
        st.subheader("Uploaded SVG File")
        st.image(uploaded_file, caption="Preview SVG", use_column_width=True)

        try:
            # Baca file SVG
            svg_data = uploaded_file.read()
            
            # Konversi ke EPS
            eps_file = convert_svg_to_eps(svg_data)

            # Tampilkan tautan unduh untuk file EPS
            st.success("SVG successfully converted to EPS!")
            st.download_button(
                label="Download EPS file",
                data=eps_file,
                file_name="converted.eps",
                mime="application/postscript",
            )
        except Exception as e:
            st.error(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
