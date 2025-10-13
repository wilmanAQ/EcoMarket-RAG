
# Documentación Técnica: Módulo `app` - EcoMarket RAG

---

## 1. Estructura del Proyecto

```
app/
├── __init__.py
├── README.md
├── config/
│   └── settings.py
├── rag/
│   ├── embeddings_hugging_face.py
│   ├── embeddings.py
│   ├── generator.py
│   ├── prompts.txt
│   ├── retriever.py
│   └── __pycache__/
```

- **config/**: Configuración global y parámetros del sistema.
- **rag/**: Lógica principal de RAG (embeddings, retrieval, generación, prompts).
- **README.md**: Documentación técnica y guía de uso del módulo.

---

## 2. Arquitectura del Chatbot con IA

### Diagrama General

```
Usuario → FastAPI (main.py) → DocumentRetriever → EmbeddingService → Vector Store (ChromaDB/Pinecone) → LLM (OpenAI/Azure/HF) → Respuesta
```

### Componentes Clave

- **DocumentRetriever** (`rag/retriever.py`):
	- Carga documentos locales y desde Azure Blob Storage.
	- Realiza chunking y limpieza de texto.
	- Indexa los chunks en el vector store.

- **EmbeddingService** (`rag/embeddings_hugging_face.py`, `embeddings.py`):
	- Genera embeddings usando modelos de Hugging Face, OpenAI o Azure OpenAI.
	- Soporta tokenización manual y pooling para mayor control.

- **Generator** (`rag/generator.py`):
	- Construye prompts y consulta el LLM.
	- Gestiona la generación de respuestas y manejo de errores.

- **Prompts** (`rag/prompts.txt`):
	- Plantillas para interacción con el LLM.

- **Config** (`config/settings.py`):
	- Parámetros de conexión, claves API, rutas y settings generales.

---

## 3. Dependencias Técnicas

- **Principales:**
	- `langchain`, `chromadb`, `openai`, `transformers`, `torch`, `azure-storage-blob`, `loguru`, `pypdf`
- **Soporte:**
	- `pytest`, `pytest-asyncio`, `python-dotenv`

---

## 4. Guía de Uso

1. Instala dependencias desde la raíz del proyecto:
	 ```bash
	 pip install -r requirements.txt
	 ```
2. Configura el archivo `.env` con tus claves y parámetros.
3. Ejecuta la API desde la raíz:
	 ```bash
	 python main.py
	 ```
4. Usa los endpoints `/query` para preguntas y `/health` para ver el estado.

---

## 5. Extensión y Personalización

- Puedes agregar nuevos loaders en `rag/` para otros formatos de documentos.
- Modifica los prompts en `prompts.txt` para adaptar el estilo conversacional.
- Cambia el modelo de embeddings en `embeddings_hugging_face.py` según tus necesidades.

---

## 6. Buenas Prácticas

- Mantén las dependencias actualizadas y revisa el archivo `requirements.txt`.
- Protege las claves API y configura los permisos de acceso.
- Versiona los documentos y realiza pruebas unitarias con cada cambio.

---

Para más detalles, consulta el README principal del proyecto o la carpeta `docs/`.
