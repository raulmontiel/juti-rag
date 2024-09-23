# Chatea con PDFs usando Ollama y ChromaDB

### RAG runs offline on local CPU

1. Crear un entorno Virtual:

```
python3 -m venv slrag
source slrag/bin/activate
```
   
3. Instalar requirements: 

```
pip install -r requirements.txt
```

4. Instalar <a href="https://ollama.ai">Ollama</a> ejecutar pull del modelo LLM especificado en config.yml

5. Correr LLama3.1 usando Ollama

```
ollama pull llama3.1
ollama run llama3.1
```

6. Run app.py usando el cliente de Streamlit:

```
streamlit run app.py
```