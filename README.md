# EcoMarket-RAG
# UNIVERSIDAD ICESI
# MAESTRIA EN  IA APLICADA
# Trabajo IA Generativa -  Caso de Estudio: Optimización de la Atención al Cliente en una Empresa EcoMarket de E-commerce
## Nombres:
#### Carlos Alberto Martinez Ramirez
#### Wilman Andres Quiñonez Valencia

## Descripción
EcoMarket-RAG es una solución de Recuperación Aumentada por Generación (RAG) para consultas inteligentes sobre documentación y datos del dominio EcoMarket. Permite a usuarios hacer preguntas en lenguaje natural y obtener respuestas precisas y citables combinando embeddings vectoriales, búsqueda semántica y modelos LLM. Incluye API con FastAPI y procesamiento de documentos PDF locales y desde Azure Blob Storage.

## Arquitectura y Diagrama (RAG)
**Componentes principales:**
- **FastAPI**: API REST para consultas y gestión de documentos.
- **LangChain**: Orquestación de pipelines RAG (embeddings, retrievers, prompts, chunking).
- **ChromaDB**: Vector store local para desarrollo y pruebas.
- **Azure Blob Storage**: Almacenamiento de documentos fuente (PDF) y datos de ingesta.
- **OpenAI/Azure OpenAI/Hugging Face**: Modelos LLM y embeddings.
- **Loguru**: Logging avanzado.

**Flujo RAG:**
1. **Ingesta**: Documentos PDF locales o desde Azure Blob Storage → chunking → generación de embeddings → indexación en ChromaDB.
2. **Consulta**: Usuario envía pregunta vía API → embeddings de la consulta → recuperación top-k en ChromaDB → LLM genera respuesta con contexto y citas.
3. **Observabilidad**: Logs, métricas y trazas de la cadena.

**Diagrama (alto nivel):**
```
[Usuario/API] → FastAPI → LangChain (RAG Pipeline)
→ Retriever (ChromaDB) ← Embeddings (OpenAI/HuggingFace)
→ Contexto (de documentos locales o Azure Blob)
→ LLM (OpenAI/Azure/HF) → Respuesta con citas
```

## Instalación y Ejecución

### 1. Requisitos previos
- Python 3.10 o superior
- Acceso a Azure Blob Storage (si se usa ingesta remota)
- Claves API de OpenAI/Azure OpenAI (si se usa LLM externo)

### 2. Instalación de dependencias
```bash
pip install -r requirements.txt
```

### 3. Configuración
1. Copia `.env.example` a `.env` y completa tus credenciales y parámetros.
2. Configura los datos de Azure Blob Storage si vas a usar ingesta remota.

### 4. Ejecución de la API
```bash
python main.py
```
La API estará disponible en `http://localhost:8000/docs` (Swagger UI).

### 5. Pruebas unitarias
```bash
pytest
```

## Stack Técnico
- **Lenguaje:** Python 3.10+
- **API:** FastAPI
- **Orquestación RAG:** LangChain
- **Vector DB:** ChromaDB (local)
- **Almacenamiento:** Azure Blob Storage (opcional)
- **LLMs/Embeddings:** OpenAI, Azure OpenAI, Hugging Face Transformers
- **Testing:** pytest, pytest-asyncio
- **Logging:** loguru

## Dependencias principales
- fastapi
- uvicorn
- loguru
- pydantic
- torch
- torchvision
- transformers
- pypdf
- langchain
- langchain_community
- azure-storage-blob
- python-dotenv

### Dependencias de soporte (testing y logging)
- pytest
- pytest-asyncio
- requests
- structlog (opcional)

Consulta el archivo `requirements.txt` para versiones exactas y dependencias adicionales.

## Notas y recomendaciones
- Para ingestar documentos desde Azure Blob Storage, configura correctamente las variables de conexión en `.env` y usa el método `load_and_index_pdfs_from_blob`.
- Puedes personalizar el modelo de embeddings usando Hugging Face (`EmbeddingHuggingFaceService`) o Sentence Transformers.
- La arquitectura permite extender el vector store a Pinecone, Qdrant, etc. para producción.
- Revisa los logs en la carpeta `logs/` para trazabilidad y debugging.

---

Para dudas, revisa la documentación en la carpeta `docs/` o contacta al equipo de EcoMarket.

```plaintext
curl -X 'POST' \
  'http://127.0.0.1:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "¿Que leyes cumple ecomarket para protejer a sus compradores?",
  "top_k": 3,
  "temperature": 0.7
}'

{
  "answer": "Soy el Asistente de Servicio al Cliente. Estoy aquí para informarte sobre nuestra tienda y ayudarte con cualquier otra consulta relacionada con nuestras políticas.\n\nEcoMarket cumple con varias leyes colombianas para proteger a sus compradores y garantizar una experiencia de compra segura y transparente. Entre estas leyes se encuentran:\n\n- Ley 1480 de 2011 – Estatuto del Consumidor Colombiano, que protege los derechos de los consumidores.\n- Ley 527 de 1999 – Comercio electrónico y firmas digitales, que regula las transacciones electrónicas.\n- Ley 1581 de 2012 – Protección de datos personales, que salvaguarda la privacidad de los clientes.\n- Decreto 1074 de 2015 – Decreto Único Reglamentario del Sector Comercio, Industria y Turismo, que establece normativas aplicables al comercio.\n\nEstas normativas respaldan nuestro compromiso con la transparencia, la satisfacción del cliente y el comercio responsable.\n\nFue un gusto proporcionarle la información solicitada, no dude en volver a usar nuestros servicios de Chat Autómatizado. Cordialmente: Servicio al Cliente",
  "sources": [
    {
      "content": "solución conciliada basada en buena fe y comunicación transparente. \nPolítica de compra a proveedores19. Las muestras de producto, cuando sean requeridas, \ndeberán ser proporcionadas sin costo por el ",
      "metadata": {
        "filename": "Politicas_Compra_Proveedores_EcoMarket.pdf",
        "chunk": 5
      }
    },
    {
      "content": "EcoMarket reafirma su compromiso con la transparencia, la satisfacción del cliente y el \ncomercio responsable. Estas políticas buscan asegurar una experiencia de compra con fiable \ny coherente con los",
      "metadata": {
        "filename": "Politicas_Compra_Cliente_EcoMarket.pdf",
        "chunk": 6
      }
    },
    {
      "content": "Políticas de Compra a Proveedores – EcoMarket \nDatos General \nTítulo: Políticas de Compra a Proveedores – EcoMarket \nAutor: Departamento de Abastecimiento y Compras Sostenibles \nFecha: 11/10/2025 \n \nD",
      "metadata": {
        "filename": "Politicas_Compra_Proveedores_EcoMarket.pdf",
        "chunk": 0
      }
    }
  ],
  "confidence": 0.3709913889567057
}
´´´  
