"""
SADL — Servidor Flask
Banco de Alimentos Quito

Cómo iniciar:
  pip install flask flask-cors folium requests
  python servidor.py

Luego abre en el navegador: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests as req
import folium
from folium.plugins import AntPath
import math

app = Flask(__name__, static_folder=".")
CORS(app)

N8N_WEBHOOK = "http://localhost:5678/webhook/banco-alimentos"

# ─────────────────────────────────────────
# DATOS KFC
# ─────────────────────────────────────────
KFC_LOCATIONS = [
    {"id":1,  "name":"KFC Mitad del Mundo",                  "lat":-0.0087818,            "lon":-78.4453248},
    {"id":2,  "name":"KFC Carcelén",                         "lat":-0.09096943698450818,  "lon":-78.47240877617304},
    {"id":3,  "name":"KFC Calderón",                         "lat":-0.10168228114577059,  "lon":-78.42259957617303},
    {"id":4,  "name":"KFC Llano Grande",                     "lat":-0.10933131518582592,  "lon":-78.44497092149685},
    {"id":5,  "name":"KFC El Portal",                        "lat":-0.10784235236073714,  "lon":-78.4581366491866},
    {"id":6,  "name":"KFC Carapungo",                        "lat":-0.10388727942985249,  "lon":-78.45334764733742},
    {"id":7,  "name":"KFC Santa María Condado",              "lat":-0.10560653707793938,  "lon":-78.49737677617296},
    {"id":8,  "name":"KFC La Prensa",                        "lat":-0.125327863819403,    "lon":-78.49369167829639},
    {"id":9,  "name":"KFC Comité del Pueblo",                "lat":-0.12646367961966587,  "lon":-78.46868586083046},
    {"id":10, "name":"KFC Eloy Alfaro",                      "lat":-0.12299483184347916,  "lon":-78.471521232287},
    {"id":11, "name":"KFC Molineros",                        "lat":-0.12889582202539948,  "lon":-78.47225647802205},
    {"id":12, "name":"KFC Cotocollao Autorápido",            "lat":-0.12169419482234402,  "lon":-78.49415794918652},
    {"id":13, "name":"KFC Plaza de las Américas Autorápido", "lat":-0.17472996652261663,  "lon":-78.49301907617267},
    {"id":14, "name":"KFC El Inca",                          "lat":-0.1592092647918051,   "lon":-78.48285583384396},
    {"id":15, "name":"KFC Quicentro Norte",                  "lat":-0.17621119074516067,  "lon":-78.48054887719914},
    {"id":16, "name":"KFC CCI",                              "lat":-0.17679089533123768,  "lon":-78.48475936267944},
    {"id":17, "name":"KFC CCI K4",                           "lat":-0.17684453925504715,  "lon":-78.48472717617267},
    {"id":18, "name":"KFC El Jardín",                        "lat":-0.18874366669164389,  "lon":-78.48747006083026},
    {"id":19, "name":"KFC Colón Autorápido",                 "lat":-0.1977426257000934,   "lon":-78.49569040431861},
    {"id":20, "name":"KFC Baca Ortiz",                       "lat":-0.20148436685755877,  "lon":-78.4865384626794},
    {"id":21, "name":"KFC Hospital del IESS",                "lat":-0.20502102443974507,  "lon":-78.50257040500823},
    {"id":22, "name":"KFC Patria",                           "lat":-0.208111266948482,    "lon":-78.49554441850127},
    {"id":23, "name":"KFC San Francisco de Quito",           "lat":-0.22016058085245827,  "lon":-78.51424117617246},
    {"id":24, "name":"KFC Coral",                            "lat":-0.23856279614953846,  "lon":-78.52351876267925},
    {"id":25, "name":"KFC El Recreo",                        "lat":-0.2522124207113469,   "lon":-78.52268390445943},
    {"id":26, "name":"KFC El Recreo K10",                    "lat":-0.2518047288925947,   "lon":-78.5224264124049},
    {"id":27, "name":"KFC Michelena",                        "lat":-0.24790806756087938,  "lon":-78.53360041850112},
    {"id":28, "name":"KFC Shell Sur Autorápido",             "lat":-0.2672972253383375,   "lon":-78.55220317802146},
    {"id":29, "name":"KFC Santa María Chillogallo",          "lat":-0.2788676819904058,   "lon":-78.55297537617217},
    {"id":30, "name":"KFC Quitumbe",                         "lat":-0.30030492591740493,  "lon":-78.55740957617215},
    {"id":31, "name":"KFC San Rafael",                       "lat":-0.30314416859959653,  "lon":-78.45456756452818},
    {"id":32, "name":"KFC Sangolquí",                        "lat":-0.3144520113681821,   "lon":-78.45058331771331},
    {"id":33, "name":"KFC Guamaní",                          "lat":-0.33770596936109815,  "lon":-78.54910423384315},
    {"id":34, "name":"KFC Mega Santa María",                 "lat":-0.32912936916411534,  "lon":-78.45110261850083},
    {"id":35, "name":"KFC Cumbayá Autorápido",               "lat":-0.19739068189120232,  "lon":-78.43939920685743},
]

ORIGENES = {
    "Banco de Alimentos": {"name": "Banco de Alimentos", "lat": -0.2711541, "lon": -78.5270773},
    "Bodega Norte":       {"name": "Bodega Norte",       "lat": -0.0936,    "lon": -78.4632},
    "Bodega Sur":         {"name": "Bodega Sur",         "lat": -0.3512,    "lon": -78.5589},
}

# Estilos diferenciados por vehículo:
# dash_array y delay distintos hacen que las animaciones sean visualmente distintas
ESTILOS_VRP = [
    {"color": "#2D5A1B", "borde": "#1a3510", "dash": [15, 20], "delay": 500,  "peso": 5},
    {"color": "#E8A020", "borde": "#a06e10", "dash": [20, 15], "delay": 700,  "peso": 5},
    {"color": "#C4391A", "borde": "#8a2710", "dash": [10, 25], "delay": 900,  "peso": 5},
    {"color": "#1e64b4", "borde": "#103d70", "dash": [25, 10], "delay": 1100, "peso": 5},
]

# Offsets laterales en metros para cada vehículo
# Negativo = desplazar a la izquierda, positivo = derecha
OFFSETS_METROS = [-12, -4, 4, 12]


def buscar_kfc(nombre):
    nombre_limpio = nombre.replace("KFC ", "").strip()
    for kfc in KFC_LOCATIONS:
        if kfc["name"] == nombre or kfc["name"] == nombre_limpio:
            return kfc
    nombre_lower = nombre_limpio.lower()
    for kfc in KFC_LOCATIONS:
        if nombre_lower in kfc["name"].lower() or kfc["name"].lower() in nombre_lower:
            return kfc
    return None


def aplicar_offset(coords, offset_m):
    """
    Desplaza cada punto de la polilínea lateralmente offset_m metros,
    usando la perpendicular al segmento local.
    Esto separa visualmente rutas que comparten la misma calle.
    offset_m negativo = izquierda, positivo = derecha (respecto a la dirección de marcha)
    """
    if not coords or len(coords) < 2:
        return coords

    # En Quito (lat ~0), 1 grado lat ≈ 1 grado lon ≈ 111,320 metros
    M_POR_GRADO = 111320.0

    resultado = []
    n = len(coords)

    for i in range(n):
        # Vector dirección usando puntos vecinos
        if i == 0:
            dlat = coords[1][0] - coords[0][0]
            dlon = coords[1][1] - coords[0][1]
        elif i == n - 1:
            dlat = coords[n-1][0] - coords[n-2][0]
            dlon = coords[n-1][1] - coords[n-2][1]
        else:
            dlat = coords[i+1][0] - coords[i-1][0]
            dlon = coords[i+1][1] - coords[i-1][1]

        longitud = math.sqrt(dlat*dlat + dlon*dlon)
        if longitud < 1e-10:
            resultado.append(list(coords[i]))
            continue

        # Perpendicular: rotar 90° el vector dirección
        perp_lat = -dlon / longitud
        perp_lon =  dlat / longitud

        nueva_lat = coords[i][0] + perp_lat * (offset_m / M_POR_GRADO)
        nueva_lon = coords[i][1] + perp_lon * (offset_m / M_POR_GRADO)
        resultado.append([nueva_lat, nueva_lon])

    return resultado


# ─────────────────────────────────────────
# GENERAR MAPA CON RUTA DESDE n8n
# ─────────────────────────────────────────
def generar_mapa_con_ruta(data):
    tipo          = data.get("tipo", "TSP")
    origen_nm     = data.get("origen", "Banco de Alimentos")
    vehiculos     = data.get("vehiculos", [])
    ruta_tsp      = data.get("ruta", [])
    geometria_tsp = data.get("geometria")

    origen = ORIGENES.get(origen_nm, ORIGENES["Banco de Alimentos"])

    quito_map = folium.Map(
        location=[-0.22, -78.50],
        zoom_start=12,
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap &copy; CARTO"
    )

    # ── Sucursales inactivas en gris ──
    rutas_activas = set()
    if tipo == "VRP":
        for v in vehiculos:
            for nombre in v.get("ruta", []):
                rutas_activas.add(nombre.replace("KFC ", "").strip().lower())
    else:
        for nombre in ruta_tsp:
            rutas_activas.add(nombre.replace("KFC ", "").strip().lower())

    for kfc in KFC_LOCATIONS:
        if kfc["name"].lower() not in rutas_activas:
            folium.CircleMarker(
                location=[kfc["lat"], kfc["lon"]],
                radius=6, color="#aaaaaa", fill=True,
                fill_color="#cccccc", fill_opacity=0.6,
                tooltip=kfc["name"],
            ).add_to(quito_map)

    # ── Marcador de origen ──
    folium.Marker(
        location=[origen["lat"], origen["lon"]],
        popup=folium.Popup(
            f"<b>{origen['name']}</b><br>Punto de partida y retorno",
            max_width=200
        ),
        icon=folium.Icon(icon="home", color="orange", prefix="fa"),
    ).add_to(quito_map)

    # ────────────────────────────────────────
    # TSP — una sola ruta
    # ────────────────────────────────────────
    if tipo == "TSP":
        if geometria_tsp and "coordinates" in geometria_tsp:
            coords = [[c[1], c[0]] for c in geometria_tsp["coordinates"]]
        else:
            coords = [[origen["lat"], origen["lon"]]]
            for nombre in ruta_tsp:
                kfc = buscar_kfc(nombre)
                if kfc:
                    coords.append([kfc["lat"], kfc["lon"]])
            coords.append([origen["lat"], origen["lon"]])

        if len(coords) > 1:
            folium.PolyLine(
                locations=coords,
                color="#0a3060", weight=8, opacity=0.3,
            ).add_to(quito_map)
            AntPath(
                locations=coords,
                color="#1e64b4", weight=4, opacity=0.95,
                delay=800, dash_array=[20, 30],
                tooltip="Ruta TSP (incluye retorno al origen)"
            ).add_to(quito_map)

        for i, nombre in enumerate(ruta_tsp):
            kfc = buscar_kfc(nombre)
            if not kfc:
                continue
            num = i + 1
            icon_html = (
                f'<div style="background:#1e64b4;color:white;border-radius:50%;'
                f'width:28px;height:28px;display:flex;align-items:center;'
                f'justify-content:center;font-weight:700;font-size:13px;'
                f'border:2.5px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.35);'
                f'font-family:sans-serif;">{num}</div>'
            )
            folium.Marker(
                location=[kfc["lat"], kfc["lon"]],
                tooltip=f"{num}. {kfc['name']}",
                popup=folium.Popup(
                    f"<b>Parada {num}: {kfc['name']}</b>",
                    max_width=200
                ),
                icon=folium.DivIcon(
                    html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)
                ),
            ).add_to(quito_map)

    # ────────────────────────────────────────
    # VRP — múltiples rutas con offset lateral
    # ────────────────────────────────────────
    else:
        for vi, vehiculo in enumerate(vehiculos):
            estilo      = ESTILOS_VRP[vi % len(ESTILOS_VRP)]
            offset_m    = OFFSETS_METROS[vi % len(OFFSETS_METROS)]
            color       = estilo["color"]
            color_borde = estilo["borde"]
            dash        = estilo["dash"]
            delay       = estilo["delay"]
            peso        = estilo["peso"]

            ruta_v      = vehiculo.get("ruta", [])
            tiempo_v    = vehiculo.get("tiempo_min", 0)
            distancia_v = vehiculo.get("distancia_km", 0)
            geometria_v = vehiculo.get("geometria")
            vid         = vehiculo.get("id", vi + 1)

            # Obtener coordenadas crudas
            if geometria_v and "coordinates" in geometria_v:
                coords_raw = [[c[1], c[0]] for c in geometria_v["coordinates"]]
            else:
                coords_raw = [[origen["lat"], origen["lon"]]]
                for nombre in ruta_v:
                    kfc = buscar_kfc(nombre)
                    if kfc:
                        coords_raw.append([kfc["lat"], kfc["lon"]])
                coords_raw.append([origen["lat"], origen["lon"]])

            # Aplicar offset lateral para separar líneas superpuestas
            coords = aplicar_offset(coords_raw, offset_m)

            h = tiempo_v // 60
            m = tiempo_v % 60
            tiempo_str  = f"{h}h {m}m" if h > 0 else f"{m}min"
            tooltip_ruta = f"Vehículo {vid} — {tiempo_str} · {distancia_v}km"

            if len(coords) > 1:
                # Sombra/borde oscuro debajo para dar profundidad
                folium.PolyLine(
                    locations=coords,
                    color=color_borde,
                    weight=peso + 4,
                    opacity=0.3,
                    tooltip=tooltip_ruta
                ).add_to(quito_map)
                # Línea animada encima
                AntPath(
                    locations=coords,
                    color=color,
                    weight=peso,
                    opacity=0.95,
                    delay=delay,
                    dash_array=dash,
                    tooltip=tooltip_ruta
                ).add_to(quito_map)

            # Marcadores numerados — se dibujan sobre las coordenadas REALES (sin offset)
            # para que los pines queden exactamente sobre la sucursal
            for i, nombre in enumerate(ruta_v):
                kfc = buscar_kfc(nombre)
                if not kfc:
                    continue
                num = i + 1
                icon_html = (
                    f'<div style="background:{color};color:white;border-radius:50%;'
                    f'width:28px;height:28px;display:flex;align-items:center;'
                    f'justify-content:center;font-weight:700;font-size:13px;'
                    f'border:2.5px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.35);'
                    f'font-family:sans-serif;">{num}</div>'
                )
                folium.Marker(
                    location=[kfc["lat"], kfc["lon"]],
                    tooltip=f"V{vid} · {num}. {kfc['name']} — {tiempo_str} · {distancia_v}km",
                    popup=folium.Popup(
                        f"<b>Vehículo {vid} — Parada {num}</b>"
                        f"<br>{kfc['name']}<br>{tiempo_str} · {distancia_v}km",
                        max_width=200
                    ),
                    icon=folium.DivIcon(
                        html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)
                    ),
                ).add_to(quito_map)

    return quito_map._repr_html_()


# ─────────────────────────────────────────
# RUTAS FLASK
# ─────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

@app.route("/n8n", methods=["POST"])
def n8n_proxy():
    """Proxy hacia n8n — recibe respuesta, genera mapa con ruta y devuelve todo"""
    try:
        data = request.json
        response = req.post(N8N_WEBHOOK, json=data, timeout=120)
        result = response.json()
        print("=== DEBUG JUSTIFICACIONES ===")
        print("justificacion:", result.get("justificacion", "VACIO"))
        print("justificacion_algoritmo:", result.get("justificacion_algoritmo", "VACIO"))
        print("justificacion_incidente:", result.get("justificacion_incidente", "VACIO"))
        print("==============================")

        # ── FIX: concatenar justificación del Agente 1 (algoritmo) con la del Agente 2 (incidente) ──
        justif_algoritmo = result.get("justificacion_algoritmo", "")
        justif_incidente = result.get("justificacion_incidente", "")
        justif_base      = result.get("justificacion", "")

        # Prioridad: justif_algoritmo (Agente 1) como base, justif_incidente (Agente 2) como complemento
        partes = []
        if justif_algoritmo:
            partes.append(justif_algoritmo)
        elif justif_base:
            partes.append(justif_base)

        if justif_incidente and justif_incidente not in partes:
            partes.append(f"Gestión de incidente: {justif_incidente}")

        if partes:
            result["justificacion"] = " | ".join(partes)
        # ── fin fix ──

        if "error" not in result:
            result["map_html"] = generar_mapa_con_ruta(result)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n──────────────────────────────────────")
    print("  SADL — Banco de Alimentos Quito")
    print("  Servidor iniciado en:")
    print("  → http://localhost:5000")
    print("──────────────────────────────────────\n")
    app.run(debug=True, port=5000)
