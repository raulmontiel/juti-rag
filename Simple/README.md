# RAG Simple

Este ejemplo esta basado en el siguiente codigo:

:open_file_folder:[pixegami/langchain-rag-tutorial](https://github.com/pixegami/langchain-rag-tutorial)

Adaptado para la charla.

> Recomendacion: Antes de seguir. si desean pueden crear entornos con menv o conda, o su herramienta favorita para no ensuciar sus entornos de desarrollo con distintas versiones de paquetes. **ESTE** es el momento.

```
python3 -m venv simplerag
source simplerag/bin/activate
```

## Instalar los requerimientos
```
pip install -r requirements.txt
```

> Es posible que los requirements esten desactualizados, y tengan que actualizar a versiones actualizadas de los paquetes.

## Crear la base de datos
```
python create_database.py
```

### Limpiar la base de datos
```
python create_database.py --reset
```

## Consultar la base de datos
```
python query_data.py "How does Alice meet the Mad Hatter?"
```
