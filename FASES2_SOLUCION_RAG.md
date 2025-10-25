
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

---

###  Resumen del flujo lógico
###  Resumen del flujo lógico

```
%%{init: {"theme": "neutral", "flowchart": {"curve": "linear", "htmlLabels": false}}}%%
flowchart TD
    A["Cliente solicita devolución"]
    B["Validar orden y obtener datos"]
    C["Consultar políticas de devolución (RAG)"]
    D["Verificar elegibilidad del producto"]
    E["Generar etiqueta"]
    F["Notificar cliente"]
    G["Cerrar caso"]
    H["Explicar motivo y finalizar"]

    A --> B
    B --> C
    C --> D
    D -->|Elegible| E
    E --> F
    F --> G
    D -->|No elegible| H

---

