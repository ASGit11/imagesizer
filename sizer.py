import streamlit as st
from PIL import Image
import os

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
    converted_file_sizes = {"JPG": {}}
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".png"):
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            input_file = uploaded_file.name
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_file_jpg = f"{base_name}_converted.jpg"
            
            convert_image(input_file, output_file_jpg)
            
            # Store the file sizes
            converted_file_sizes["JPG"][output_file_jpg] = get_file_size_kb(output_file_jpg)
            
            # Display the original and converted images
            st.image(uploaded_file, caption=f"Original PNG: {uploaded_file.name}")
            st.image(output_file_jpg, caption=f"Converted JPEG: {output_file_jpg}")
            
            # Remove the saved files after processing
            os.remove(input_file)
            os.remove(output_file_jpg)
    
    # Print the file sizes of the newly converted images
    st.subheader("Converted Image Sizes (KB)")
    for format_type, sizes in converted_file_sizes.items():
        for file, size in sizes.items():
            st.write(f"{file}: {size:.2f} KB")
