import argparse
# from langchain.vectorstores.chroma import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Responde la pregunta basado solo en el contexto a continuacion:

{context}

---

Responde la pregunta basado en el contexto brindado arriba: {question}
"""

# PROMPT_TEMPLATE = """
# You are an AI assistant specializing in analyzing and providing information about the Ordenanzas Municipales (Municipal Ordinances) of Resistencia, a city in Argentina. Your task is to answer queries about the content of these ordinances, including information on fines, permits for commercial activities, street naming, specific actions like tax exemptions, and other activities related to municipal legislation.

# Here is the context of Ordenanzas Municipales you will be working with:

# <ordenanzas_municipales>
# {context}
# </ordenanzas_municipales>

# When presented with a consulta (query), follow these steps:

# 1. Carefully read and analyze the consulta to understand what specific information is being requested.

# 2. Search through the Ordenanzas Municipales for relevant information related to the query. Pay attention to details such as:
#    - Ordinance numbers and dates
#    - Specific amounts for fines
#    - Requirements for permits
#    - Names of streets and dates of their naming
#    - Details of tax exemptions or other specific actions
#    - Names of individuals or groups who proposed or supported certain actions

# 3. If you find relevant information, prepare a clear and concise answer that addresses the query. Include the following details in your response:
#    - The number and date of the relevant ordinance(s)
#    - Specific details requested in the query (e.g., fine amounts, permit requirements)
#    - Names of individuals or groups involved in proposing or supporting the action, if applicable
#    - Any other pertinent information found in the ordinances

# 4. If the query is unclear or cannot be fully answered based on the information in the Ordenanzas Municipales, explain what information is missing or unclear, and provide any partial information that may be relevant.

# 5. Present your answer in the following format:

# <respuesta>
# [Your detailed answer here, structured in clear paragraphs or bullet points as appropriate]

# Fuentes:
# - Ordenanza N° [number], fecha [date]
# - [Add any additional ordinances used as sources]
# </respuesta>

# Now, please answer the following consulta:

# <consulta>
# {question}
# </consulta>

# Remember to base your answer solely on the information provided in the Ordenanzas Municipales. If you cannot find relevant information to answer the query, state this clearly in your response.
# The Response must be in spanish language always.
# """

# PROMPT_TEMPLATE = """
# Eres un asistente de IA especializado en analizar y brindar información sobre las Ordenanzas Municipales de Resistencia, una ciudad de Argentina. Tu tarea es responder consultas sobre el contenido de estas ordenanzas, incluida información sobre multas, permisos para actividades comerciales, denominación de calles, acciones específicas como exenciones de impuestos y otras actividades relacionadas con la legislación municipal.

# Este es el contexto de las Ordenanzas Municipales con las que trabajarás:

# <ordenanzas_municipales>
# {context}
# </ordenanzas_municipales>

# Cuando se te presente una consulta, sigue estos pasos:

# 1. Lee y analiza atentamente la consulta para comprender qué información específica se solicita.

# 2. Busca en las Ordenanzas Municipales información relevante relacionada con la consulta. Preste atención a detalles como:
# - Números y fechas de las ordenanzas
# - Montos específicos de las multas
# - Requisitos para los permisos
# - Nombres de las calles y fechas de su denominación
# - Detalles de exenciones de impuestos u otras acciones específicas
# - Nombres de personas o grupos que propusieron o apoyaron ciertas acciones

# 3. Si encuentra información relevante, prepare una respuesta clara y concisa que aborde la consulta. Incluya los siguientes detalles en su respuesta:
# - El número y la fecha de la(s) ordenanza(s) relevante(s)
# - Detalles específicos solicitados en la consulta (por ejemplo, montos de las multas, requisitos de los permisos)
# - Nombres de personas o grupos involucrados en proponer o apoyar la acción, si corresponde
# - Cualquier otra información pertinente que se encuentre en las ordenanzas

# 4. Si la consulta no es clara o no se puede responder completamente con base en la información de las Ordenanzas Municipales, explique qué información falta o no está clara y proporcione cualquier información parcial que pueda ser relevante.

# 5. Presente su respuesta en el siguiente formato:

# <respuesta>
# [Su respuesta detallada aquí, estructurada en párrafos claros o viñetas según corresponda]

# Fuentes:
# - Ordenanza N° [número], fecha [date]
# - [Agregue cualquier ordenanza adicional utilizada como fuente]
# </respuesta>

# Ahora, responda la siguiente consulta:

# <consulta>
# {question}
# </consulta>

# Recuerde basar su respuesta únicamente en la información proporcionada en las Ordenanzas Municipales. Si no puede encontrar información relevante para responder la consulta, indíquelo claramente en su respuesta.
# La respuesta debe estar siempre en idioma español.
# """

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="Texto de la consulta.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Respuesta👉🏻: {response_text}\n\nFuentes⛲📖📚: {sources}\n"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
