import streamlit as st
from PIL import Image
import os
import zipfile
import io

# Function to convert image to JPEG format
def convert_image(input_path, output_path_jpg):
    img = Image.open(input_path)
    
    # Convert RGBA to RGB if necessary for JPEG
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(output_path_jpg, format="JPEG", quality=100)

# Function to get file size in KB
def get_file_size_kb(file_path):
    return os.path.getsize(file_path) / 1024

# Streamlit App
st.title("PNG to JPEG Converter")

uploaded_files = st.file_uploader("Upload PNG Images", type=["png"], accept_multiple_files=True)

if uploaded_files:
    converted_file_sizes = {"Filename": [], "Size (KB)": []}
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for uploaded_file in uploaded_files:
            if uploaded_file.name.lower().endswith(".png"):
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                input_file = uploaded_file.name
                base_name = os.path.splitext(uploaded_file.name)[0]
                output_file_jpg = f"{base_name}_converted.jpg"
                
                convert_image(input_file, output_file_jpg)
                
                # Store the file sizes
                converted_file_sizes["Filename"].append(output_file_jpg)
                converted_file_sizes["Size (KB)"].append(get_file_size_kb(output_file_jpg))
                
                # Add the converted image to the zip file
                zip_file.write(output_file_jpg)
                
                # Remove the saved files after processing
                os.remove(input_file)
                os.remove(output_file_jpg)
    
    # Display the file sizes in a table
    st.subheader("Converted Image Sizes")
    st.table(converted_file_sizes)
    
    # Provide the zip file for download
    zip_buffer.seek(0)
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name="converted_images.zip",
        mime="application/zip"
    )
