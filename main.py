import streamlit as st
import json
import tempfile
import os
import shutil
from moviepy.editor import VideoFileClip
from lottie.utils import write_lottie_as_gif
import ffmpeg

def convert_lottie_to_mp4(lottie_json, output_path, resolution=(3840, 2160), fps=30):
    temp_gif = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
    write_lottie_as_gif(lottie_json, temp_gif.name)
    
    # Convert GIF to MP4 using ffmpeg
    ffmpeg.input(temp_gif.name).output(output_path, 
                                       vcodec='libx264', 
                                       pix_fmt='yuv420p', 
                                       s=f"{resolution[0]}x{resolution[1]}", 
                                       r=fps).run()
    os.remove(temp_gif.name)

def main():
    st.title("Lottie to MP4 Converter (4K)")
    uploaded_file = st.file_uploader("Upload Lottie JSON file", type=["json"])
    
    if uploaded_file is not None:
        lottie_json = json.load(uploaded_file)
        temp_mp4 = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        
        with st.spinner("Converting to MP4 (4K)..."): 
            convert_lottie_to_mp4(lottie_json, temp_mp4.name)
        
        st.success("Conversion completed!")
        st.video(temp_mp4.name)
        
        st.download_button("Download MP4", data=open(temp_mp4.name, "rb").read(), file_name="lottie_4k.mp4", mime="video/mp4")
        
        os.remove(temp_mp4.name)

if __name__ == "__main__":
    main()
