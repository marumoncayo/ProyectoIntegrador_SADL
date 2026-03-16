"""
SADL — Servidor Flask
Banco de Alimentos Quito

Cómo iniciar:
  pip install flask folium
  python servidor.py

Luego abre en el navegador: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
import folium
import json
import math
import os

app = Flask(__name__, static_folder=".")

# ─────────────────────────────────────────
# DATOS KFC
# ─────────────────────────────────────────
KFC_LOCATIONS = [
    {"id":1,  "name":"Mitad del Mundo",       "lat":-0.0087818, "lon":-78.4453248, "zona":"norte"},
    {"id":2,  "name":"Pomasqui",              "lat":-0.0641,    "lon":-78.4448,    "zona":"norte"},
    {"id":3,  "name":"Carcelén",              "lat":-0.0786,    "lon":-78.4632,    "zona":"norte"},
    {"id":4,  "name":"Calderón",              "lat":-0.0701,    "lon":-78.4268,    "zona":"norte"},
    {"id":5,  "name":"Carapungo",             "lat":-0.0841,    "lon":-78.4356,    "zona":"norte"},
    {"id":6,  "name":"El Condado",            "lat":-0.0936,    "lon":-78.5001,    "zona":"norte"},
    {"id":7,  "name":"Llano Grande",          "lat":-0.0521,    "lon":-78.4152,    "zona":"norte"},
    {"id":8,  "name":"Portal Shopping",       "lat":-0.1124,    "lon":-78.4987,    "zona":"norte"},
    {"id":9,  "name":"Cotocollao",            "lat":-0.1034,    "lon":-78.4889,    "zona":"norte"},
    {"id":10, "name":"La Prensa",             "lat":-0.1312,    "lon":-78.4901,    "zona":"norte"},
    {"id":11, "name":"Comité del Pueblo",     "lat":-0.0978,    "lon":-78.4612,    "zona":"norte"},
    {"id":12, "name":"Molineros",             "lat":-0.1456,    "lon":-78.4801,    "zona":"norte"},
    {"id":13, "name":"Eloy Alfaro",           "lat":-0.1589,    "lon":-78.4745,    "zona":"norte"},
    {"id":14, "name":"El Inca",               "lat":-0.1623,    "lon":-78.4634,    "zona":"norte"},
    {"id":15, "name":"Granados Outlet",       "lat":-0.1534,    "lon":-78.4512,    "zona":"norte"},
    {"id":16, "name":"Quicentro Norte",       "lat":-0.1712,    "lon":-78.4823,    "zona":"norte"},
    {"id":17, "name":"CCI",                   "lat":-0.1934,    "lon":-78.4867,    "zona":"centro-norte"},
    {"id":18, "name":"El Jardín",             "lat":-0.1987,    "lon":-78.4923,    "zona":"centro-norte"},
    {"id":19, "name":"Colón Autorápido",      "lat":-0.2098,    "lon":-78.4934,    "zona":"centro-norte"},
    {"id":20, "name":"Baca Ortiz",            "lat":-0.2134,    "lon":-78.5012,    "zona":"centro-norte"},
    {"id":21, "name":"Patria",                "lat":-0.2201,    "lon":-78.5023,    "zona":"centro-norte"},
    {"id":22, "name":"Colonial",              "lat":-0.2312,    "lon":-78.5134,    "zona":"centro"},
    {"id":23, "name":"San Francisco",         "lat":-0.2198,    "lon":-78.5156,    "zona":"centro"},
    {"id":24, "name":"MASGAS",                "lat":-0.2456,    "lon":-78.5201,    "zona":"sur"},
    {"id":25, "name":"Villaflora",            "lat":-0.2634,    "lon":-78.5189,    "zona":"sur"},
    {"id":26, "name":"Tte. Michelena",        "lat":-0.2712,    "lon":-78.5234,    "zona":"sur"},
    {"id":27, "name":"El Recreo",             "lat":-0.2834,    "lon":-78.5312,    "zona":"sur"},
    {"id":28, "name":"Solanda",               "lat":-0.3012,    "lon":-78.5389,    "zona":"sur"},
    {"id":29, "name":"Mariscal Sucre",        "lat":-0.3156,    "lon":-78.5423,    "zona":"sur"},
    {"id":30, "name":"Sta. María Chillog.",   "lat":-0.3234,    "lon":-78.5478,    "zona":"sur"},
    {"id":31, "name":"Morán Valverde",        "lat":-0.3389,    "lon":-78.5534,    "zona":"sur"},
    {"id":32, "name":"Quicentro Sur Patio",   "lat":-0.3512,    "lon":-78.5589,    "zona":"sur"},
    {"id":33, "name":"Quitumbe",              "lat":-0.3678,    "lon":-78.5634,    "zona":"sur"},
    {"id":34, "name":"Tumbaco",               "lat":-0.2134,    "lon":-78.3978,    "zona":"valles"},
    {"id":35, "name":"San Rafael Autoráp.",   "lat":-0.3012,    "lon":-78.4234,    "zona":"valles"},
    {"id":36, "name":"San Luis Shopping",     "lat":-0.3234,    "lon":-78.4312,    "zona":"valles"},
    {"id":37, "name":"Sangolquí",             "lat":-0.3389,    "lon":-78.4489,    "zona":"valles"},
    {"id":38, "name":"Mega Santa María",      "lat":-0.2456,    "lon":-78.4312,    "zona":"valles"},
]

ORIGENES = {
    "banco": {"name": "Banco de Alimentos", "lat": -0.1978, "lon": -78.5023},
    "norte": {"name": "Bodega Norte",       "lat": -0.0936, "lon": -78.4632},
    "sur":   {"name": "Bodega Sur",         "lat": -0.3512, "lon": -78.5589},
}

# ─────────────────────────────────────────
# TSP — Vecino Más Cercano + 2-opt
# ─────────────────────────────────────────
def haversine(a, b):
    R = 6371
    dlat = math.radians(b["lat"] - a["lat"])
    dlon = math.radians(b["lon"] - a["lon"])
    h = math.sin(dlat/2)**2 + math.cos(math.radians(a["lat"])) * math.cos(math.radians(b["lat"])) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(h))

def nearest_neighbor(origin, stops):
    route = []
    remaining = stops[:]
    current = origin
    while remaining:
        nearest = min(remaining, key=lambda s: haversine(current, s))
        route.append(nearest)
        current = nearest
        remaining.remove(nearest)
    return route

def two_opt(route, origin):
    full = [origin] + route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(full) - 1):
            for j in range(i + 1, len(full)):
                d1 = haversine(full[i-1], full[i])
                d2 = haversine(full[j-1], full[j]) if j < len(full) else 0
                new = full[:i] + full[i:j+1][::-1] + full[j+1:]
                d3 = haversine(new[i-1], new[i])
                d4 = haversine(new[j-1], new[j]) if j < len(new) else 0
                if d3 + d4 < d1 + d2 - 0.001:
                    full = new
                    improved = True
    return full[1:]  # quitar el origen

def total_distance(origin, route):
    all_pts = [origin] + route
    return sum(haversine(all_pts[i], all_pts[i+1]) for i in range(len(all_pts)-1))

def estimate_time(dist_km, n_stops):
    drive_min = (dist_km / 25) * 60   # velocidad urbana Quito ~25 km/h
    stop_min  = n_stops * 12           # ~12 min por parada de carga
    return round(drive_min + stop_min)

# ─────────────────────────────────────────
# GENERAR MAPA FOLIUM CON RUTA
# ─────────────────────────────────────────
def generate_map(origin, route):
    # Centro del mapa = punto medio entre todos los puntos
    all_pts = [origin] + route
    center_lat = sum(p["lat"] for p in all_pts) / len(all_pts)
    center_lon = sum(p["lon"] for p in all_pts) / len(all_pts)

    quito_map = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB positron")

    # Todas las sucursales KFC en gris (inactivas)
    for kfc in KFC_LOCATIONS:
        is_in_route = any(k["id"] == kfc["id"] for k in route)
        if not is_in_route:
            folium.CircleMarker(
                location=[kfc["lat"], kfc["lon"]],
                radius=6,
                color="#aaaaaa",
                fill=True,
                fill_color="#cccccc",
                fill_opacity=0.6,
                tooltip=kfc["name"],
            ).add_to(quito_map)

    # Línea de ruta
    route_coords = [[origin["lat"], origin["lon"]]] + [[s["lat"], s["lon"]] for s in route]
    folium.PolyLine(
        locations=route_coords,
        color="#2D5A1B",
        weight=4,
        opacity=0.85,
        dash_array="8 5",
        tooltip="Ruta óptima TSP"
    ).add_to(quito_map)

    # Marcador de origen
    folium.Marker(
        location=[origin["lat"], origin["lon"]],
        tooltip=f"📦 {origin['name']} (Origen)",
        popup=folium.Popup(f"<b>📦 {origin['name']}</b><br>Punto de partida", max_width=200),
        icon=folium.Icon(icon="home", color="orange", prefix="fa"),
    ).add_to(quito_map)

    # Marcadores de ruta numerados
    for i, stop in enumerate(route):
        num = i + 1
        icon_html = f"""
        <div style="
            background:#E4002B;color:white;border-radius:50%;
            width:28px;height:28px;display:flex;align-items:center;
            justify-content:center;font-weight:700;font-size:13px;
            border:2.5px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.35);
            font-family:sans-serif;">{num}</div>
        """
        folium.Marker(
            location=[stop["lat"], stop["lon"]],
            tooltip=f"{num}. {stop['name']}",
            popup=folium.Popup(f"<b>Parada {num}: {stop['name']}</b><br>Zona: {stop['zona']}", max_width=200),
            icon=folium.DivIcon(html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)),
        ).add_to(quito_map)

    return quito_map._repr_html_()


# ─────────────────────────────────────────
# RUTAS FLASK
# ─────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data     = request.json
    origen_k = data.get("origen", "banco")
    zona_v   = data.get("zona", "todas")
    capacidad = data.get("capacidad", "medium")
    tiempo   = data.get("tiempo", "none")
    obs      = data.get("observaciones", "")

    origin = ORIGENES.get(origen_k, ORIGENES["banco"])

    # Filtrar por zona
    if zona_v == "todas":
        selected = KFC_LOCATIONS[:]
    else:
        selected = [k for k in KFC_LOCATIONS if k["zona"] == zona_v]

    # Limitar según capacidad
    max_stops = {"small": 6, "medium": 10, "large": 15}.get(capacidad, 10)
    if len(selected) > max_stops:
        selected = selected[:max_stops]

    if not selected:
        return jsonify({"error": "No hay sucursales para la zona seleccionada"}), 400

    # TSP
    nn_route  = nearest_neighbor(origin, selected)
    opt_route = two_opt(nn_route, origin) if len(nn_route) > 2 else nn_route

    dist_km   = total_distance(origin, opt_route)
    time_min  = estimate_time(dist_km, len(opt_route))

    # Algoritmo info
    n = len(opt_route)
    if n <= 1:
        algo_name = "Directo"
        algo_text = "Con una sola parada no se requiere optimización combinatoria."
    elif n <= 8:
        algo_name = "NN + 2-opt"
        algo_text = f"Para {n} paradas, Vecino Más Cercano construye la ruta inicial en O(n²) y 2-opt elimina cruces de aristas hasta alcanzar un óptimo local, con soluciones dentro del 5–15% del óptimo global."
    else:
        algo_name = "NN + 2-opt*"
        algo_text = f"Para {n} paradas se aplica Vecino Más Cercano con 2-opt. La solución está dentro del 10–20% del óptimo teórico. Para instancias mayores se recomendaría OR-opt o algoritmos genéticos."

    # Generar mapa Folium
    map_html = generate_map(origin, opt_route)

    return jsonify({
        "origen":    origin["name"],
        "route":     [{"name": s["name"], "zona": s["zona"]} for s in opt_route],
        "dist_km":   round(dist_km, 1),
        "time_min":  time_min,
        "algo_name": algo_name,
        "algo_text": algo_text,
        "map_html":  map_html,
    })


if __name__ == "__main__":
    print("\n──────────────────────────────────────")
    print("  SADL — Banco de Alimentos Quito")
    print("  Servidor iniciado en:")
    print("  → http://localhost:5000")
    print("──────────────────────────────────────\n")
    app.run(debug=True, port=5000)
