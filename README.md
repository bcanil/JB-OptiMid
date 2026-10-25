# JB OptiMid

**Asistente de Investigación de Operaciones**  
Proyecto académico de la Universidad Mariano Gálvez de Guatemala.

JB OptiMid reúne herramientas de apoyo para modelar y resolver problemas introductorios de Investigación de Operaciones. Está desarrollado con Python y Streamlit.

## Módulos disponibles

- **Inicio:** entrada a la aplicación.
- **Modelación:** apoyo para expresar situaciones como modelos matemáticos.
- **Programación lineal:** resolución de modelos de dos variables mediante optimización lineal.
- **Método gráfico:** representación visual de modelos de programación lineal.
- **Método Simplex:** implementación educativa para problemas de maximización con dos variables y restricciones de tipo `≤`.
- **Transporte y asignación:** herramientas para problemas de distribución y asignación.
- **Inventarios:** cálculos básicos relacionados con gestión de inventarios.
- **Tutor y prácticas:** apoyo didáctico con inteligencia artificial y ejercicios.

> El alcance y los supuestos dependen de cada módulo. Revisa las condiciones que muestra la interfaz y verifica los resultados antes de usarlos en decisiones reales.

## Requisitos

- Python compatible con las versiones de las dependencias del proyecto.
- Las dependencias declaradas en `requirements.txt`.
- Una clave de API de Gemini para las funciones de tutoría con IA.

## Ejecutar localmente en Windows

Abre CMD en la carpeta del proyecto y ejecuta:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit mostrará una dirección local para abrir la aplicación en el navegador. Para detener el servidor, vuelve a la terminal y presiona `Ctrl+C`.

## Configurar Gemini

La aplicación lee la clave desde el secreto `GEMINI_API_KEY`. No escribas la clave directamente en `app.py`, no la publiques en el repositorio y no la compartas en capturas o mensajes.

- **Streamlit Community Cloud:** abre la configuración de la aplicación, entra a **Secrets** y define `GEMINI_API_KEY` con el valor de tu clave.
- **Ejecución local:** puedes configurar el secreto mediante el archivo `.streamlit/secrets.toml` (mantén ese archivo fuera de Git). Ejemplo de estructura:

```toml
GEMINI_API_KEY = "TU_CLAVE_AQUI"
```

Sustituye el texto de ejemplo por tu propia clave; nunca subas el valor real a GitHub. Si Gemini está temporalmente saturado, espera unos minutos y vuelve a intentarlo.

## Dependencias principales

Las dependencias están listadas en `requirements.txt`:

- Streamlit: interfaz web.
- NumPy: operaciones numéricas.
- Plotly: gráficas interactivas.
- SciPy: algoritmos de optimización.
- Google Gen AI SDK: integración con Gemini.

## Despliegue y trabajo de desarrollo

La aplicación publicada y la rama de desarrollo pueden contener versiones diferentes. Los cambios propuestos en una rama o pull request no se consideran incorporados a la versión principal hasta que se revisen y aprueben.

## Uso responsable

JB OptiMid es una herramienta académica de apoyo. Los resultados dependen de que los datos, las unidades, la función objetivo y las restricciones estén bien formulados. Comprueba el modelo y la solución con los procedimientos vistos en clase.
