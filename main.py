import streamlit as st
import json
import tempfile
import os
from moviepy.editor import VideoClip
from lottie import parse_lottie
from PIL import Image

def lottie_to_frames(lottie_data, duration=1, fps=30):
    """Konversi animasi Lottie ke daftar frame gambar."""
    animation = parse_lottie(lottie_data)
    frames = []
    for t in range(int(duration * fps)):
        img = animation.render_frame(t / fps)
        frames.append(Image.fromarray(img))
    return frames

def frames_to_video(frames, output_path, fps=30):
    """Konversi daftar frame menjadi video MP4."""
    def make_frame(t):
        frame_index = min(int(t * fps), len(frames) - 1)
        return frames[frame_index]
    
    clip = VideoClip(make_frame, duration=len(frames)/fps)
    clip.write_videofile(output_path, fps=fps, codec='libx264')

st.title("Lottie JSON to MP4 Converter")

uploaded_file = st.file_uploader("Upload Lottie JSON File", type=["json"])

if uploaded_file:
    lottie_data = json.load(uploaded_file)
    st.json(lottie_data)
    
    with st.spinner("Processing animation..."):
        frames = lottie_to_frames(lottie_data, duration=2, fps=30)
        
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        frames_to_video(frames, temp_video.name, fps=30)
        
    st.success("Conversion complete!")
    st.video(temp_video.name)
    
    with open(temp_video.name, "rb") as file:
        st.download_button("Download MP4", file, "animation.mp4", "video/mp4")
