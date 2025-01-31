import streamlit as st
import json
import svglottie
from pathlib import Path

def convert_lottie_to_svg(lottie_json):
    try:
        svg_output = svglottie.svglottie(lottie_json)
        return svg_output
    except Exception as e:
        return str(e)

def main():
    st.title("Lottie to SVG Converter")
    st.write("Upload a Lottie JSON file to convert it to SVG animation.")
    
    uploaded_file = st.file_uploader("Upload Lottie JSON", type=["json"])
    
    if uploaded_file is not None:
        try:
            lottie_json = json.load(uploaded_file)
            svg_result = convert_lottie_to_svg(lottie_json)
            
            if isinstance(svg_result, str):
                st.error("Error: " + svg_result)
            else:
                st.success("Conversion Successful!")
                svg_path = Path("output.svg")
                svg_path.write_text(svg_result, encoding="utf-8")
                
                st.download_button(
                    label="Download SVG Animation",
                    data=svg_result,
                    file_name="animation.svg",
                    mime="image/svg+xml"
                )
                
                st.image(svg_path, caption="Converted SVG Animation")
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid Lottie file.")
    
if __name__ == "__main__":
    main()
