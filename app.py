"""
Purpose: Q&A application based on uploaded pdf
"""

from dotenv import load_dotenv
import streamlit as st

load_dotenv()
from services.process import store_to_vector_db
from services.pdf_processor import read_data_from_pdf
from services.qa import get_response


def main():
    """
    Main function of application
    """
    st.set_page_config("Ask Me")
    st.header("Ask Me")
    user_question = st.text_input("Question")
    if user_question:
        response = get_response(user_question)
        st.markdown(response)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True,
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                for pdf in pdf_docs:
                    raw_text = read_data_from_pdf(pdf)
                    store_to_vector_db(raw_text)
                st.success("Done")


if __name__ == "__main__":
    main()
