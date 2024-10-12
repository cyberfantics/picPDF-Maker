import streamlit as st
from PIL import Image, ImageEnhance
from fpdf import FPDF
import os

# Function to create a PDF with specified layout options
def create_pdf(image_list, page_size, orientation, margins, margin_color, bg_color):
    pdf = FPDF(orientation=orientation, unit='mm', format=page_size)

    # Set margins
    pdf.set_left_margin(margins['left'])
    pdf.set_right_margin(margins['right'])
    pdf.set_top_margin(margins['top'])
    pdf.set_auto_page_break(auto=True, margin=margins['bottom'])

    # Convert colors from hex to RGB
    margin_color_rgb = tuple(int(margin_color[i:i+2], 16) for i in (1, 3, 5))
    bg_color_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))

    temp_image_paths = []

    for idx, image in enumerate(image_list):
        pdf.add_page()

        # Fill margin color
        pdf.set_fill_color(*margin_color_rgb)
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')

        # Fill background color for the content area
        pdf.set_fill_color(*bg_color_rgb)
        pdf.rect(margins['left'], margins['top'], pdf.w - margins['left'] - margins['right'], pdf.h - margins['top'] - margins['bottom'], 'F')

        img_path = f"temp_image_{idx}.png"
        image.save(img_path)
        temp_image_paths.append(img_path)

        # Layout handling: Only Full Page
        pdf.image(img_path, x=margins['left'], y=margins['top'], w=pdf.w - margins['left'] - margins['right'])

    # Save the PDF as a byte string
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Cleanup: delete temporary image files
    for img_path in temp_image_paths:
        os.remove(img_path)

    return pdf_bytes

# App title and emojis
st.set_page_config(page_title="PicPDF Maker 📄🖼️", page_icon="📄")

# Main Menu
menu = ["Home 🏠", "Convert 📄", "About Us 👨‍💻"]
choice = st.sidebar.selectbox("Main Menu", menu)

# Dark mode toggle
dark_mode = st.sidebar.checkbox("Enable Dark Mode 🌙")

# Apply dark mode styling using custom CSS
if dark_mode:
    st.markdown(
        """
        <style>
        /* General body and background settings */
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
            color: white;
        }
        .stSidebar {
            background-color: #1e1e1e;
            color: white;
        }
        /* Input boxes and widgets */
        .stTextInput > div > input, .stButton > button, .stSelectbox > div > div, .stSlider > div > div {
            background-color: #333;
            color: white;
            border: none;
        }
        /* Text elements */
        .stMarkdown, .stText, .stCaption {
            color: white; /* Ensuring regular text is white */
        }
        h1, .st-emotion-cache-sy3zga {
            color: #FFD700; /* Gold color for better visibility */
        }
        p {
        color:green;
        }
        /* Download button styling */
        .stDownloadButton > button {
            background-color: #1e1e1e;
            color: white;
            border: none;
        }
        /* File uploader styling */
        .stFileUploader > div {
            background-color: #333;
            color: white;
            border: none;
        }
        /* Alert messages */
        .stAlert {
            background-color: #333;
            color: white;
        }
        /* Title and header text */
        .stTitle, .stSidebar > div > div {
            color: white;
        }
        /* Dropdown options */
        .css-1aumxhk {
            background-color: #333;
        }
        /* Page background */
        .css-18e3th9 {
            background-color: #121212;
            color: white;
        }
        /* Checkbox label color */
        .stCheckbox > div > label {
            color: white;
        }
        /* Radio button label color */
        .stRadio > div > label {
            color: white;
        }
        /* Customize select box text */
        .css-19g8g3f {
            color: white;
        }
        h3,h2, .st-bp{
            color: blue;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if choice == "Home 🏠":
    st.title("Welcome to the PicPDF Maker 📄🖼️")
    st.subheader("Convert your images to high-quality PDFs with ease! 🚀")
    st.write("""
        This application allows you to:
        - Upload multiple images in various formats (JPEG, JPG, PNG, GIF, TIFF) 🖼️
        - Edit images by cropping, resizing, and adjusting brightness and contrast 🔧
        - Customize PDF layout options such as page size, orientation, margins, and background colors 📏🎨
        - Download the converted PDF easily 📥
    """)

elif choice == "Convert 📄":
    st.title("PicPDF Maker 📄")
    
    # Image file upload
    uploaded_images = st.file_uploader(
        "Upload Images (JPEG, JPG, PNG, GIF, TIFF)", 
        type=["jpeg", "jpg", "png", "gif", "tiff"], 
        accept_multiple_files=True
    )

    # Page Layout Options
    st.sidebar.header("Page Layout Options 📝")
    page_size = st.sidebar.selectbox("Select Page Size 📐", options=["A4", "Letter"])
    orientation = st.sidebar.selectbox("Select Orientation 🧭", options=["Portrait", "Landscape"])

    # PDF Name Input
    pdf_name = st.sidebar.text_input("Enter PDF File Name 📝", "converted_images.pdf")

    # Margins Adjustment
    margins = {
        'top': st.sidebar.slider("Top Margin (mm)", 0, 200, 10),
        'bottom': st.sidebar.slider("Bottom Margin (mm)", 0, 200, 10),
        'left': st.sidebar.slider("Left Margin (mm)", 0, 20, 10),
        'right': st.sidebar.slider("Right Margin (mm)", 0, 20, 10)
    }

    # Margin Color Selection
    margin_color = st.sidebar.color_picker("Select Margin Color 🎨", "#FFFFFF")
    bg_color = st.sidebar.color_picker("Select Background Color 🎨", "#FFFFFF")

    # Process uploaded images
    if uploaded_images:
        images = []
        for uploaded_image in uploaded_images:
            try:
                image = Image.open(uploaded_image)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                images.append(image)
            except Exception as e:
                st.error(f"Error processing {uploaded_image.name}: {e}")

        # Add a button for conversion
        if st.button("Convert to PDF 📄"):
            pdf_size = 'A4' if page_size == "A4" else 'Letter'
            pdf_orientation = 'P' if orientation == "Portrait" else 'L'
            
            # Create the PDF using the final adjusted images
            pdf_bytes = create_pdf(images, pdf_size, pdf_orientation, margins, margin_color, bg_color)

            # Provide the download button for the PDF
            st.download_button(
                "Download PDF 📥",
                data=pdf_bytes,
                file_name=pdf_name if pdf_name.endswith('.pdf') else f"{pdf_name}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Please upload images (JPEG, JPG, PNG, GIF, TIFF).")

elif choice == "About Us 👨‍💻":
    st.title("About Us 👨‍💻")
    st.image("assets/logo.png", use_column_width=False, width=250, output_format="auto")
 
    st.write("""
        **Developer:** Syed Mansoor ul Hassan Bukhari 💻
        - Passionate about software development and automation 🤖
        - Skilled in Python, web development, and data processing 📊
        - Focused on creating tools that enhance productivity and simplify tasks 🛠️

        Feel free to reach out on [LinkedIn](https://www.linkedin.com/in/mansoor-bukhari-77549a264/) for any inquiries or collaborations! 🤝
    """)
