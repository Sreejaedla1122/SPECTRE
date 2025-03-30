import streamlit as st
import uuid
import shutil
from pathlib import Path
import demo

st.title("SPECTRE: Visual Speech-Aware Perceptual 3D Facial Expression Reconstruction from Videos")

# Upload video file
uploaded_file = st.file_uploader("Upload an MP4 video", type=["mp4"])

if uploaded_file:
    # Generate unique filename
    video_id = str(uuid.uuid4())
    input_path = f"samples/LRS3/{video_id}.mp4"

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(input_path)

    if st.button("Generate Processed Videos"):
        dir_path = Path(Path(input_path).parent, Path(input_path).stem)
        result_shape_file_path = str(dir_path) + '_shape.mp4'
        result_grid_file_path = str(dir_path) + '_grid.mp4'

        if dir_path.exists():
            shutil.rmtree(dir_path)
        if Path(result_shape_file_path).exists():
            Path(result_shape_file_path).unlink()
        if Path(result_grid_file_path).exists():
            Path(result_grid_file_path).unlink()

        # Run processing
        result_shape_path, result_grid_path = demo.main2(input_path=input_path, device="cuda", audio=True)

        # Display output videos
        st.video(result_shape_path)
        st.video(result_grid_path)