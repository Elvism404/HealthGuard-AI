# 🏥 HealthGuard AI - Agente de Bienestar Preventivo y Gamificación de Salud

## 🚀 Proyecto desarrollado para hackIAthon 2026

HealthGuard AI fue desarrollado por el equipo **Promptásticos** como parte del proceso de selección del hackIAthon organizado por VIAMATICA.

Nuestra propuesta utiliza Inteligencia Artificial para analizar diagnósticos frecuentes y generar campañas preventivas automatizadas enfocadas en bienestar y salud.

Además, el sistema incorpora gamificación médica mediante beneficios automáticos para asegurados que cumplen sus chequeos preventivos.

Con este proyecto buscamos demostrar nuestras habilidades en:
- Inteligencia Artificial aplicada
- Automatización de procesos
- Integración de APIs
- Desarrollo backend
- Soluciones tecnológicas para el sector salud
  
---

## 📝 Descripción del Proyecto
Un agente que analiza de forma anónima los diagnósticos más frecuentes del hospital para esa aseguradora y diseña campañas de prevención específicas (ej. chequeos de próstata o mamas). Si el asegurado cumple con su chequeo en el hospital, el agente le otorga beneficios o descuentos automáticos en su prima en el CRM de Notion.

---

## 🚀 Enlace de Acceso Funcional
Para probar la aplicación interactiva en tiempo real, acceda al siguiente enlace:
👉 **[Ejecutar HealthGuard AI](https://c9678688-1a10-41b5-a0c0-da41d3a28f7a-00-12htecrt17g94.spock.replit.dev:8000/)**

-

## 📊 CRM y Registro de Beneficios

HealthGuard AI integra Notion como sistema CRM para almacenar y visualizar los registros de asegurados que completan sus chequeos preventivos.

Cada vez que un usuario cumple con su control médico:
- Se registra automáticamente en la base de datos
- Se aplica un descuento del 10%
- La información queda organizada en tiempo real

🔗 Base de datos en Notion:
https://seen-eyeliner-3e4.notion.site/3611a1ce16d0805ab701fa0fd68510bb?v=3611a1ce16d08086a824000c885b1978

---

## 📋 Instrucciones de Uso de la Plataforma

1. **Generación de Campañas:** En el cuadro de texto de "Diagnósticos", ingrese una o varias condiciones médicas (ej. *Hipertensión*, *Diabetes*) y haga clic en **"Generar campañas"**. El motor de IA Gemini procesará y desplegará la estrategia preventiva en la pantalla.
2. **Gamificación y Registro CRM:** En la sección inferior, ingrese el nombre de un asegurado que haya asistido a su control y presione **"Registrar Chequeo Cumplido"**. El sistema calculará automáticamente un **10% de descuento** en su prima y enviará un registro seguro mediante la API directo a la base de datos de Notion.

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

---

## 👥 Colaboradores

- Elvis Marcillo  
🔗 https://github.com/Elvism404

- Kristel Echeverría  
🔗 https://github.com/Krissie2005
