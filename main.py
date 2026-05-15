import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from google import genai
from google.genai import errors as genai_errors
from notion_client import Client as NotionClient
from notion_client.errors import APIResponseError

app = FastAPI()

genai_client = genai.Client(api_key=os.environ["MI_API_KEY"])

DEFAULT_DIAGNOSES = ["Hipertensión", "Diabetes", "Cáncer de próstata"]

DISCOUNT_RATE = 0.10


class GenerateRequest(BaseModel):
    diagnoses: list[str]


class RegisterRequest(BaseModel):
    nombre: str
    diagnostico: str


@app.get("/", response_class=HTMLResponse)
def home():
    default_list = "\n".join(DEFAULT_DIAGNOSES)
    return f"""
    <html>
        <head>
            <title>HealthGuard AI</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <style>
                #campaign h1, #campaign h2, #campaign h3 {{ font-weight: 700; margin-top: 1rem; margin-bottom: 0.5rem; }}
                #campaign h1 {{ font-size: 1.5rem; }}
                #campaign h2 {{ font-size: 1.25rem; }}
                #campaign h3 {{ font-size: 1.1rem; }}
                #campaign ul, #campaign ol {{ padding-left: 1.5rem; margin-bottom: 0.75rem; }}
                #campaign ul {{ list-style-type: disc; }}
                #campaign ol {{ list-style-type: decimal; }}
                #campaign li {{ margin-bottom: 0.25rem; }}
                #campaign p {{ margin-bottom: 0.75rem; }}
                #campaign strong {{ font-weight: 700; }}
                #campaign em {{ font-style: italic; }}
            </style>
        </head>
        <body class="bg-gray-100">
            <div class="max-w-4xl mx-auto p-10">
                <h1 class="text-4xl font-bold mb-6">HealthGuard AI</h1>

                <!-- Campaign Generator -->
                <div class="bg-white p-6 rounded-xl shadow">
                    <h2 class="text-2xl font-semibold mb-2">Diagnósticos</h2>
                    <p class="text-sm text-gray-500 mb-1">Ingresa un diagnóstico por línea.</p>
                    <p class="text-sm text-gray-400 mb-3">(puedes borrar estos diagnósticos y escribir los que desees)</p>
                    <textarea
                        id="diagnosesInput"
                        rows="5"
                        class="w-full border border-gray-300 rounded-lg p-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-y"
                        placeholder="Ej: Hipertensión"
                    >{default_list}</textarea>
                    <button
                        id="generateBtn"
                        onclick="generateCampaign()"
                        class="mt-4 inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
                    >
                        <svg id="genSpinner" class="hidden animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                        </svg>
                        <span id="genBtnText">Generar campañas</span>
                    </button>
                </div>

                <!-- Campaign Results -->
                <div id="result" class="hidden mt-6 bg-white p-6 rounded-xl shadow">
                    <h2 class="text-2xl font-semibold mb-4">Campañas Generadas</h2>
                    <div id="campaign" class="text-gray-700"></div>
                </div>

                <!-- Compliance Registration Form -->
                <div id="registerSection" class="hidden mt-6 bg-white p-6 rounded-xl shadow">
                    <h2 class="text-2xl font-semibold mb-1">Registrar Cumplimiento de Asegurado</h2>
                    <p class="text-sm text-gray-500 mb-4">Al registrar el chequeo, se aplica un <strong>10% de descuento</strong> en la prima y se guarda en Notion.</p>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Asegurado</label>
                    <input
                        id="nombreInput"
                        type="text"
                        placeholder="Ej: Juan Pérez"
                        class="w-full border border-gray-300 rounded-lg p-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
                    />
                    <button
                        id="registerBtn"
                        onclick="registrarChequeo()"
                        class="inline-flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
                    >
                        <svg id="regSpinner" class="hidden animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                        </svg>
                        <span id="regBtnText">Registrar Chequeo Cumplido</span>
                    </button>

                    <div id="registerSuccess" class="hidden mt-4 bg-green-50 border border-green-200 text-green-800 p-4 rounded-xl"></div>
                    <div id="registerError" class="hidden mt-4 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl"></div>
                </div>

                <div id="error" class="hidden mt-6 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl"></div>
            </div>

            <script>
                let lastDiagnoses = [];

                async function generateCampaign() {{
                    const btn = document.getElementById('generateBtn');
                    const spinner = document.getElementById('genSpinner');
                    const btnText = document.getElementById('genBtnText');
                    const result = document.getElementById('result');
                    const errorBox = document.getElementById('error');
                    const registerSection = document.getElementById('registerSection');
                    const input = document.getElementById('diagnosesInput').value;

                    const diagnoses = input
                        .split('\\n')
                        .map(d => d.trim())
                        .filter(d => d.length > 0);

                    if (diagnoses.length === 0) {{
                        errorBox.textContent = 'Por favor, ingresa al menos un diagnóstico.';
                        errorBox.classList.remove('hidden');
                        return;
                    }}

                    btn.disabled = true;
                    spinner.classList.remove('hidden');
                    btnText.textContent = 'Generando...';
                    result.classList.add('hidden');
                    registerSection.classList.add('hidden');
                    errorBox.classList.add('hidden');

                    try {{
                        const res = await fetch('/generate', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ diagnoses }})
                        }});
                        const data = await res.json();

                        if (!res.ok) {{
                            throw new Error(data.detail || 'Error desconocido');
                        }}

                        document.getElementById('campaign').innerHTML = marked.parse(data.campaign);
                        result.classList.remove('hidden');
                        lastDiagnoses = diagnoses;
                        registerSection.classList.remove('hidden');
                    }} catch (err) {{
                        errorBox.textContent = 'Error: ' + err.message;
                        errorBox.classList.remove('hidden');
                    }} finally {{
                        btn.disabled = false;
                        spinner.classList.add('hidden');
                        btnText.textContent = 'Generar campañas con IA';
                    }}
                }}

                async function registrarChequeo() {{
                    const btn = document.getElementById('registerBtn');
                    const spinner = document.getElementById('regSpinner');
                    const btnText = document.getElementById('regBtnText');
                    const successBox = document.getElementById('registerSuccess');
                    const errorBox = document.getElementById('registerError');
                    const nombre = document.getElementById('nombreInput').value.trim();

                    if (!nombre) {{
                        errorBox.textContent = 'Por favor, ingresa el nombre del asegurado.';
                        errorBox.classList.remove('hidden');
                        successBox.classList.add('hidden');
                        return;
                    }}

                    const diagnostico = lastDiagnoses.join(', ');

                    btn.disabled = true;
                    spinner.classList.remove('hidden');
                    btnText.textContent = 'Registrando...';
                    successBox.classList.add('hidden');
                    errorBox.classList.add('hidden');

                    try {{
                        const res = await fetch('/register', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ nombre, diagnostico }})
                        }});
                        const data = await res.json();

                        if (!res.ok || data.status === 'error') {{
                            throw new Error(data.message || data.detail || 'Error desconocido');
                        }}

                        successBox.innerHTML = `
                            <p class="font-semibold text-lg">¡Chequeo registrado exitosamente!</p>
                            <p class="mt-1">Asegurado: <strong>${{nombre}}</strong></p>
                            <p>Diagnóstico(s): <strong>${{diagnostico}}</strong></p>
                            <p>Descuento aplicado: <strong>${{data.descuento}}</strong> en la prima</p>
                            <p class="mt-2 text-sm text-green-600">Registro guardado en Notion.</p>
                        `;
                        successBox.classList.remove('hidden');
                        document.getElementById('nombreInput').value = '';
                    }} catch (err) {{
                        errorBox.textContent = 'Error: ' + err.message;
                        errorBox.classList.remove('hidden');
                    }} finally {{
                        btn.disabled = false;
                        spinner.classList.add('hidden');
                        btnText.textContent = 'Registrar Chequeo Cumplido';
                    }}
                }}
            </script>
        </body>
    </html>
    """


@app.get("/health")
def health():
    return {
        "status": "ok",
        "api_key_loaded": bool(os.environ.get("MI_API_KEY")),
        "notion_configured": bool(os.environ.get("NOTION_TOKEN") and os.environ.get("NOTION_DATABASE_ID"))
    }


@app.post("/generate")
def generate_campaign(body: GenerateRequest):
    if not body.diagnoses:
        raise HTTPException(status_code=422, detail="Se requiere al menos un diagnóstico.")

    diagnoses_list = "\n".join(f"- {d}" for d in body.diagnoses)

    prompt = f"""
    Analiza estos diagnósticos médicos:

    {diagnoses_list}

    Genera campañas preventivas para una aseguradora médica.
    """

    try:
        response = genai_client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return {"campaign": response.text}
    except genai_errors.APIError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/register")
def register_compliance(body: RegisterRequest):
    try:
        if not body.nombre or not body.diagnostico:
            return JSONResponse(
                status_code=200,
                content={"status": "error", "message": "Nombre y diagnóstico son requeridos."}
            )

        descuento_pct = int(DISCOUNT_RATE * 100)
        descuento_str = f"{descuento_pct}%"

        notion_token = os.environ.get("NOTION_TOKEN")
        database_id = os.environ.get("NOTION_DATABASE_ID")

        if not notion_token or not database_id:
            return JSONResponse(
                status_code=200,
                content={"status": "error", "message": "Notion no está configurado correctamente."}
            )

        try:
            notion = NotionClient(auth=notion_token)
            notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Nombre": {
                        "title": [{"text": {"content": body.nombre}}]
                    },
                    "Diagnóstico": {
                        "rich_text": [{"text": {"content": body.diagnostico}}]
                    },
                    "Descuento": {
                        "number": descuento_pct
                    }
                }
            )
        except Exception as notion_err:
            print(f"[Notion error] {notion_err}")
            return JSONResponse(
                status_code=200,
                content={"status": "error", "message": f"Notion write failed: {str(notion_err)}"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "nombre": body.nombre,
                "diagnostico": body.diagnostico,
                "descuento": descuento_str
            }
        )

    except Exception as e:
        print(f"[Unhandled error in /register] {e}")
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": f"Unexpected error: {str(e)}"}
        )
