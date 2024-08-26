import streamlit as st
import os
import tempfile
from moviepy.editor import VideoFileClip
import random
import graphviz

# Ensure video is retained across pages
if 'video_path' not in st.session_state:
    st.session_state.video_path = None

# Function to handle video upload and saving
def save_uploaded_video(uploaded_video):
    video_path = tempfile.mktemp(suffix=".mp4")  # Use a temporary file
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())
    st.session_state.video_path = video_path
    return video_path

# Custom CSS for Dark Mode and Font
def add_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        .stApp {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
        }
        .title-text {
            font-size: 50px;
            font-weight: bold;
            color: #1DB954;
            text-align: center;
        }
        .subheader-text {
            font-size: 24px;
            color: #b3b3b3;
            text-align: center;
        }
        .upload-button {
            text-align: center;
        }
        .video-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #1c1c1c;
            color: #ffffff;
        }
        h3 {
            color: #1DB954;
        }
        p {
            color: #b3b3b3;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1aab48;
            color: white;
            border: none;
        }
        .stSlider>.st-de { color: #ffffff; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Upload Video to upload video and display video
def main_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>Video Upload and Display</div>", unsafe_allow_html=True)

    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"], help="Supported formats: MP4, MOV, AVI", label_visibility="visible")

    if uploaded_video:
        video_path = save_uploaded_video(uploaded_video)

    if st.session_state.video_path:
        st.markdown("<div class='video-container'>", unsafe_allow_html=True)
        st.video(st.session_state.video_path)
        st.markdown("</div>", unsafe_allow_html=True)

# Page to generate a random clip from the uploaded video
def video_clip_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>Random Video Clip Generator</div>", unsafe_allow_html=True)

    if st.session_state.video_path:
        video_path = st.session_state.video_path
        
        # Display video duration
        with VideoFileClip(video_path) as video:
            duration = video.duration
            st.write(f"Video Duration: {duration:.2f} seconds")

            # Generate random start and end times
            clip_length = 10  # Desired length of the clip in seconds
            start_time = random.uniform(0, max(0, duration - clip_length))
            end_time = start_time + clip_length

            st.write(f"Generated Clip from {start_time:.2f} to {end_time:.2f} seconds")

            if st.button("Generate Random Clip", help="Click to generate and view a random clip"):
                with st.spinner("Processing..."):
                    # Extract and save the clip
                    clip = VideoFileClip(video_path).subclip(start_time, end_time)
                    clip_path = tempfile.mktemp(suffix=".mp4")  # Use a temporary file
                    clip.write_videofile(clip_path, codec="libx264")

                    st.markdown("<div class='video-container'>", unsafe_allow_html=True)
                    st.video(clip_path)
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a video on the Upload Video first.")

# Page to generate topics covered in the video
def topics_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>Topics Covered in the Video</div>", unsafe_allow_html=True)

    if st.session_state.video_path:
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        st.write("Topics detected in the video:")
        topics = [
            "Introduction to Machine Learning",
            "Deep Learning Basics",
            "Neural Networks Explained",
            "Convolutional Neural Networks (CNNs)",
            "Natural Language Processing (NLP)",
            "Reinforcement Learning",
            "AI Ethics and Bias",
            "Future of AI"
        ]
        detected_topics = random.sample(topics, k=3)
        for topic in detected_topics:
            st.markdown(f"- {topic}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a video on the Upload Video first.")

# Page to display the app architecture diagram
def architecture_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>App Architecture Diagram</div>", unsafe_allow_html=True)

    diagram = graphviz.Digraph(comment='App Architecture')

    diagram.attr(style='filled', color='black')
    diagram.attr('node', style='filled', color='#2C3E50', fontcolor='white', shape='box')
    diagram.attr('edge', color='#1DB954')

    diagram.node('A', 'Video Input\n(Upload Video)')
    diagram.node('B', 'Extract Audio')
    diagram.node('C', 'Whisper Model\n(Speech to Text)')
    diagram.node('D', 'Topic Generation\n(TopicBERT)')
    diagram.node('E', 'Summarization')
    diagram.node('F', 'Shorts Creation')

    diagram.edge('A', 'B', label='Extracts audio from video')
    diagram.edge('B', 'C', label='Audio to Text')
    diagram.edge('C', 'D', label='Generates Topics')
    diagram.edge('C', 'E', label='Summarizes Content')
    diagram.edge('C', 'F', label='Creates Shorts')

    st.graphviz_chart(diagram)

# Page to suggest enhancements for the video
def enhancements_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>Video Enhancement Suggestions</div>", unsafe_allow_html=True)

    if st.session_state.video_path:
        with VideoFileClip(st.session_state.video_path) as video:
            duration = video.duration
            st.write(f"Video Duration: {duration:.2f} seconds")
            
            # Example suggestions based on basic analysis
            st.markdown("<div style='background-color: #1c1c1c; padding: 20px; border-radius: 10px; margin-top: 20px;'>", unsafe_allow_html=True)
            st.write("**Suggested Enhancements:**")
            st.write("- **Resolution Improvement:** Ensure your video is recorded in at least 1080p for better quality.")
            st.write("- **Audio Quality:** Use a high-quality microphone for clear audio.")
            st.write("- **Editing:** Trim any unnecessary sections to keep your content engaging.")
            st.write("- **Lighting:** Ensure good lighting to improve video clarity.")
            st.write("- **Content Structure:** Organize content with clear sections and transitions.")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a video on the Upload Video first.")

# Page to provide summarization of the video
def summarization_page():
    st.markdown("<div class='title-text'>REVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-text'>Video Summarization</div>", unsafe_allow_html=True)

    if st.session_state.video_path:
        st.write("Generating summary...")
        
        # Placeholder for actual summarization logic
        summary = "This is a placeholder summary of the video content. Replace this with actual summarization logic using Mistral and LangChain."

        st.markdown(
            "<div style='background-color: #1c1c1c; padding: 20px; border-radius: 10px; margin-top: 20px;'>",
            unsafe_allow_html=True
        )
        st.write("**Video Summary:**")
        st.write(summary)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a video.")

# Sidebar for navigation
def sidebar():
    st.sidebar.title("REVA")
    return st.sidebar.radio("", ["Upload Video", "Generate Short", "Topics Covered", "Architecture Diagram", "Suggestions", "Video Summarization"], index=0)

# Page navigation logic
def main():
    add_custom_css()
    page = sidebar()

    if page == "Upload Video":
        main_page()
    elif page == "Generate Short":
        video_clip_page()
    elif page == "Topics Covered":
        topics_page()
    elif page == "Architecture Diagram":
        architecture_page()
    elif page == "Suggestions":
        enhancements_page()
    elif page == "Video Summarization":
        summarization_page()

if __name__ == "__main__":
    main()
