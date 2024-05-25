import streamlit as st
from PIL import Image
import numpy as np

def img_proc(img):
    w, h = img.size    
    return f"size: {w}x{h}"

def main():
    st.title("Skincare Shopping Assistant")
    uploaded_img = st.file_uploader(label = 'Upload face image', type=['jpg', 'jpeg', 'png'], accept_multiple_files= False)
    if uploaded_img is not None:
        image = Image.open(uploaded_img)
        
        st.image(image, caption= "Uploaded image", use_column_width= True)
        st.write("")
        st.write("Fetching best skincare recs for ya bestie")
        
        output_text = img_proc(image)
        
        st.text(output_text)
        
if __name__ == "__main__":
    main()
        