import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Pdf tools",
        page_icon="📄🧰",
    )

    st.write("# PDF TOOLS 📄🧰")

    st.sidebar.success("Select a pdf tool.")

    st.markdown(
    """
    **PDF Tools** is a Streamlit project developed by Jaran Gjerland Stenstad using only ChatGPT and an Android phone. 
    
    Why? I want to stop scrolling and start creating.
    The goal? To see how far you can go with just a mobile device for development—so stop scrolling and dive into the possibilities!

    **👈 Select a PDF tool from the sidebar** or explore individual tools directly:

    - [🔗 Merge PDF](https://pdf-toolkit.streamlit.app/merge_pdf)
    - [🔗 Extract Pages from PDF](https://pdf-toolkit.streamlit.app/PDF_exstract_pages)
    - [🔗 Rotate PDF Pages](https://pdf-toolkit.streamlit.app/Rotate_Pages)
    """
    )


if __name__ == "__main__":
    run()
