import streamlit as st
from PIL import Image
import numpy as np
import polars as pl


def img_proc(img):
    w, h = img.size    
    return f"size: {w}x{h}"


def match_according_to_skin_type(products_targets_df, requirements_of_user, serialised_products):
    skin_matches = products_targets_df.filter(
        pl.col("skin type") == requirements_of_user["skin type"]
    )

    all_filtered = skin_matches.filter(
        pl.col("acne") == requirements_of_user["acne"],
        pl.col("dark circles") == requirements_of_user["dark circles"],
        pl.col("acne scarring") == requirements_of_user["acne scarring"],
        pl.col("wrinkles") == requirements_of_user["wrinkles"],
        pl.col("pores") == requirements_of_user["pores"],
    )

    return np.array(serialised_products)[all_filtered["index"].to_numpy()]


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
        