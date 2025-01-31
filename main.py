import streamlit as st
import json
import tempfile
import os
from lottie import Lottie
from moviepy.editor import VideoClip

def convert_lottie_to_mp4(lottie_json, output_file):
    # Simpan JSON ke file sementara
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_json:
        temp_json.write(json.dumps(lottie_json).encode('utf-8'))
        temp_json_path = temp_json.name

    # Konversi Lottie JSON ke MP4
    lottie = Lottie(temp_json_path)
    lottie.save_as_mp4(output_file)

    # Hapus file JSON sementara
    os.remove(temp_json_path)

def main():
    st.title("Konversi Lottie JSON ke MP4")

    # Unggah file JSON
    uploaded_file = st.file_uploader("Unggah file Lottie JSON", type=["json"])

    if uploaded_file is not None:
        # Baca file JSON
        lottie_json = json.load(uploaded_file)

        # Tampilkan animasi Lottie
        st.write("Animasi Lottie:")
        st.json(lottie_json)

        # Konversi ke MP4
        output_file = "output.mp4"
        convert_lottie_to_mp4(lottie_json, output_file)

        # Tampilkan video MP4
        st.write("Video MP4:")
        st.video(output_file)

        # Tautan unduh video
        with open(output_file, "rb") as file:
            btn = st.download_button(
                label="Unduh MP4",
                data=file,
                file_name=output_file,
                mime="video/mp4"
            )

if __name__ == "__main__":
    main()
