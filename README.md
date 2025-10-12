# EcoMarket-RAG

## Descripción
EcoMarket-RAG es una aplicación de Recuperación Aumentada por Generación (RAG) para consultas inteligentes sobre documentación y datos del dominio EcoMarket. Permite a usuarios hacer preguntas en lenguaje natural y obtener respuestas precisas y citables combinando embeddings vectoriales, búsqueda semántica y modelos LLM. La interfaz está construida con Streamlit para una experiencia rápida y fácil de usar.

## Arquitectura y Diagrama (RAG)
Componentes principales:
- Streamlit (UI): interfaz web para consultas y visualización de resultados/citas.
- LangChain: orquestación de cadenas RAG (embeddings, retrievers, prompts, herramientas).
- Azure Blob Storage: almacenamiento de documentos fuente (PDF/CSV/JSON) y datos de ingesta.
- Pinecone: base vectorial para indexar y recuperar documentos por similitud.
- OpenAI (API): LLM para generación de respuestas y embeddings.

Flujo RAG:
1) Ingesta: Documentos en Azure Blob Storage -> carga/parsing -> generación de embeddings -> upsert a Pinecone.
2) Consulta: Usuario pregunta en Streamlit -> embeddings de la consulta -> retrieve top-k de Pinecone -> re-rank opcional -> LLM de OpenAI genera respuesta con contexto y citas.
3) Observabilidad: logs/trazas de la cadena y métricas básicas de uso.

Diagrama (alto nivel):
[Usuario] → Streamlit UI → LangChain (Chain RAG)
→ Retriever (Pinecone) ← Embeddings (OpenAI)
→ Contexto (de documentos en Azure Blob)
→ LLM (OpenAI) → Respuesta con citas

## Stack Técnico
- Lenguaje: Python 3.10+
- UI: Streamlit
- Orquestación RAG: LangChain
- Vector DB: Pinecone
- Almacenamiento: Azure Blob Storage
- LLMs/Embeddings: OpenAI API
- Testing: pytest
- Logging/Observabilidad: logging estándar de Python, opcionalmente loguru/structlog

## Dependencias principales
- streamlit
- langchain
- openai
- pinecone-client
- azure-storage-blob
- pydantic
- python-dotenv

### Dependencias de soporte (testing y logging)
- pytest
- pytest-asyncio (si aplica)
- requests (para utilidades)
- loguru o structlog (opcional)

Consulta el archivo requirements.txt para versiones exactas.


