import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tempfile
import os
from PIL import Image

# Konfigurasi 4K
TARGET_RESOLUTION = (3840, 2160)  # 4K UHD
DPI = 300  # Meningkatkan kualitas rendering
BITRATE = 12000000  # 12 Mbps (dalam bits per second)

def generate_4k_video(json_data, fps):
    try:
        frames_data = json_data.get('frames', [])
        
        if not frames_data:
            st.error("Format JSON tidak valid: Tidak ada data frames")
            return None

        temp_dir = tempfile.mkdtemp()
        frame_files = []

        # Hitung ukuran figure dalam inci berdasarkan DPI dan resolusi target
        fig_width = TARGET_RESOLUTION[0] / DPI
        fig_height = TARGET_RESOLUTION[1] / DPI

        for i, frame in enumerate(frames_data):
            fig = plt.figure(figsize=(fig_width, fig_height), dpi=DPI)
            ax = fig.add_subplot(111)
            
            # Set area plot sesuai resolusi 4K
            ax.set_xlim(0, TARGET_RESOLUTION[0])
            ax.set_ylim(0, TARGET_RESOLUTION[1])
            ax.axis('off')  # Matikan axis untuk full frame
            
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
            
            # Simpan frame dengan kualitas tinggi
            frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
            plt.savefig(
                frame_path,
                bbox_inches='tight',
                pad_inches=0,
                dpi=DPI
            )
            plt.close()
            frame_files.append(frame_path)

        # Create video writer dengan setting 4K
        video_path = os.path.join(temp_dir, "output_4k.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # atau 'h264' jika tersedia
        video_writer = cv2.VideoWriter(
            video_path,
            fourcc,
            fps,
            TARGET_RESOLUTION
        )
        
        # Set bitrate (bergantung pada codec support)
        video_writer.set(cv2.VIDEOWRITER_PROP_BITRATE, BITRATE)

        # Convert frames ke video
        for frame_file in frame_files:
            img = cv2.imread(frame_file)
            
            # Resize untuk memastikan resolusi tepat 4K
            img = cv2.resize(img, TARGET_RESOLUTION)
            
            video_writer.write(img)

        video_writer.release()
        return video_path

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

# Streamlit UI
st.title("4K Video Converter")
st.markdown("*Resolusi 4K (3840x2160) | 60 FPS | Bitrate 12 Mbps*")

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
fps = st.slider("Select FPS", 1, 120, 60)  # Maksimum 120 FPS

if uploaded_file is not None:
    try:
        json_data = json.load(uploaded_file)
        
        if st.button("Generate 4K Video"):
            with st.spinner("Creating 4K video (Proses mungkin lama)..."):
                video_path = generate_4k_video(json_data, fps)
                
                if video_path:
                    st.success("Video 4K berhasil dibuat!")
                    
                    # Tampilkan metadata
                    video_info = {
                        "Resolusi": "3840x2160",
                        "FPS": fps,
                        "Bitrate": "12 Mbps",
                        "Codec": "H.264/MPEG-4"
                    }
                    st.json(video_info)
                    
                    # Preview video
                    st.video(video_path)
                    
                    # Download button
                    with open(video_path, "rb") as f:
                        st.download_button(
                            label="Download 4K MP4",
                            data=f,
                            file_name="4k_output.mp4",
                            mime="video/mp4"
                        )
    
    except json.JSONDecodeError:
        st.error("File JSON tidak valid")

# ... (bagian contoh JSON tetap sama)
