# 🏥 HealthGuard AI - Agente de Bienestar Preventivo y Gamificación de Salud

## 📝 Descripción del Proyecto
Un agente que analiza de forma anónima los diagnósticos más frecuentes del hospital para esa aseguradora y diseña campañas de prevención específicas (ej. chequeos de próstata o mamas). Si el asegurado cumple con su chequeo en el hospital, el agente le otorga beneficios o descuentos automáticos en su prima en el CRM de Notion.

---

## 🚀 Flujo Completo del Proyecto (End-to-End)

**HealthGuard AI** opera de forma automatizada e integral siguiendo estos 5 pasos clave:

1. **Entrada de Datos (Análisis de Prevalencia):** El sistema recibe los diagnósticos más frecuentes ingresados por el hospital o administrador (ej. *Hipertensión*, *Diabetes*, *Asma*).
2. **Cerebro de Inteligencia Artificial (Gemini 2.0 Flash):** El backend procesa de forma anónima estas condiciones y genera automáticamente 4 campañas estratégicas de salud preventiva con enfoque financiero y de comunicación.
3. **Gamificación e Incentivo de Salud:** El asegurado asiste al hospital a realizarse sus chequeos preventivos. El administrador registra el cumplimiento ingresando el nombre del paciente en la plataforma web.
4. **Cálculo Automático de Beneficios:** El backend de Python procesa el cumplimiento y calcula de manera inmediata un **10% de descuento** en la prima (mensualidad) del seguro del usuario como recompensa.
5. **Integración en Tiempo Real con el CRM (Notion API):** La aplicación se conecta de manera segura a internet e inserta una fila en tiempo real dentro de la base de datos del CRM de Notion con la estructura: `[Nombre del Asegurado]`, `[Diagnóstico Cumplido]` y `[Descuento Otorgado]`.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3 con el framework **FastAPI** para la creación de rutas y API REST de alto rendimiento.
* **Servidor Web:** **Uvicorn** para el despliegue del entorno en la nube.
* **Inteligencia Artificial:** **Google GenAI SDK** utilizando el modelo de última generación **Gemini 2.0 Flash**.
* **Base de Datos / CRM:** **Notion API** para el almacenamiento seguro y visualización estructurada de los registros de cumplimiento.
* **Seguridad:** Uso de **Variables de Entorno (Secrets)** para mitigar riesgos y ocultar las llaves privadas de acceso de las APIs públicas.

---

## 📋 Requisitos para Replicar el Proyecto

Para desplegar este proyecto de forma idéntica en cualquier entorno local o en la nube, se deben configurar las siguientes variables de entorno obligatorias:

* `MI_API_KEY`: API Token oficial de Google AI Studio para el motor Gemini.
* `NOTION_TOKEN`: Token de integración interno (`secret_...`) generado desde el portal de desarrolladores de Notion.
* `NOTION_DATABASE_ID`: Identificador único de 32 caracteres correspondiente a la tabla CRM en Notion.

*Nota: La tabla de Notion asociada debe contar de forma estricta con las columnas: **Nombre** (Tipo Título), **Diagnóstico** (Tipo Texto) y **Descuento** (Tipo Número).*

