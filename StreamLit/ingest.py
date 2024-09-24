"""
Este script ingiere documentos de texto en una base de datos de vectores para una recuperación eficiente y búsqueda semántica.

Utiliza la biblioteca LangChain para la división de texto, generación de incrustaciones (embeddings), y creación de una base de datos de vectores.
"""

import shutil
import box
import yaml
import warnings
# from langchain.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore deprecated warnings


def run_ingest(documents):
    """
    Ingesta los documentos proporcionados en una base de datos de vectores de LangChain.

    Argumentos:
        documents: Una lista de documentos de texto a ser ingeridos.
    """

    # Cargar las variables de configuración desde un archivo YAML
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    # Dividir el texto en fragmentos manejables para la generación de incrustaciones
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE,
        chunk_overlap=cfg.CHUNK_OVERLAP
    )
    splits = text_splitter.split_text(documents)
    texts = text_splitter.create_documents(splits)
    print(f"Loaded {len(texts)} splits")

     # Crear embbedings usando un modelo de Hugging Face
    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.EMBEDDINGS,
        model_kwargs={'device': cfg.DEVICE},
        encode_kwargs={'normalize_embeddings': cfg.NORMALIZE_EMBEDDINGS}
    )

    # Crear o vaciar la carpeta de la base de datos de vectores
    shutil.rmtree(cfg.VECTOR_DB, ignore_errors=True)
    print(f'{cfg.VECTOR_DB} : Carpeta Borrada')

    # Construir la base de datos de vectores usando Chroma de LangChain
    vector_store = Chroma.from_documents(
        texts,
        embeddings,
        collection_name=cfg.COLLECTION_NAME,
        collection_metadata={"hnsw:space": cfg.VECTOR_SPACE},  # Configure HNSW indexing
        persist_directory=cfg.VECTOR_DB
    )

    print(f"BD de Vectores creada en {cfg.VECTOR_DB}")


if __name__ == "__main__":
    # Ejecutar el proceso de ingestión cuando se ejecute como un script
    run_ingest()


