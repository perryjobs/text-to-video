import streamlit as st
from moviepy.editor import * 
import os
from typing import List

def load_video(file):
    return VideoFileClip(file)

def add_typewriter_text(clip, text, duration, fontsize=40, color='white'):
    text_clips = []
    for i in range(1, len(text) + 1):
        t = TextClip(text[:i], fontsize=fontsize, color=color).set_duration(duration / len(text))
        text_clips.append(t)

    # Position the text center-bottom
    composed_text = concatenate_videoclips(text_clips).set_position(('center', 'bottom'))
    final = CompositeVideoClip([clip, composed_text.set_start(0)])
    return final

def merge_videos_with_text(video_files: List[str], text: str):
    clips = [load_video(file) for file in video_files]
    final_clip = concatenate_videoclips(clips)
    final_with_text = add_typewriter_text(final_clip, text, duration=final_clip.duration)
    output_path = "final_output.mp4"
    final_with_text.write_videofile(output_path, codec='libx264')
    return output_path

# Streamlit UI
st.title("📽️ Typewriter Text Video Maker")

uploaded_files = st.file_uploader("Upload video clips", type=["mp4"], accept_multiple_files=True)
text_input = st.text_input("Enter text for typewriter effect")

if st.button("Generate Video") and uploaded_files and text_input:
    with st.spinner("Processing..."):
        temp_paths = []
        for uploaded in uploaded_files:
            temp_path = f"temp_{uploaded.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded.read())
            temp_paths.append(temp_path)

        result = merge_videos_with_text(temp_paths, text_input)

        # Clean up temporary files
        for path in temp_paths:
            os.remove(path)

        st.success("🎉 Video created successfully!")
        st.video(result)
        with open(result, "rb") as file:
            st.download_button("Download Video", file, file_name="output.mp4")
