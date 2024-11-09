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
        Pdf tools is part of a Streamlit project developed by Jaran Gjerland Stenstad, using only chat gpt and an Android phone, to see how far you can can come only using your phone. 
       
        **👈 Select a pdf-tool from the sidebar**
    """
    )


if __name__ == "__main__":
    run()
