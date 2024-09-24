# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
import box
import yaml
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_embedding_model(model_name, normalize_embedding=True, device='cpu'):
    """
    Carga un modelo de embbedings de Hugging Face.

    Argumentos:
        model_name (str): Nombre del modelo de Hugging Face a cargar (por ejemplo, "sentence-transformers/all-mpnet-base-v2").
        normalize_embedding (bool, opcional): Si se deben normalizar las incrustaciones durante la codificación. Por defecto es True.
        device (str, opcional): Dispositivo a usar para la inferencia del modelo (por ejemplo, "cpu" o "cuda"). Por defecto es "cpu".

    Retorna:
        HuggingFaceEmbeddings: El modelo de embbedings cargado.
    """

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={
            'normalize_embeddings': normalize_embedding
        }
    )


def load_retriever(embeddings, store_path, collection_name, vector_space, num_results=1):
    """
    Carga un retriever desde una base de datos de vectores de Chroma.

    Argumentos:
        embeddings (HuggingFaceEmbeddings): El modelo de embbedings a usar para codificar documentos.
        store_path (str): Ruta al directorio donde se persiste la base de datos de vectores.
        collection_name (str): Nombre de la colección dentro de la base de datos de vectores.
        vector_space (str): Tipo de espacio vectorial usado en la colección (por ejemplo, "hnsw").
        num_results (int, opcional): Número de documentos a recuperar por consulta. Por defecto es 1.

    Retorna:
        RetrievalQA: El retriever cargado.
    """

    vector_store = Chroma(collection_name=collection_name,
                          persist_directory=store_path,
                          collection_metadata={"hnsw:space": vector_space},
                          embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": num_results})

    return retriever


def load_prompt_template():
    """
    Carga un objeto PromptTemplate para guiar al modelo de lenguaje grande (LLM) durante la recuperación basada en preguntas y respuestas (QA).

    Retorna:
        PromptTemplate: La plantilla de prompt cargada.
    """

    template = """Usa las siguiente informacion para responder las consultas del usuario.
    Si no encuentras la respuesta, solo di que no se la respuesta, no intentes responder en ese caso.

    Contexto: {context}
    Consulta: {question}

    Devuel solo respuestas utiles a continuacion, y nada mas
    Respuesta:
    """

    prompt = PromptTemplate.from_template(template)

    return prompt


def load_qa_chain(retriever, llm, prompt):
    """
    Carga una cadena de preguntas y respuestas basada en recuperación (RetrievalQA) para realizar QA.

    Argumentos:
        retriever (RetrievalQA): El retriever a usar para recuperar documentos relevantes.
        llm (Ollama): El LLM a usar para responder la pregunta.
        prompt (PromptTemplate): La plantilla de prompt para guiar al LLM.

    Retorna:
        RetrievalQA: La cadena de QA cargada.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )


def build_rag_pipeline():
    
    # Importar variables de configuración
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    print("Cargando Embedding Model...")
    embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS,
                                      normalize_embedding=cfg.NORMALIZE_EMBEDDINGS,
                                      device=cfg.DEVICE)

    print("Cargando BD de Vectores y Retriever...")
    retriever = load_retriever(embeddings,
                               cfg.VECTOR_DB,
                               cfg.COLLECTION_NAME,
                               cfg.VECTOR_SPACE,
                               cfg.NUM_RESULTS)

    print("Cargando Prompt Template...")
    prompt = load_prompt_template()

    print("Cargando Ollama...")
    llm = Ollama(model=cfg.LLM, verbose=False, temperature=0)

    print("Cargando QA Chain...")
    qa_chain = load_qa_chain(retriever, llm, prompt)

    return qa_chain


