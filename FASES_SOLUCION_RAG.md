
# Fases y Solución del Sistema RAG para EcoMarket

Este documento guía al usuario en la implementación y operación de una solución RAG (Retrieval-Augmented Generation) para EcoMarket, cubriendo desde la selección de componentes hasta la integración y recomendaciones finales.

---

## Fase 1: Selección de Componentes Clave del Sistema de RAG

### 1. Modelo de Embeddings
- **Recomendado:** `text-embedding-3-large` de Azure OpenAI por su precisión multilingüe y facilidad de integración.
- **Alternativas:** Modelos open-source de Hugging Face (`all-MiniLM-L6-v2`, `distiluse-base-multilingual-cased`) para despliegues locales o sin dependencia de servicios propietarios.
- **Consideraciones:** 
La comparación entre all-MiniLM-L6-v2 y text-embedding-3-large revela diferencias notables en precisión, velocidad, recursos y casos de uso ideales.

| Modelo                  | Idiomas soportados                              | Precisión en español       | Notas                                                     |
|--------------------------|------------------------------------------------|----------------------------|-----------------------------------------------------------|
| all-MiniLM-L6-v2         | Inglés, algo de español/francés/árabe           | Buena en textos cortos     | Mejor rendimiento en inglés; existen variantes multilingües |
| text-embedding-3-large   | 100+ (incl. español)                            | Excelente, tareas complejas| Soporte robusto en español y más de 100 idiomas           |

En conclusión, text-embedding-3-large es superior para tareas multilingües y para el procesamiento de textos complejos en cualquier idioma principal, mientras que all-MiniLM-L6-v2 es adecuado para aplicaciones bilingües simples o donde la velocidad y el uso local predominan.

| Modelo                  | Despliegue local | API externa | Infraestructura requerida        |
|--------------------------|------------------|--------------|----------------------------------|
| all-MiniLM-L6-v2         | Sí               | Opcional     | Python, CPU/GPU                  |
| text-embedding-3-large   | No               | Sí           | API Key, acceso OpenAI/Azure     |

En conclusión, all-MiniLM-L6-v2 es óptimo para soluciones privadas y flexibles, mientras que text-embedding-3-large simplifica la integración cloud pero impone dependencia de proveedores externos

### 2. Vector Store
- **Desarrollo local:** ChromaDB por su simplicidad y velocidad.
- **Producción:** Pinecone (API cloud), Qdrant, Weaviate según necesidades de escalabilidad y filtros avanzados.
- **Recomendación:** Para pruebas y prototipos, ChromaDB; para producción, Pinecone o Qdrant.

| Plataforma | Prototipos  | Producción masiva | Facilidad setup   | Escalado y seguridad       |
|------------|-------------|-------------------|-------------------|----------------------------|
| ChromaDB   | Excelente   | Limitada          | Instantáneo       | Básico                     |
| Pinecone   | Adecuado    | Excelente         | Rápido vía SaaS   | Empresarial/SaaS           |
| Qdrant     | Adecuado    | Excelente         | Moderado          | Avanzado/Personalizable    |

En conclusión: ChromaDB acelera prototipado y pruebas locales; Pinecone y Qdrant son recomendados para producción por escalabilidad, features de seguridad, libertad de despliegue y rendimiento robusto.

### 3. Orquestación y Backend
- **LangChain:** Para pipelines de chunking, embeddings, retrieval y prompts.
- **FastAPI:** API REST para consultas y gestión de documentos.
- **Logging:** Loguru para trazabilidad y debugging avanzado.

---

## Fase 2: Creación y Mantenimiento de la Base de Conocimiento

### 1. Identificación y Carga de Documentos
- **Tipos:** PDF (políticas, manuales), CSV/Excel (inventario), JSON (FAQ), Markdown/HTML (guías).
- **Carga:** Local (`docs/`) o remota (Azure Blob Storage). Usa los métodos `load_and_index_pdfs` y `load_and_index_pdfs_from_blob`.

### 2. Limpieza y Segmentación (Chunking)
- **Estrategias:**
    - Chunking recursivo por tamaño/token (ej. 1000 tokens, solapamiento 200).
    - Por párrafos o secciones para preservar sentido semántico.
- **Herramienta:** `RecursiveCharacterTextSplitter` de LangChain.

### 3. Embeddings e Indexación
- **Embeddings:** Genera vectores con Azure OpenAI, Hugging Face o Sentence Transformers.
- **Indexación:** Inserta los chunks y sus embeddings en ChromaDB (o Pinecone/Qdrant en producción), incluyendo metadatos (nombre, tipo, chunk).

### 4. Actualización y Versionado
- **Recomendación:** Versiona los documentos y actualiza el índice periódicamente. Usa metadatos para control de versiones y auditoría.

---

## Fase 3: Integración, Consulta y Pruebas

### 1. Integración API y Frontend
- **API:** FastAPI expone endpoints para consulta (`/query`), salud (`/health`) y administración.
- **Frontend:** Opcionalmente, Streamlit o Gradio para prototipos visuales.

### 2. Flujo de Consulta RAG
1. Usuario envía pregunta vía API.
2. Se genera embedding de la consulta.
3. Se recuperan los chunks más relevantes del vector store.
4. Se construye el prompt y se consulta el LLM (OpenAI/Azure/HF).
5. Se retorna la respuesta con citas y contexto.

### 3. Pruebas y Validación
- **Unitarias:** Usa `pytest` y `pytest-asyncio` para validar ingestión, retrieval y generación.
- **Integración:** Prueba el pipeline completo con documentos de ejemplo.
- **Observabilidad:** Revisa los logs en `logs/` y usa métricas de recuperación y generación.

### 4. Ventajas y limitaciones

- Ventajas
  - Respuestas actualizadas y auditables; reducción de alucinaciones con citación.
  - Control de dominio y cumplimiento normativo si se usa índice privado.
  - Mejora de precisión con recuperación híbrida.

- Limitaciones
  - Dependencia de calidad del corpus y cobertura documental.
  - Coste y latencia por pasos adicionales (recuperación y re-ranking).
  - Riesgos de fuga de información si la gobernanza es débil.

- Mitigaciones
  - Curación continua; monitoreo de métricas RAG; caché de consultas frecuentes.
  - Límite de tokens/contexto y compresión de pasajes.
  - ABAC y segregación de índices por tenant.
---

## Fase 4: Recomendaciones y Buenas Prácticas

- **Seguridad:** Protege las claves API y restringe el acceso a los endpoints sensibles.
- **Escalabilidad:** Para grandes volúmenes, considera vector stores cloud y procesamiento batch.
- **Auditoría:** Versiona los documentos y guarda trazas de consultas y respuestas.
- **Documentación:** Mantén actualizado el README y los ejemplos en la carpeta `docs/`.
- **Extensibilidad:** El sistema permite agregar nuevos loaders, modelos y stores según necesidades futuras.

---

## Ejemplo de Ejecución

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configura `.env` con tus claves y parámetros.
3. Ejecuta la API:
   ```bash
   python main.py
   ```
4. Accede a la documentación interactiva en `http://localhost:8000/docs`.
5. Realiza consultas usando el endpoint `/query`.

---

Para dudas, revisa el README, la carpeta `docs/` o contacta al equipo de EcoMarket.

