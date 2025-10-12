# FASES DE LA SOLUCIÓN RAG (EcoMarket-RAG)

Este documento describe, de extremo a extremo, las fases para diseñar, implementar y operar una solución RAG (Retrieval-Augmented Generation) para EcoMarket-RAG. Incluye selección de componentes, construcción de la base de conocimiento, integración y pruebas, ejemplos, ventajas y limitaciones, decisiones arquitectónicas y recomendaciones de documentación.

---

## 1) Selección de componentes

- Modelo generativo (LLM)
  - Local/servidor: Llama 3.x / Mistral 7B/8x7B (vía Ollama o vLLM) para entornos on-prem o bajo costo.
  - API gestionada: OpenAI (gpt-4o/4.1/4-mini), Anthropic (Claude), Azure OpenAI. Pros: simplicidad y rendimiento; Contras: costo, datos fuera de red.
  - Criterios: calidad en español, instrucciones, coste por token, latencia, contexto admitido, políticas de datos.

- Motor de embeddings
  - Opciones: bge-m3, e5-large, text-embedding-3-large, multilingual-e5, jina-embeddings.
  - Criterios: multilingüe, rendimiento en dominio, tamaño de vector, coste, compatibilidad con el vector store.

- Vector store / índice
  - Servicios: Qdrant, Weaviate, Milvus, Elasticsearch/OpenSearch (kNN), Chroma para desarrollo.
  - Criterios: similitud (cosine/dot), filtros, HNSW/IVF, persistencia, backups, gestión de metadatos.

- Orquestación de pipelines
  - LangChain o LlamaIndex para: carga, partición, embeddings, indexado, recuperación híbrida, re-ranking, RAG fusion.
  - Alternativa ligera: pipelines propios con FastAPI + controladores específicos.

- Re-ranking / búsqueda híbrida
  - BM25 + embeddings; opcionalmente re-rankers (e.g., Cohere, bge-reranker, jina-reranker) para mejorar precisión.

- Preprocesamiento de documentos
  - Parsers: pdfplumber, PyPDF2, unstructured, docx2txt, Markdown/HTML loaders.
  - Limpieza y normalización: eliminación de encabezados/pies repetidos, OCR (tesseract) si fuese necesario.

- Aplicación backend y API
  - Framework: FastAPI (Python) por su rendimiento y tipado.
  - Workers: Celery/RQ para tareas batch (ingesta masiva, reindexado).
  - Observabilidad: Prometheus + Grafana, OpenTelemetry traces.

- Frontend
  - Streamlit/Gradio para prototipos; Next.js/React para producción.

- Control de calidad y gobernanza
  - Evaluación: Ragas/ARES para métricas RAG (Recall@k, Faithfulness, Answer Relevancy, Context Precision).
  - Trazabilidad: guardado de prompts, contextos y respuestas (para auditoría y mejora continua).

---

## 2) Base de conocimiento (ingesta y mantenimiento)

- Fuentes de datos
  - Documentos de productos, fichas técnicas, FAQ, políticas, tickets, guías de uso, catálogos.
  - Formatos: PDF, DOCX, XLSX/CSV, Markdown, HTML, JSON, páginas web internas.

- Pipeline de ingesta
  1. Descubrimiento y versionado de fuentes (repos, buckets, URLs).
  2. Extracción con loaders específicos (PDF/HTML/Markdown/CSV).
  3. Limpieza: quitar ruido, normalizar encoding, títulos, tablas a texto estructurado.
  4. Particionado: chunking semántico (por títulos) + límite de tokens (p.ej. 400-800 tokens) con solapamiento 10-20%.
  5. Enriquecimiento de metadatos: título, sección, versión, fecha, etiquetas, idioma, permisos.
  6. Embeddings y almacenamiento en el vector store (batch + reintentos).
  7. Construcción de índices adicionales: BM25, índices por campo, filtros por metadatos.

- Actualizaciones y control de versiones
  - Estrategia upsert con versionado semántico; flags is_latest.
  - Trabajos programados (cron) para refrescar fuentes y detectar cambios por hash.
  - Soft delete + retención para auditoría; política de backups del índice.

- Seguridad y permisos
  - Filtrado a nivel de recuperación por tenant/rol (attribute-based access control) adjuntando claims en metadatos.
  - Cifrado en tránsito (TLS) y en reposo según el vector store.

- Calidad del corpus
  - Deduplicación por similitud; normalización de términos; glosario de sinónimos.
  - Curación manual de contenidos críticos (FAQ y políticas sensibles).

---

## 3) Integración, flujo RAG y pruebas

- Flujo RAG recomendado
  1. Recepción de la consulta del usuario y normalización (detección de idioma, corrección menor, clasificación de intención).
  2. Recuperación híbrida: BM25 + embeddings con filtros por metadatos y top_k inicial (p.ej. 12-20).
  3. Re-ranking de pasajes (top_k re-rankeado a 4-8) con modelo cross-encoder.
  4. Construcción de prompt con instrucciones, estilo, y contextos citables (con fuente, título y enlace/ID).
  5. Llamada al LLM con límites de temperatura y máximo de tokens; activar logprobs si disponible.
  6. Post-procesado: extracción de citas, generación de respuesta estructurada, detección de alucinaciones.
  7. Guardado de la traza: consulta, contextos, respuesta, métricas, feedback del usuario.

- Pruebas automatizadas y de calidad
  - Unitarias: parsers, chunkers, formateadores de prompts, clientes de índice.
  - Integración: pipeline de ingesta end-to-end contra un índice de pruebas.
  - E2E: consultas representativas con oráculos de respuesta; Ragas para puntuar.
  - No funcionales: rendimiento (latencia P95), estrés, coste por consulta, resiliencia ante timeouts.

- Métricas clave
  - Recuperación: Recall@k, MRR, nDCG.
  - Generación: Faithfulness, Answer Relevancy, Context Precision.
  - Producto: CSAT, tasa de clic en citas, tiempo a primera respuesta, costo por sesión.

---

## 4) Ejemplos

- Prompt de sistema (español, EcoMarket)
  "Actúa como asistente de EcoMarket. Responde basado exclusivamente en el contexto proporcionado. Si la información no está en el contexto, indica con claridad que no la tienes y sugiere fuentes internas. Devuelve referencias a las secciones utilizadas."

- Plantilla de prompt
  "Consulta: {question}
  Contexto (máx 8 pasajes):
  {contexts}
  Instrucciones: Responde en español claro y conciso, con viñetas si procede, e incluye citas [#]. Si faltan datos, dilo explícitamente."

- Código de recuperación (ejemplo pseudo-Python)
  ```python
  def retrieve(query, k=16, rerank_k=6):
      docs_bm25 = bm25.search(query, k)
      docs_vec = vectordb.similarity_search(query, k)
      merged = fuse(docs_bm25, docs_vec)  # RAG fusion
      reranked = cross_encoder_rerank(query, merged)[:rerank_k]
      return reranked
  ```

- Esquema de metadatos
  ```json
  {
    "doc_id": "uuid",
    "source": "faq.pdf",
    "title": "Política de Devoluciones",
    "section": "Condiciones",
    "version": "v1.3",
    "lang": "es",
    "created_at": "2025-09-01",
    "tags": ["devoluciones", "políticas"],
    "acl": {"tenant": "default", "roles": ["support", "admin"]}
  }
  ```

---

## 5) Ventajas y limitaciones

- Ventajas
  - Respuestas actualizadas y auditables; reducción de alucinaciones con citación.
  - Control de dominio y cumplimiento normativo si se usa índice privado.
  - Mejora de precisión con recuperación híbrida + re-ranking.

- Limitaciones
  - Dependencia de calidad del corpus y cobertura documental.
  - Coste y latencia por pasos adicionales (recuperación y re-ranking).
  - Riesgos de fuga de información si la gobernanza es débil.

- Mitigaciones
  - Curación continua; monitoreo de métricas RAG; caché de consultas frecuentes.
  - Límite de tokens/contexto y compresión de pasajes.
  - ABAC y segregación de índices por tenant.

---

## 6) Decisiones arquitectónicas (ADR resumidas)

- ADR-001: RAG híbrido (BM25 + embeddings) con re-ranking cross-encoder por mejor precisión sin degradar excesivamente la latencia.
- ADR-002: Qdrant como vector store por su simplicidad, HNSW y filtros robustos. Alternativa: Weaviate administrado.
- ADR-003: bge-m3 para embeddings multilingües y costo/beneficio equilibrado.
- ADR-004: FastAPI + LangChain para rapidez de implementación y mantenibilidad.
- ADR-005: Trazabilidad completa de prompts/contextos para auditoría y evaluación continua.

---

## 7) Sugerencias para la documentación del repo

- README
  - Objetivo del proyecto, arquitectura, diagrama de flujo RAG, cómo ejecutar local y en producción.
  - Variables de entorno y .env.example detallado.

- Carpeta docs/
  - ADRs completos (formato Markdown) y diagramas (Mermaid/PlantUML).
  - Guía de ingesta: cómo agregar nuevas fuentes, tags y permisos.
  - Guía de evaluación: cómo correr Ragas/ARES y leer métricas.

- Ejemplos y notebooks
  - notebooks/ingesta.ipynb, notebooks/evaluacion_rag.ipynb, ejemplos de prompts y consultas típicas.

- Contribución
  - Guia de estilo de código, pruebas, y checklist de PR (evaluación básica de calidad RAG obligatoria).

---

## 8) Operación y despliegue

- Despliegue
  - Docker Compose para desarrollo; Helm/K8s para producción con autoescalado del backend y del índice.
  - Variables: URL del vector store, modelo LLM, llaves API, flags de re-ranking.

- Observabilidad y SRE
  - Tracing de cada petición; dashboards de latencia, recall@k, errores.
  - Alertas por degradación de recall, timeouts, crecimiento anómalo de costes.

- Seguridad
  - Rotación de llaves; registro de accesos; segregación por entorno (dev/stg/prod);
  - DLP básico en prompts y respuestas; sanitización de HTML/Markdown.

---

## 9) Roadmap sugerido

- Fase 1: MVP con RAG híbrido, Qdrant, bge-m3, FastAPI, evaluación Ragas básica.
- Fase 2: Re-ranking avanzado, compresión de contexto, caché semántica, feedback loop.
- Fase 3: Multi-tenant, control fino de permisos, monitoring avanzado, optimización de costes.
- Fase 4: Guardrails de seguridad, detección de PII, workflows de moderación.

---

## 10) Checklist de verificación

- [ ] Fuentes inventariadas y versionadas
- [ ] Ingesta y chunking reproducibles
- [ ] Embeddings generados y validados en muestreo
- [ ] Índices híbridos operativos (BM25 + vector)
- [ ] Re-ranking activado y medido
- [ ] Prompts con citación y políticas de fallback
- [ ] Evaluación RAG automatizada en CI
- [ ] Observabilidad y trazabilidad habilitadas
- [ ] Políticas de seguridad y permisos probadas
- [ ] Documentación actualizada en docs/ y README
