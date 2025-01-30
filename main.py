import streamlit as st
import json
import base64
import cv2
import numpy as np
import tempfile
import os

def decode_base64_image(encoded_str):
    decoded_data = base64.b64decode(encoded_str)
    np_arr = np.frombuffer(decoded_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def create_video_from_json(json_data, output_path, fps=30):
    frames = [decode_base64_image(frame["image"]) for frame in json_data["frames"]]
    height, width, _ = frames[0].shape
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        video_writer.write(frame)
    
    video_writer.release()

def main():
    st.title("JSON to MP4 Converter")
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
    
    if uploaded_file is not None:
        json_data = json.load(uploaded_file)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
            create_video_from_json(json_data, tmpfile.name)
            tmpfile_path = tmpfile.name
        
        st.video(tmpfile_path)
        
        with open(tmpfile_path, "rb") as file:
            btn = st.download_button(
                label="Download MP4",
                data=file,
                file_name="output.mp4",
                mime="video/mp4"
            )
        
        os.remove(tmpfile_path)

if __name__ == "__main__":
    main()
