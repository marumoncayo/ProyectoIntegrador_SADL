# Sistema inteligente de apoyo a la toma de decisiones para la resolución del Problema del Agente Viajero en empresas de logística mediante modelos de lenguaje y algoritmos de optimización

**SADL — Sistema de Apoyo a la Decisión Logística**  
Trabajo de Titulación — Ingeniería en Sistemas y Computación  
Universidad San Francisco de Quito — 2026  
Estudiante: María Eulalia Moncayo Altamirano | Código: 00326226

---

## Descripción

SADL es un prototipo funcional de sistema inteligente para la planificación de rutas de recolección de alimentos desarrollado para el Banco de Alimentos Quito. El sistema interpreta escenarios logísticos descritos en lenguaje natural, selecciona automáticamente el algoritmo de optimización más adecuado (TSP, CVRPTW, Simplex, Método del Costo Mínimo o Shortest Path), construye rutas optimizadas mediante la heurística Nearest Neighbor, y gestiona incidentes viales en tiempo real. La solución integra un agente LLM (Gemini) como orquestador con OpenRouteService como motor de enrutamiento geográfico.

---

## Arquitectura general

El sistema está compuesto por cinco componentes principales que operan de forma integrada:

- **n8n (workflow)**: orquesta el flujo completo, incluyendo los dos agentes de IA, los nodos de código y la lógica condicional de incidentes.
- **Gemini (LLM)**: actúa como agente estratégico para selección de algoritmo, asignación de paradas por vehículo y gestión de incidentes viales.
- **OpenRouteService (ORS)**: motor de enrutamiento geográfico que calcula distancias y trazados reales sobre el mapa vial de Quito.
- **servidor.py**: proxy Flask que permite la comunicación entre n8n y ORS resolviendo restricciones de CORS.
- **index.html**: interfaz web del operador desde donde se ingresan los parámetros de la operación y se visualizan los resultados.

---

## Descripción de archivos

| Archivo | Descripción |
|---|---|
| `My_Final_SADL_workflow.json` | Workflow principal importable en n8n. Contiene los dos agentes, nodos de código y lógica completa del sistema. |
| `servidor.py` | Servidor proxy Flask. Debe estar corriendo localmente para que n8n pueda comunicarse con ORS. |
| `index.html` | Interfaz web del operador. Se abre directamente en el navegador. |
| `GUIS_Interactive_Map(1).py` | Script auxiliar para generación de mapas interactivos con Folium. |
| `Quito's KFCMap.html` | Mapa estático de referencia con la ubicación de las sucursales KFC en Quito utilizadas como puntos de recolección. |

---

## Requisitos previos

- [n8n](https://n8n.io/) instalado localmente
- Python 3.10 o superior
- Librerías Python: `flask`, `flask-cors`, `requests`, `folium`
- API Key de Google Gemini
- API Key de OpenRouteService

Instalación de dependencias Python:

```bash
pip install flask flask-cors requests folium
```

---

## Cómo ejecutar

1. **Levantar el servidor proxy:**
```bash
python servidor.py
```

2. **Importar el workflow en n8n:**
   - Abrir n8n en el navegador (`http://localhost:5678`)
   - Ir a Workflows → Import
   - Seleccionar `My_Final_SADL_workflow.json`
   - Configurar las credenciales de Gemini y ORS en los nodos correspondientes

3. **Abrir la interfaz:**
   - Abrir `index.html` directamente en el navegador
   - Ingresar los parámetros de la operación y ejecutar

---

## Contexto académico

Este sistema fue desarrollado como trabajo de titulación de la carrera de Ingeniería en Sistemas y Computación de la Universidad San Francisco de Quito (USFQ), en colaboración con el Banco de Alimentos Quito. El prototipo tiene fines académicos y de investigación.
