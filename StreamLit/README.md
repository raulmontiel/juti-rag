# Chatea con PDFs usando Ollama y ChromaDB

Este ejemplo esta basado en el siguiente codigo:

:open_file_folder:[vsingh9076/Building_LLM_Applications](https://github.com/vsingh9076/Building_LLM_Applications)

### RAG Offline en CPU local 

1. Crear un entorno Virtual:

```
python3 -m venv slrag
source slrag/bin/activate
```
   
2. Instalar requerimientos: 

```
pip install -r requirements.txt
```

3. Instalar <a href="https://ollama.ai">Ollama</a> ejecutar pull del modelo LLM especificado en config.yml

4. Correr LLama3.1 usando Ollama

```
ollama pull llama3.1
ollama run llama3.1
```

5. Run app.py usando el cliente de Streamlit:

```
streamlit run app.py
```