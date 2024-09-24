import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from rag.pipeline import build_rag_pipeline
from main import get_rag_response
import timeit
from htmlTemplates import css  # Assuming css contains CSS styles for formatting

from ingest import run_ingest


def get_pdf_text(pdf_docs: list[str]) -> str:
    """
    Extrae el contenido de texto de una lista de documentos PDF.

    Argumentos:
        pdf_docs: Una lista de rutas de archivo o de objetos de datos que representan los documentos PDF.

    Retorna:
        Una cadena de texto que contiene el contenido combinado de todos los PDFs.
    """

    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def handle_userinput(user_question: str) -> None:
    """
    Procesa la entrada del usuario y obtiene una respuesta utilizando una tubería RAG (Generador de Respuestas).

    Argumentos:
        user_question: La pregunta del usuario sobre los documentos subidos.

    Retorna:
        Nada (modifica el estado de la aplicación Streamlit con la respuesta y el tiempo de procesamiento).
    """

    start = timeit.default_timer()

    qa_chain = build_rag_pipeline()
    answer = get_rag_response(user_question, qa_chain)

    end = timeit.default_timer()

    st.write(answer)
    st.markdown(f"**Tiempo tomado en devolver una respuesta:** {end - start:.2f} segundos", unsafe_allow_html=True)


def main() -> None:
    """
    La función principal de la aplicación Streamlit.

    Carga las variables de entorno, configura el diseño de la aplicación Streamlit,
    maneja la interacción con el usuario y procesa los PDFs.
    """

    load_dotenv()
    st.set_page_config(page_title="Chatea con PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)  # Apply CSS styles

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chatea con PDFs :books:")
    user_question = st.text_input("Hacé una pregunta :")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Documentos")
        pdf_docs = st.file_uploader(
            "Subí tus PDFs y hacé click en 'Ingestar'", accept_multiple_files=True)
        if st.button("Ingestar"):
            with st.spinner("Procesando..."):
                # Process PDFs
                raw_text = get_pdf_text(pdf_docs)
                run_ingest(raw_text)


if __name__ == '__main__':
    main()

