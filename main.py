import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tempfile
import os
from PIL import Image

def generate_video_from_json(json_data, fps):
    try:
        # Parse JSON data
        frames_data = json_data.get('frames', [])
        
        if not frames_data:
            st.error("Format JSON tidak valid: Tidak ada data frames")
            return None

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        frame_files = []

        # Generate frames
        for i, frame in enumerate(frames_data):
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            # Plot background
            ax.set_facecolor('white')
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.set_title(f"Frame {i+1}")

            # Plot shapes
            for shape in frame.get('shapes', []):
                if shape['type'] == 'circle':
                    circle = plt.Circle(
                        (shape['x'], shape['y']),
                        shape['radius'],
                        color=shape.get('color', 'blue'),
                        alpha=shape.get('alpha', 1.0)
                    )
                    ax.add_patch(circle)
            
            # Save frame to image
            frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
            plt.savefig(frame_path)
            plt.close()
            frame_files.append(frame_path)

        # Create video from frames
        if not frame_files:
            st.error("Tidak ada frame yang dihasilkan")
            return None

        # Get frame dimensions from first image
        first_image = cv2.imread(frame_files[0])
        height, width, _ = first_image.shape

        # Create video writer
        video_path = os.path.join(temp_dir, "output.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        # Write frames to video
        for frame_file in frame_files:
            img = cv2.imread(frame_file)
            video_writer.write(img)

        video_writer.release()
        return video_path

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

# Streamlit UI
st.title("JSON to MP4 Converter")

# File upload
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

# FPS selection
fps = st.slider("Select FPS", min_value=1, max_value=60, value=24)

if uploaded_file is not None:
    try:
        # Load JSON data
        json_data = json.load(uploaded_file)
        
        # Generate video
        if st.button("Generate Video"):
            with st.spinner("Creating video..."):
                video_path = generate_video_from_json(json_data, fps)
                
                if video_path:
                    st.success("Video created successfully!")
                    
                    # Show preview
                    st.video(video_path)
                    
                    # Download button
                    with open(video_path, "rb") as f:
                        st.download_button(
                            label="Download MP4",
                            data=f,
                            file_name="output.mp4",
                            mime="video/mp4"
                        )
    
    except json.JSONDecodeError:
        st.error("File tidak valid. Harap upload file JSON yang valid.")

# Contoh struktur JSON
st.subheader("Contoh Struktur JSON")
st.code("""{
    "frames": [
        {
            "shapes": [
                {
                    "type": "circle",
                    "x": 20,
                    "y": 50,
                    "radius": 10,
                    "color": "red",
                    "alpha": 0.8
                }
            ]
        },
        {
            "shapes": [
                {
                    "type": "circle",
                    "x": 40,
                    "y": 50,
                    "radius": 10,
                    "color": "blue",
                    "alpha": 0.8
                }
            ]
        }
    ]
}""")

st.write("""
*Instruksi:*
1. Upload file JSON dengan struktur seperti contoh di atas
2. Sesuaikan FPS sesuai kebutuhan
3. Klik tombol "Generate Video"
4. Setelah proses selesai, video akan muncul dan bisa di-download
""")
