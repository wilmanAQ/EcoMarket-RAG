
---

# 🧠 Fase 1: Diseño de la Arquitectura del Agente

## 1. Definición de las Herramientas (Tools)

Las herramientas representan las funciones que permiten al agente ejecutar acciones autónomas sobre sistemas externos o internos de **EcoMarket**. En este caso, se definen las siguientes:

### 🧰 Herramientas del Agente

| **Herramienta** | **Descripción** | **Entrada (Input)** | **Salida (Output)** | **Propósito principal** |
|------------------|-----------------|----------------------|----------------------|---------------------------|
| `obtener_orden` | Consulta la información completa de una orden específica. | ID de orden. | Datos de la orden (productos, fechas, estado). | Permite validar si la orden existe y si puede ser procesada. |
| `get_orders_dataset` | Obtiene el dataset completo de órdenes registradas en el sistema. | Ninguna. | Conjunto de órdenes con información general (IDs, fechas, estado, productos). | Facilita el acceso masivo a los datos históricos de órdenes. |
| `get_order` | Recupera la información detallada de una orden específica. | ID de la orden. | Información detallada de la orden (productos, valor total, estado, cliente). | Permite al agente consultar detalles de una orden puntual. |
| `query` | Realiza consultas al sistema RAG (Retrieval-Augmented Generation) para obtener información contextual. | Pregunta o instrucción del usuario. | Respuesta generada a partir de la base de conocimiento. | Permite recuperar información semántica y contextual desde la base de conocimiento. |
| `register_return_order` | Registra una nueva orden de devolución en el sistema. | ID de la orden y motivo de devolución. | Confirmación de registro y número de caso. | Automatiza el proceso de devoluciones, generando trazabilidad en el sistema. |


Estas herramientas funcionan como **módulos independientes**, invocados por el agente según la fase del flujo.
Todas siguen un formato estructurado de **entrada/salida** y retornan mensajes **JSON controlados**, lo que garantiza **consistencia, interpretabilidad y seguridad**.

---

## 2. Selección del Marco de Agentes

Se selecciona **LangChain**, apoyado en **LangGraph** para la orquestación del flujo del agente.

### Justificación

* **Integración natural con RAG:** LangChain permite conectar el agente con el sistema RAG existente, reutilizando los retrievers y document loaders sin modificar la estructura base.
* **Ejecución segura de herramientas:** Su sistema de *tool calling* y validación de esquemas JSON evita alucinaciones y garantiza que el agente solo actúe mediante funciones autorizadas.
* **Flujo de trabajo controlado:** LangGraph permite representar el proceso de devolución como un grafo de estados (inicio, verificación, acción, cierre), ofreciendo transparencia, trazabilidad y control sobre las decisiones.
* **Escalabilidad y modularidad:** La arquitectura basada en *chains* y *agents* facilita agregar nuevas herramientas en fases futuras (p. ej., `gestionar_reembolsos` o `consultar_inventario`).
* **Compatibilidad con auditoría y observabilidad:** Las integraciones con **LangSmith** permiten rastrear cada paso del agente para fines de depuración o cumplimiento normativo.

> En comparación, **LlamaIndex** se orienta más a la recuperación y organización avanzada de información (*RAG*), mientras que **LangChain/LangGraph** aportan mejor control sobre la toma de decisiones y la ejecución de acciones autónomas, esenciales para este caso de uso.

---

## 3. Planificación del Flujo de Trabajo

El proceso automatizado que seguirá el agente se estructura en **fases secuenciales**, definidas por decisiones lógicas y llamadas a herramientas:

1. **Inicio e interpretación:**
   El agente analiza la intención del usuario (solicitud de devolución) y verifica que la conversación corresponda al flujo de devoluciones.

2. **Obtención de datos:**
   Si el cliente no proporciona los datos necesarios (número de orden, producto, motivo), el agente solicita la información y llama a `obtener_orden`.

3. **Consulta de políticas:**
   Mediante el módulo RAG, se ejecuta `consultar_politica_devoluciones` para traer las condiciones vigentes según el tipo de producto y la fecha de compra.

4. **Verificación de elegibilidad:**
   Con la información de la orden y la política, el agente ejecuta `verificar_elegibilidad_producto`.

   * Si **no cumple** los criterios, el agente explica el motivo al cliente citando la política.
   * Si **cumple**, continúa al siguiente paso.

5. **Generación de etiqueta:**
   Se llama a `generar_etiqueta_devolucion` para crear la guía de envío y registrar el proceso.

6. **Notificación y cierre:**
   El agente usa `notificar_cliente` para enviar el comprobante y la etiqueta, actualiza el estado de la orden y registra la auditoría final del caso.
   
7. [Diseño, Planificación del Flujo del Trabajo del Agente ](https://drive.google.com/file/d/1KQxbUxqEhoYMhs3Xw-ShIKC2cHn0p8P-/view?usp=sharing)


-------


# 🧩 Fase 2: Implementación y Conexión de Componentes

En esta fase se continuó con la implementación del sistema **RAG existente**, logrando que el modelo seleccionado —**LangChain**— automatizara el proceso de devolución mediante la **política generada** en fases anteriores.

El modelo ahora es capaz de **gestionar de forma autónoma** la generación de **etiquetas numéricas**, utilizadas para **identificar los productos elegibles** dentro del flujo de devolución. Esta nueva capacidad le otorga al agente una **autonomía operativa**, permitiéndole responder eficazmente a las **consultas y solicitudes de los usuarios** de la empresa **EcoMarket**, integrando tanto la lógica del negocio como las políticas de devolución vigentes.

-----

## ⚙️ Integración Técnica

Esta fase corresponde al proceso de **codificación e integración de componentes**.
Se realizó la integración del trabajo realizado en el *Taller 2* con la nueva **funcionalidad del agente inteligente**, siguiendo los lineamientos definidos:

### 🔧 Extensión del Código Base

A partir del código desarrollado en el taller anterior, se añadió la lógica del agente, definiendo las **herramientas (tools)** como funciones y configurando su **inicialización dentro del entorno FastAPI**.

### 💬 Manejo de Respuestas

El agente no solo ejecuta las acciones, sino que también **formatea las respuestas** de forma clara y empática, informando al usuario sobre el resultado del proceso (por ejemplo, si el producto fue **elegible para devolución** y si se generó su **etiqueta de envío**).
Además, maneja **mensajes de error** y **validaciones** del flujo de manera controlada y coherente.

### 🧠 Evaluación del Comportamiento

Se realizaron pruebas con **diversos prompts y escenarios** para comprobar la capacidad del agente de discernir:

* Cuándo debe **utilizar las herramientas** (`retrieval`, `query`, `FastAPI`, `register_return_order`).
* Cuándo debe **responder directamente** utilizando el **contexto recuperado de ChromaDB** y procesado por el **LLM (OpenAI/Azure)**.

---

## 🧩 Conexión de Componentes

Esta fase consolidó la **interconexión entre los módulos principales**:

| Componente                            | Descripción                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| **SAP Front (SPA)**                   | Interfaz donde el usuario realiza la solicitud de devolución.                      |
| **API REST / FastAPI Backend**        | Recibe la solicitud, valida datos, ejecuta herramientas y coordina el flujo.       |
| **LangChain (Orquestación)**          | Controla el flujo de decisiones del agente y la interacción con las herramientas.  |
| **ChromaDB (Retrieval)**              | Base vectorial que almacena las políticas de devolución y contexto relevante.      |
| **LLM / Embeddings (OpenAI - Azure)** | Motor de razonamiento que interpreta la consulta y genera la respuesta contextual. |

---

> ✅ Con esta arquitectura integrada, el sistema RAG logra automatizar el proceso de devolución, generar etiquetas únicas y ofrecer respuestas dinámicas y contextualizadas a los usuarios de **EcoMarket**, garantizando eficiencia, trazabilidad y una experiencia de atención optimizada.


-------

# Fase 3 · Análisis Crítico y Propuestas de Mejora  
**Caso:** Agente de IA para devoluciones de productos y generación de etiquetas (RAG + LLM + FastAPI)

---

## 🔐 Análisis de Seguridad y Ética

Cuando un agente de IA con arquitectura RAG (Retrieval-Augmented Generation) y modelo LLM recibe la capacidad de **tomar acciones autónomas**, como verificar elegibilidad o generar etiquetas de devolución, surgen riesgos éticos y técnicos que deben ser abordados desde el diseño.

1. **Riesgo de ejecución indebida.**  
   El LLM podría interpretar mal las políticas o generar una acción no permitida (como emitir reembolsos en lugar de solo etiquetas).  
   **Solución:** implementar validaciones con *schemas* Pydantic y una política de autorización previa a la ejecución (Rule-Based Access Control).

2. **Fuga de información (PII).**  
   El contexto recuperado por el RAG podría incluir información sensible de la devulucoón.  
   **Solución:** anonimizar datos antes de ser procesados por el LLM y aplicar enmascaramiento en los logs de FastAPI.

3. **Alucinación de políticas o decisiones.**  
   El modelo podría citar reglas inexistentes o modificar las condiciones reales de devolución.  
   **Solución:** utilizar un verificador de contexto (“retriever-verifier”) que contraste las fuentes RAG con las políticas oficiales indexadas.

4. **Transparencia y responsabilidad.**  
   Es fundamental explicar al cliente por qué su devolución fue aceptada o rechazada, con base en fuentes verificables.  
   **Solución:** generar trazas explicativas y conservar registros auditables (WORM) de todas las decisiones tomadas por el agente.

5. **Equidad y ética operacional.**  
   La IA no debe favorecer ni discriminar a clientes por idioma, zona o historial.  
   **Solución:** aplicar métricas de equidad y revisiones periódicas de sesgo en los datos y en las respuestas del modelo.

---

## 📊 Monitoreo y Observabilidad

La operación confiable de un agente autónomo requiere **observabilidad integral**, desde FastAPI hasta el modelo LLM.

1. **Registro estructurado de acciones.**  
   Cada paso —consulta, verificación, generación de etiqueta— debe registrarse con `trace_id` y `span_id`.  
   **Solución:** implementar OpenTelemetry y almacenar trazas estructuradas (JSON) con métricas como latencia, éxito y tokens usados.

2. **Panel de control (Grafana / Prometheus).**  
   Permite observar métricas de desempeño y alertar desviaciones.  
   - `label_issue_success_rate` → porcentaje de etiquetas generadas con éxito.  
   - `policy_block_rate` → acciones bloqueadas por reglas.  
   - `llm_latency_ms` → tiempo de respuesta del modelo.  
   **Solución:** integrar un tablero con indicadores de calidad y seguridad.

3. **Sistema de alertas automáticas.**  
   Si el agente genera demasiados errores o detecta PII sin enmascarar, debe suspender la ejecución.  
   **Solución:** configurar alertas en **Slack** o correo cuando se supere un umbral de riesgo definido (por ejemplo, 5% de errores críticos).

4. **Evaluación continua (Shadow Mode).**  
   Permite validar nuevas versiones del agente sin ejecutar acciones reales.  
   **Solución:** habilitar modo sombra en FastAPI, comparando decisiones propuestas con las históricas de analistas humanos.

---

## 🚀 Propuestas de Mejora

El agente actual puede evolucionar hacia un ecosistema de **agentes colaborativos**, ampliando sus capacidades dentro del proceso de atención al cliente.

1. **Agente de reemplazo automático.**  
   Si el producto es elegible, genera una nueva orden de envío en el sistema ERP y coordina el despacho al recibir la etiqueta escaneada.  
   *Beneficio:* mejora la experiencia del cliente y reduce tiempos de reposición.

2. **Agente CRM inteligente.**  
   Actualiza el historial del cliente en tiempo real: motivos de devolución, nivel de satisfacción y frecuencia de reembolsos.  
   *Beneficio:* aporta datos valiosos para segmentación y retención.

3. **Agente logístico.**  
   Agenda automáticamente la recolección del producto con el operador de transporte, según el SLA y la zona geográfica.  
   *Beneficio:* reduce intervención humana y optimiza rutas de entrega.

4. **Agente auditor.**  
   Verifica que cada decisión del agente principal esté sustentada en políticas vigentes y correctamente citadas.  
   *Beneficio:* refuerza trazabilidad y cumplimiento normativo.

5. **Agente de fraude y riesgo.**  
   Evalúa patrones inusuales en las devoluciones, como repetición de solicitudes o cambios sospechosos de dirección.  
   *Beneficio:* reduce pérdidas económicas y abuso del sistema.

---

## ✅ Conclusión

El análisis crítico revela que un agente RAG con FastAPI puede operar con autonomía y seguridad siempre que se apliquen controles éticos, técnicos y de observabilidad.  
Las mejoras propuestas fortalecen su fiabilidad y escalabilidad, permitiendo que EcoMarket evolucione hacia un sistema de **atención inteligente**, trazable y centrado en la confianza del cliente.

Aquí tienes la justificación de forma breve, clara y profesional, con dos párrafos y una tabla comparativa, todo en formato **Markdown**:

---

## 🧩 Fase 4: Despliegue de la Aplicación

Durante la fase de despliegue se optó por utilizar **Gradio** como herramienta principal para la construcción de la interfaz del agente RAG de devoluciones. Esta elección se fundamenta en su **simplicidad, rapidez de implementación y compatibilidad directa con modelos conversacionales**, lo que permite construir interfaces funcionales en pocos minutos sin requerir una estructura compleja. Gradio ofrece componentes nativos para chat, carga de archivos y botones interactivos, lo que facilita la comunicación entre el usuario y el backend basado en FastAPI, optimizando el flujo entre solicitud, verificación y generación de etiquetas de devolución.

Por otro lado, **Streamlit**, aunque es una herramienta potente para el desarrollo de dashboards interactivos y aplicaciones de análisis de datos, no resulta tan eficiente para un escenario centrado en la **interacción conversacional y las respuestas en tiempo real**. Su estructura requiere más configuración de estados, manejo de sesiones y desarrollo de interfaz, lo que incrementa el tiempo y la complejidad sin aportar beneficios sustanciales en un caso donde la prioridad es la respuesta rápida y clara del agente.

---

### ⚖️ Comparativa entre Gradio y Streamlit

| Criterio                        | **Gradio**                                           | **Streamlit**                                         |
| ------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| **Enfoque principal**           | Demos de IA, chatbots, inferencia en tiempo real     | Dashboards, visualizaciones, aplicaciones multipágina |
| **Facilidad de uso**            | Muy alta: interfaz lista en minutos                  | Alta, pero requiere más estructura y código           |
| **Componentes de chat**         | Nativos y optimizados (`ChatInterface`, `Textbox`)   | Requiere personalización manual con `st.chat_*`       |
| **Integración con FastAPI**     | Simple con `requests` o endpoints directos           | Similar, pero con más configuración de estado         |
| **Despliegue**                  | Rápido (Hugging Face Spaces, Gradio Cloud, Docker)   | Más orientado a Streamlit Cloud o servidores propios  |
| **Adecuado para este proyecto** | ✅ Ideal para el flujo conversacional de devoluciones | ❌ Excesivo para un caso no analítico                  |

---

> ✅ En conclusión, **Gradio** fue la herramienta ideal para este proyecto, al equilibrar **rapidez, funcionalidad y facilidad de integración** con el backend del agente RAG, logrando una interfaz fluida y centrada en la experiencia del usuario.






---

