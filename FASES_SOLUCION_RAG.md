# Documento Explicativo: Fases y Solución del Sistema RAG para EcoMarket


***

## Fase 1: Selección de Componentes Clave del Sistema RAG

**Decisiones arquitectónicas principales:**

### 1. Modelo de Embeddings

- **Elección:** Se selecciona el modelo propietario `text-embedding-3-large` de Azure OpenAI.
- **Justificación:**
    - *Precisión.* Este modelo está entrenado con datos multilingües, ofrece muy buena calidad semántica y soporta preguntas en español, crucial para EcoMarket.
    - *Costo.* Azure OpenAI no requiere infraestructura propia y su precio por 1K tokens es competitivo para escalabilidad.
    - *Idioma español.* Los modelos open-source de Hugging Face como "distiluse-base-multilingual-cased" también funcionan, pero en pruebas prácticas el modelo de Azure OpenAI ofrece mayor retorno semántico y mejor soporte de textos comerciales.
    - *Código abierto vs propietario.* El modelo Azure OpenAI fue preferido por simplicidad de configuración, menor overhead operativo y manejo seguro de claves.


### 2. Base de Datos Vectorial

- **Opciones analizadas:** Pinecone, ChromaDB y Weaviate.
- **Elección:** Pinecone (API en la nube).
- **Ventajas de Pinecone:**
    - *Escalabilidad.* Facilidad de crecimiento horizontal en la nube.
    - *Integración.* Compatible con LangChain y otros frameworks de IA moderna.
    - *Costo.* Plan gratuito para desarrollo; pago por uso en producción.
    - *Desventajas:* Dependencia de proveedor externo, pero mitigada por backups y exportabilidad de índices.
- **Comparativa rápida:**
    - *ChromaDB:* Muy fácil y rápido en local, pero no escala tan bien para producción cloud.
    - *Weaviate:* Permite auto-alojamiento, pero tiene más fricción para empezar, y requeriría DevOps adicional.
    - *Pinecone:* Balance ideal para startups y proyectos académicos/prácticos.

***

## Fase 2: Creación de la Base de Conocimiento de Documentos

### 1. Identificación de Documentos Clave (Ejemplo EcoMarket)

- **Política de Devoluciones** (PDF): Información sobre procesos, plazos y condiciones.
- **Inventario de Productos** (CSV/Excel): Lista de productos, SKU, stock y precios.
- **Preguntas Frecuentes** (JSON): Respuestas estandarizadas sobre envíos, pagos y servicio.


### 2. Segmentación (Chunking)

- **Estrategias comparadas:**
    - *Tamaño fijo:* Divide los documentos en fragmentos de n palabras/tokens (ej: 500 tokens).
    - *Por párrafos:* Separa por saltos de párrafo, útil para preguntas sobre secciones específicas.
    - *Recursiva:* Une pequeños fragmentos hasta alcanzar tamaño deseado, evitando romper el sentido.
- **Estrategia seleccionada:**
    - *Chunk recursivo por tamaño/token y límites semánticos.* Evita cortar frases a la mitad, mejora recuperación y precisión del contexto para la LLM.


### 3. Indexación

- **Flujo:**

1. Los fragmentos/chunks se generan y limpian (remoción de textos irrelevantes).
2. Cada chunk se convierte en embedding usando el modelo seleccionado (Azure OpenAI).
3. Los embeddings, junto al metadata (tipo de documento, referencia), se cargan en Pinecone para búsquedas por similitud.

***

## Fase 3: Integración y Ejecución del Código

### 1. Preparación con LangChain y Streamlit

- *Se usa LangChain para integrar el flujo RAG (retriever, embeddings, prompt construction).* Streamlit provee la interfaz visual para la demo y uso práctico.


### 2. Código

- El repositorio incluye `main.py`, módulos auxiliares para Azure Blob Storage, embeddings en OpenAI, indexación en Pinecone y pruebas unitarias para validar ingestión, retrieval y generación.
- El código del taller ajusta el modelo base para EcoMarket y lo extiende con el pipeline RAG definido:
    - Ingestión de documentos multi-formato
    - Limpieza, chunking y embedding
    - Indexación y consulta semántica
    - Presentación conversacional con logging avanzado


### 3. Limitaciones y Suposiciones

- *Recursos:* La demo utiliza cuentas gratuitas o educativas de Azure/Pinecone/OpenAI; en producción se recomienda escalar según demanda y volumen documental.
- *Suposiciones:*
    - Los documentos subidos a Azure Blob están limpios de datos sensibles.
    - La cantidad de documentos/consultas no sobrepasa el límite de uso de la cuenta gratuita.
    - El modelo de embeddings elegido funciona bien en español conversacional y comercial.
- *Limitaciones posibles:*
    - Si el tamaño de los documentos es muy grande, el chunking y la indexación pueden tardar algunos minutos.
    - La calidad de la respuesta depende de la calidad documental y el prompt engineering; respuestas incorrectas pueden ocurrir si el contexto no fue bien indexado o chunked.
    - El costo de consulta y almacenamiento aumenta con la escala y profundidad de consulta.

***


<div align="center">⁂</div>
[^1]: https://github.com/camartinezolimpiait/EcoMarket-RAG/blob/main/README.md

