# Fases y Solución del Sistema RAG para EcoMarket

Este documento guía al usuario en la implementación y operación de una solución RAG (Retrieval-Augmented Generation) para EcoMarket, cubriendo desde la selección de componentes hasta la integración y recomendaciones finales.

# 🧩 Fase 1: Selección de Componentes Clave del Sistema RAG  

## 1. Modelo de Embeddings  

### 🧠 Contexto general  

En el desarrollo del **Sistema RAG (Retrieval-Augmented Generation)** para **EcoMarket**, el modelo de *embeddings* es el núcleo semántico del sistema.  
Su función es transformar los documentos oficiales de la empresa —**Política de Garantía**, **Política de Devolución**, **Política de Compra del Cliente** y **Política de Proveedores**— en **vectores numéricos** que representen su significado.  

Estos vectores permiten que el sistema identifique la similitud entre preguntas y fragmentos de texto, de modo que, cuando un cliente realiza una consulta, el asistente de IA pueda **recuperar los fragmentos más relevantes** antes de generar la respuesta final.  

---

### 🔹 Modelo seleccionado: `all-MiniLM-L6-v2`  

El modelo **`all-MiniLM-L6-v2`** fue seleccionado como la base para el sistema RAG de EcoMarket debido a su excelente **relación entre rendimiento, costo y eficiencia**.  
Pertenece a la familia **Sentence Transformers** (Microsoft + Hugging Face), optimizado para tareas de búsqueda semántica, clasificación y recuperación de información (*semantic search*).  

#### ✳️ Características técnicas  

- **Tipo:** Open Source (gratuito).  
- **Dimensionalidad del embedding:** 384.  
- **Arquitectura:** Transformer compacto, entrenado en tareas de similitud de oraciones y *paraphrase mining*.  
- **Tamaño:** Ligero (~80 MB), permite inferencia rápida en CPU o GPU de bajo costo.  
- **Compatibilidad:** Funciona localmente con librerías como **ChromaDB**, **FAISS** o **LanceDB**.  

#### 💡 Ventajas  

1. **Costo nulo y libre acceso:** No requiere conexión a APIs de pago.  
2. **Alta eficiencia:** Velocidad de procesamiento elevada, ideal para entornos locales.  
3. **Privacidad:** Los documentos empresariales permanecen dentro del entorno de la organización.  
4. **Facilidad de integración:** Compatible con frameworks de IA abiertos y bases vectoriales locales.  

#### ⚠️ Limitaciones  

- Menor precisión semántica en textos legales o complejos.  
- Soporte parcial en español (aunque aceptable con preprocesamiento adecuado).  
- Embeddings de menor densidad comparados con modelos de última generación.  

---

### 🔹 Modelo de comparación: `text-embedding-3-large` (OpenAI)  

**`text-embedding-3-large`** es un modelo propietario desarrollado por **OpenAI**, considerado uno de los más avanzados del mercado.  
Es parte de la tercera generación de embeddings optimizados para **RAG, clasificación y búsqueda semántica multilingüe**.  

#### ✳️ Características técnicas  

- **Tipo:** Propietario (API en la nube).  
- **Dimensionalidad:** 3,072.  
- **Entrenamiento:** En corpus multilingües (más de 40 idiomas, incluyendo español).  
- **Diseño:** Pensado para integración directa con modelos GPT (GPT-4, GPT-4o, GPT-5).  
- **Optimización:** Alta precisión semántica, reducción de alucinaciones y excelente manejo de consultas ambiguas.  

#### 💡 Bondades principales  

1. **Alta precisión contextual:** Capta matices, sinónimos y relaciones semánticas profundas.  
2. **Multilingüe real:** Entiende y representa correctamente textos en español, inglés y otros idiomas.  
3. **Integración nativa con GPT:** Permite coherencia entre *retrieval* y *generation*.  
4. **Escalabilidad:** Ideal para implementaciones cloud con alto tráfico de consultas.  
5. **Menor riesgo de errores o alucinaciones** en las respuestas generadas.  

#### ⚠️ Limitaciones  

- **Costo por uso:** Factura por cada mil tokens procesados.  
- **Dependencia externa:** Requiere conexión a API y cumplimiento de políticas de privacidad.  
- **Mayor latencia:** Las consultas viajan a servidores externos.  

---

### 🔹 Comparación técnica entre ambos modelos  

| **Criterio** | **`all-MiniLM-L6-v2` (Hugging Face)** | **`text-embedding-3-large` (OpenAI)** |
|--------------|----------------------------------------|---------------------------------------|
| **Tipo de modelo** | Open Source | Propietario |
| **Dimensión del vector** | 384 | 3,072 |
| **Tamaño del modelo** | ~80 MB | ~1.5 GB (en servidores) |
| **Entrenamiento multilingüe** | Parcial | Extenso (40+ idiomas) |
| **Precisión semántica** | Buena | Muy alta |
| **Velocidad de inferencia** | Muy alta (local) | Media (API) |
| **Costo de uso** | Gratuito | Pago por tokens |
| **Privacidad** | Total (local) | Parcial (en la nube) |
| **Integración con RAG** | Manual con frameworks open-source | Nativa con modelos GPT |
| **Soporte en español** | Aceptable | Excelente |
| **Escalabilidad** | Limitada al entorno local | Alta, infraestructura cloud |
| **Uso recomendado** | Fase de desarrollo o educativa | Producción empresarial |
| **Proveedor** | Hugging Face / Microsoft | OpenAI / Azure OpenAI |

---

### 🔹 Conclusión y decisión de selección  

Para el **prototipo del sistema RAG de EcoMarket**, se seleccionó **`all-MiniLM-L6-v2`** debido a que:  

1. **No genera costos por uso** y permite trabajar sin dependencia de servicios externos.  
2. **Procesa los documentos PDF institucionales** de manera eficiente en español, con resultados adecuados para búsqueda semántica.  
3. **Facilita la experimentación y desarrollo local** sin comprometer la privacidad de los datos.  

No obstante, se reconoce que **`text-embedding-3-large`** es una opción **más robusta para entornos productivos**, recomendada para futuras fases del proyecto donde se busque **mayor precisión, escalabilidad y soporte multilingüe avanzado**.  

---

## 2. Base de Datos Vectorial  

### 🧮 Contexto  

Una vez generados los embeddings, estos deben almacenarse en una **base de datos vectorial**, que permita realizar **búsquedas por similitud** de manera eficiente.  
En el caso del sistema RAG de **EcoMarket**, la base vectorial es el componente encargado de **indexar, recuperar y ordenar** los fragmentos de los documentos relevantes para responder a las consultas de los clientes.  

A continuación se analizan tres opciones principales: **Pinecone**, **ChromaDB** y **Weaviate**.

---

### 🔹 Comparación de bases de datos vectoriales  

| **Criterio** | **Pinecone** | **ChromaDB** | **Weaviate** |
|---------------|---------------|---------------|---------------|
| **Tipo de licencia** | SaaS (propietaria, nube) | Open Source | Open Source / Cloud híbrido |
| **Modo de despliegue** | Cloud (API) | Local o nube | Local y Cloud (modular) |
| **Costo** | Pago por uso (según volumen de vectores) | Gratuito | Gratuito (local), pago en cloud |
| **Escalabilidad** | Muy alta (nube administrada) | Limitada (depende del hardware local) | Alta (soporta escalado distribuido) |
| **Facilidad de uso** | Muy alta (SDK y API simples) | Muy alta (instalación rápida en Python) | Media (mayor configuración inicial) |
| **Persistencia de datos** | Total (administrada por Pinecone) | Parcial (requiere configuración manual) | Total (almacenamiento persistente integrado) |
| **Integración con RAG** | Excelente con OpenAI y LangChain | Excelente con LangChain y Hugging Face | Compatible con OpenAI, LangChain y Transformers |
| **Requerimientos de infraestructura** | Ninguno (100% nube) | Requiere almacenamiento local | Requiere servidor o contenedor |
| **Privacidad** | Datos en servidores externos | Control local total | Control local o híbrido |
| **Rendimiento** | Alto y estable (nube optimizada) | Alto en entornos pequeños | Muy alto en entornos distribuidos |
| **Ideal para** | Producción empresarial en la nube | Fases de desarrollo, pruebas, educación | Soluciones escalables híbridas o empresariales |

---

### 🔹 Decisión para EcoMarket  

Para la **fase actual de desarrollo**, se eligió **ChromaDB** como base vectorial principal por las siguientes razones:

1. **Código abierto y gratuito**, lo que permite su uso en entornos académicos y locales sin costos adicionales.  
2. **Integración nativa con LangChain y Hugging Face**, facilitando el flujo entre embeddings, búsqueda y generación de respuestas.  
3. **Simplicidad de implementación**, ideal para prototipos funcionales y pruebas rápidas.  
4. **Control total de datos**, garantizando privacidad sobre los documentos internos de EcoMarket.  

No obstante, para una **futura implementación en producción**, **Pinecone** y **Weaviate** se consideran opciones más adecuadas debido a su **mayor escalabilidad, monitoreo y administración de carga en tiempo real**.  

---

### 🔹 Conclusión general  

| **Componente** | **Selección actual (Fase de desarrollo)** | **Alternativa recomendada (Fase de producción)** |
|----------------|--------------------------------------------|------------------------------------------------|
| **Modelo de Embeddings** | `all-MiniLM-L6-v2` (Hugging Face) | `text-embedding-3-large` (OpenAI) |
| **Base de Datos Vectorial** | `ChromaDB` (local, open-source) | `Pinecone` o `Weaviate` (cloud escalables) |

---

### ✅ Resumen  

El sistema RAG de **EcoMarket** combina la **eficiencia local del modelo `all-MiniLM-L6-v2`** con la **simplicidad de implementación de ChromaDB**, logrando un prototipo funcional, seguro y económico.  
Esta arquitectura equilibra **rendimiento, costo y control de datos**, sentando las bases para una futura migración hacia un entorno de producción más robusto con **OpenAI embeddings y bases vectoriales en la nube**.  

# 🧩 Fase 2: Creación de la Base de Conocimiento de Documentos  

El éxito del sistema **RAG (Retrieval-Augmented Generation)** de **EcoMarket** depende directamente de la calidad, organización y coherencia de su base de conocimiento.  
Esta fase tiene como propósito **preparar, estructurar y optimizar los documentos internos** que servirán como fuente de información confiable para el asistente de atención al cliente.  

---

## 📘 Identificación de Documentos  

Para garantizar que el sistema RAG pueda responder preguntas reales de los clientes con precisión, se seleccionaron **cuatro tipos de documentos clave** que contienen la información más relevante del negocio.  
Estos documentos son los que alimentarán la base de conocimiento inicial del sistema:  

1. 🧾 **Política de Garantía (PDF):** Define las condiciones bajo las cuales los productos vendidos por EcoMarket pueden ser reparados, reemplazados o reembolsados. Permite responder preguntas sobre tiempos de garantía, cobertura y procedimientos de reclamo.  

2. 📦 **Política de Devolución (PDF):** Establece las condiciones y pasos para devolver productos adquiridos por los clientes. Permite responder consultas sobre plazos, requisitos y causas válidas de devolución.  

3. 🛒 **Política de Compra del Cliente (PDF):** Describe los procesos de compra, métodos de pago y condiciones de servicio. Facilita respuestas sobre medios de pago, facturación y confirmación de pedidos.  

4. 🤝 **Política de Proveedores (PDF):** Regula la relación comercial entre EcoMarket y sus proveedores. Sirve para consultas sobre términos de suministro, pagos o requisitos de calidad.  

📌 **Justificación:**  
Estos documentos concentran la mayor cantidad de interacciones potenciales con los clientes y procesos internos, convirtiéndose en la base más sólida para entrenar un sistema de atención automatizado, confiable y coherente con las políticas oficiales de la empresa.  

---

## ✂️ Segmentación (Chunking)  

### 🎯 Objetivo de la segmentación  

La segmentación o *chunking* consiste en dividir los documentos extensos en fragmentos manejables que el modelo de embeddings pueda procesar con precisión.  
Esta fase es clave, ya que el modelo **`all-MiniLM-L6-v2`** —seleccionado en la Fase 1— tiene **limitaciones de tokens**, por lo que los textos deben dividirse sin perder coherencia semántica.  

---

### 🧮 Estrategias evaluadas  

1. **📏 Tamaño fijo (por número de caracteres o tokens):**  
   Divide el texto cada cierta cantidad de palabras (por ejemplo, 500 tokens).  
   ✅ Ventajas: control fácil del tamaño y carga uniforme.  
   ⚠️ Desventajas: puede cortar oraciones o párrafos a la mitad, afectando la coherencia.  

2. **📑 Por párrafos o secciones naturales:**  
   Divide el documento siguiendo su estructura natural (encabezados, párrafos, títulos).  
   ✅ Ventajas: mantiene el contexto y sentido completo.  
   ⚠️ Desventajas: los fragmentos pueden variar mucho en tamaño.  

3. **🔁 Recursiva (por jerarquía textual):**  
   Utiliza un método jerárquico: primero por secciones, luego por párrafos o frases si son demasiado largos.  
   ✅ Ventajas: equilibrio entre tamaño y coherencia, ideal para textos normativos.  
   ⚠️ Desventajas: requiere procesamiento adicional y más lógica de segmentación.  

---

### 🧩 Estrategia seleccionada  

Para **EcoMarket**, se eligió la **estrategia recursiva basada en secciones y párrafos**, ya que los documentos (políticas, términos y condiciones) tienen una estructura jerárquica clara y coherente.  

📚 **Justificación:**  
- Preserva la **semántica y el contexto**, manteniendo oraciones completas y subtítulos relevantes.  
- Evita la **pérdida de información**, ya que no corta apartados críticos.  
- Optimiza la **recuperación semántica**, permitiendo que cada fragmento responda a una pregunta específica.  

**Ejemplo aplicado (Política de Devolución):**  

- Sección 1: Condiciones Generales  
  - Párrafo 1: Alcance de la política  
  - Párrafo 2: Productos excluidos de devolución  
- Sección 2: Procedimiento de Devolución  
  - Párrafo 1: Pasos para iniciar una devolución  
  - Párrafo 2: Tiempos y comprobantes requeridos  

Cada fragmento se almacena con su origen y metadatos (nombre del documento, sección, párrafo, etc.), garantizando **trazabilidad y contexto** durante la búsqueda.  

---

## 🧠 Indexación  

La indexación es el proceso de **transformar los fragmentos** generados durante el chunking en **vectores numéricos (embeddings)**, para luego almacenarlos en la base de datos vectorial donde se realizará la búsqueda por similitud semántica.  

---

### ⚙️ Proceso general de indexación  

1. **📥 Extracción del texto:**  
   Se utilizan herramientas como *PyMuPDF* o *pdfminer* para extraer el contenido de los documentos PDF.  

2. **🧹 Preprocesamiento:**  
   Limpieza del texto (eliminación de saltos de línea, caracteres especiales).  
   Normalización a minúsculas y eliminación de stopwords.  

3. **🧩 Segmentación:**  
   División del texto según la estrategia recursiva seleccionada.  
   Generación de fragmentos coherentes con identificadores únicos.  

4. **🤖 Generación de embeddings:**  
   Cada fragmento se convierte en un vector utilizando el modelo **`all-MiniLM-L6-v2`**.  
   Ejemplo en pseudocódigo:  

   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   embeddings = model.encode(fragments)

5. **🗄️ Almacenamiento en la base vectorial:**  
   Los vectores se cargan en **ChromaDB**, junto con el texto original y metadatos como el nombre del documento, la sección y la fecha de carga.  

6. **🔍 Validación del índice:**  
   Se realizan búsquedas de prueba (por ejemplo: “¿Cuánto tiempo tengo para devolver un producto?”) para comprobar la relevancia de los resultados.  

---

## 🔄 Flujo del proceso  

1. 📚 Documentos PDF de EcoMarket  
2. 🧾 Extracción de texto  
3. 🧹 Limpieza y normalización  
4. ✂️ Segmentación recursiva  
5. 🤖 Generación de embeddings con `all-MiniLM-L6-v2`  
6. 🗄️ Carga en **ChromaDB**  
7. 🔍 Búsqueda semántica por similitud  

---

## 🏁 Conclusión  

La creación de la **base de conocimiento** de EcoMarket constituye el cimiento del sistema RAG, garantizando que el modelo pueda **recuperar información precisa y contextualizada**.  
La combinación del **modelo `all-MiniLM-L6-v2`**, la **segmentación recursiva** y el **almacenamiento en ChromaDB** proporciona un sistema:  

✅ **Ligero y eficiente** para entornos locales.  
🚀 **Escalable** hacia soluciones cloud en fases posteriores.  
🔒 **Confiable y trazable**, al vincular cada fragmento con su documento original.  

Gracias a esta estructura, el asistente de IA de **EcoMarket** puede ofrecer respuestas exactas, transparentes y alineadas con las políticas oficiales de la empresa.  
✨ En otras palabras, el conocimiento de la organización se convierte en una herramienta viva al servicio del cliente.  



