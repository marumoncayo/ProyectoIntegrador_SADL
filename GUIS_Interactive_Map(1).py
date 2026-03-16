#FOLIUM> Library to create the interactive map
#HTML> Code to improve pop-ups design

import folium
from folium import plugins

import branca.element #Libreria complementaria a folium que personalizan los elementos html para add to the map.

#Variables
#--Types of tiles
Thunderforest_OpenCycleMap = "https://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}{r}.png"
#--Attributes
title = "Quito's EcoMap.html"
tiles = Thunderforest_OpenCycleMap
quitos_location = [-0.18990597123329325, -78.44078744533141] #Localiza el centro de Quito
zoom_start = 11
min_lat, min_lon = -0.425, -78.27316924072967
max_lat, max_lon = 0.06, -78.65

#Setting the map
quito_map = folium.Map(location = quitos_location,
                       zoom_start= zoom_start,
                       tiles = tiles,
                       attr='My Data Attribution',
                       min_lat = min_lat,
                       max_lat = max_lat,
                       min_lon = min_lon,
                       max_lon = max_lon,
                       max_bounds = True)

#Limits
folium.CircleMarker(
        location = [max_lat, max_lon], 
        radius = 10,
        color = "blue",
        fill = True,
        fill_color = "light_blue",
        tooltip = "Límite superior derecho"
    ).add_to(quito_map)

folium.CircleMarker(
        location=[min_lat, min_lon],
        radius=10,
        color= "blue",
        fill=True,
        fill_color = "light_blue",
        tooltip= "Límite inferior izquierdo"
    ).add_to(quito_map)

#User localization
plugins.LocateControl(auto_start=True, strings = {"title": "My Location", "popup": "You are Here!"}
                      ,locateOptions = {"setView": True,"maxZoom": False,"watch": True,"timeout": 5000,"enableHighAccuracy": True}
                      ).add_to(quito_map)

#Delimit Area with vectors / Quito
quito_coordinates = [
    (-0.3936152029351594, -78.37869646369681),
    (-0.3936152029351594, -78.3580970984076),
    (-0.29817322947171143, -78.38144304573537),
    (-0.27482757468897884, -78.44392778711266),
    (-0.21852316823017134, -78.45903398832473),
    (-0.23686416911126507, -78.4423588552703),
    (-0.22666808714940312, -78.42924949947458),
    (-0.22885296247080833, -78.42245205572864),
    (-0.2371069325608505, -78.4171112071551),
    (-0.23734969632267736, -78.39016419801943),
    (-0.22375491922551324, -78.36807250584515),
    (-0.19498735847416068, -78.37717622518521),
    (-0.18236360297341808, -78.41310557068515),
    (-0.137209332991237, -78.40970684881218),
    (-0.23965595099651865, -78.33784815789366),
    (-0.23382962015205674, -78.32668092891868),
    (-0.09254050855255143, -78.27618563252032),
    (-0.06874947777928382, -78.28880945666774),
    (-0.045443968536817925, -78.33444943607111),
    (-0.04787162640397338, -78.40776472203545),
    (-0.0444729057101918, -78.4325268385385),
    (-0.0007750584892793347, -78.42815705327324),
    (0.023015993826075953, -78.49807361728449),
    (-0.002717184880458443, -78.52963317753346),
    (-0.022138451746883045, -78.47768128604669),
    (-0.05029928359050287, -78.49564595880379),
    (-0.07166266552468308, -78.49030511014627),
    (-0.06727248981775906, -78.49602162792961),
    (-0.07001906982408536, -78.4891551728332),
    (-0.07688551912216442, -78.49808156445852),
    (-0.07619887424042614, -78.50494801955493),
    (-0.08924512500975411, -78.52760732137307),
    (-0.08718519096801773, -78.53378713095982),
    (-0.11190439126944789, -78.53653371299838),
    (-0.10288731613084806, -78.5180621852871),
    (-0.11411504695905003, -78.51193795734548),
    (-0.12513863296598193, -78.53133134582727),
    (-0.134733231845533, -78.52602368161119),
    (-0.13432495111720974, -78.51581663504183),
    (-0.12758831813058938, -78.5066302931294),
    (-0.1461316506324686, -78.52230870321901),
    (-0.1441895301239671, -78.51114147420785),
    (-0.1609403138266836, -78.51162700590399),
    (-0.16798049425834205, -78.50215913782928),
    (-0.1772605070669342, -78.51942664284611),
    (-0.19656028877638715, -78.5203977062384),
    (-0.2043287481979216, -78.51032292354354),
    (-0.20542118750611335, -78.51469270880878),
    (-0.20299354449820403, -78.52282536471908),
    (-0.20979094398807865, -78.5324146157178),
    (-0.2112475300637948, -78.53022972301574),
    (-0.2540953476639321, -78.55523460533072),
    (-0.25191047638097896, -78.56555215387365),
    (-0.2804351547982303, -78.57514140487238),
    (-0.287475278497686, -78.57065023663141),
    (-0.28723251570811653, -78.57732629745331),
    (-0.27715785544539717, -78.58230299733873),
    (-0.275458514307002, -78.58691554845203),
    (-0.2932622156947786, -78.57478890910691),
    (-0.30270346354749444, -78.57530389323915),
    (-0.3119730443533526, -78.5746172477295),
    (-0.3202126648886882, -78.5744455863521),
    (-0.32639286191159206, -78.58217272240911),
    (-0.3337852549828392, -78.58266638489462),
    (-0.33053831640087483, -78.57453372898433),
    (-0.3392056502854886, -78.58189156749283),
    (-0.35533248724435496, -78.55055593458027),
    (-0.3367560016366895, -78.53759298548906),
    (-0.3285905019341503, -78.52156792240564),
    (-0.31134086265661676, -78.51799545610636),
    (-0.31613810251508057, -78.50554285929174),
    (-0.34961664954131116, -78.49880620865997),
    (-0.3673765624578858, -78.47665691763463),
    (-0.333263067408886, -78.45446578993395),
    (-0.31070585078631147, -78.45068918273203),
    (-0.32348197605688134, -78.41202198888323),
    (-0.3936152029351594, -78.37869646369681),
]
folium.PolyLine(quito_coordinates, tooltip = "Quito Border").add_to(quito_map)

#KFC Markers
kfc_points = [
    # --- Extremo Norte / Mitad del Mundo ---
    {"lat": -0.0087818, "lon": -78.4453248, "name": "KFC - Mitad del Mundo", "address": "Av S/N, Quito"},
    {"lat": -0.0512000, "lon": -78.4557000, "name": "KFC - Pomasqui", "address": "Av. Manuel Córdova Galarza, Quito"},

    # --- Norte ---
    {"lat": -0.0912162, "lon": -78.4724195, "name": "KFC - Carcelén", "address": "Av. Clemente Yerovi Indaburu, Quito"},
    {"lat": -0.1019000, "lon": -78.4226103, "name": "KFC - Calderón", "address": "Carapungo 728, Quito"},
    {"lat": -0.1041555, "lon": -78.4533691, "name": "KFC - Carapungo Gran Akí", "address": "Av. Padre Luis Vaccari, Quito"},
    {"lat": -0.1034903, "lon": -78.4904695, "name": "KFC - El Condado", "address": "Av. de la Prensa y Antonio José de Sucre, Quito"},
    {"lat": -0.1094186, "lon": -78.4449468, "name": "KFC - Llano Grande", "address": "Gabriel García Moreno, Quito"},
    {"lat": -0.1081868, "lon": -78.4524950, "name": "KFC - Portal Shopping", "address": "Av. Simón Bolívar, Portal Shopping, Quito"},
    {"lat": -0.1219195, "lon": -78.4941043, "name": "KFC Cotocollao Autorápido", "address": "Rigoberto Heredia 5545, Quito"},
    {"lat": -0.1255605, "lon": -78.4937082, "name": "KFC La Prensa Autorápido", "address": "Av. La Prensa y Av. Luis G. Tufiño, Quito"},
    {"lat": -0.1267319, "lon": -78.4687395, "name": "KFC - Comité del Pueblo", "address": "Av. Jorge Garcés y Luis Tipan, Quito"},
    {"lat": -0.1291855, "lon": -78.4721921, "name": "KFC - Molineros", "address": "Avenida Juan Molineros, Quito"},
    {"lat": -0.1315482, "lon": -78.4705343, "name": "KFC - Eloy Alfaro", "address": "Eloy Alfaro y Las Anonas esquina, Quito"},
    {"lat": -0.1595204, "lon": -78.4828451, "name": "KFC El Inca Autorápido", "address": "Av. Amazonas, Quito"},
    {"lat": -0.1684425, "lon": -78.4756207, "name": "KFC - Granados Outlet", "address": "Av. de los Granados, Quito"},
    {"lat": -0.1763811, "lon": -78.4804993, "name": "KFC Quicentro Norte", "address": "Av. de los Shyris, Quito"},
    {"lat": -0.1770162, "lon": -78.4847379, "name": "KFC - CCI", "address": "Av. Río Amazonas N36-152, Quito"},

    # --- Centro-Norte ---
    {"lat": -0.1889797, "lon": -78.4875237, "name": "KFC - El Jardín", "address": "Mall El Jardín, Av. Río Amazonas, Quito"},
    {"lat": -0.1978847, "lon": -78.4956370, "name": "KFC - Colón Autorápido", "address": "Av. Cristóbal Colón, Quito"},
    {"lat": -0.2017204, "lon": -78.4865170, "name": "KFC - Baca Ortiz", "address": "Av. Cristóbal Colón, Quito"},
    {"lat": -0.2083473, "lon": -78.4955766, "name": "KFC - Patria", "address": "Av. 6 de Diciembre, Quito"},

    # --- Centro ---
    {"lat": -0.2183534, "lon": -78.5080963, "name": "KFC - Colonial", "address": "Guayaquil N9-02 y Esmeraldas, Quito"},
    {"lat": -0.2204288, "lon": -78.5142519, "name": "KFC - San Francisco de Quito", "address": "Sebastián de Benalcázar, Quito"},

    # --- Centro-Sur ---
    {"lat": -0.2436176, "lon": -78.4826472, "name": "KFC - MASGAS", "address": "Av. Simón Bolívar, Quito"},
    {"lat": -0.2444214, "lon": -78.5180541, "name": "KFC - Villaflora", "address": "Calle El Corazón y Casitagua, Quito"},
    {"lat": -0.2481441, "lon": -78.5336326, "name": "KFC - Teniente Michelena", "address": "Av. Teniente Michelena y Luis Minacho, Quito"},
    {"lat": -0.2523939, "lon": -78.5227192, "name": "KFC - El Recreo", "address": "Av. Pedro Vicente Maldonado S11-122, Quito"},

    # --- Sur ---
    {"lat": -0.2677716, "lon": -78.5376602, "name": "KFC - Solanda", "address": "Benancio Estandoque, Quito"},
    {"lat": -0.2675118, "lon": -78.5521388, "name": "KFC - Mariscal Sucre", "address": "Av. Mariscal Sucre, Quito"},
    {"lat": -0.2791359, "lon": -78.5529861, "name": "KFC - Santa María Chillogallo", "address": "Av. Mariscal Sucre, Quito"},
    {"lat": -0.2848952, "lon": -78.5442953, "name": "KFC - Morán Valverde", "address": "Ave Morán Valverde, Quito"},
    {"lat": -0.2858080, "lon": -78.5432550, "name": "KFC - Quicentro Sur Patio", "address": "Av. Morán Valverde, C.C. Quicentro Sur, Quito"},
    {"lat": -0.3005195, "lon": -78.5574203, "name": "KFC - Quitumbe", "address": "Av. Guayanay Ñan, Quito"},

    # --- Valle (Sangolquí / San Rafael) ---
    {"lat": -0.2152175, "lon": -78.4062397, "name": "KFC - Tumbaco", "address": "Av. Interoceanica, Quito"},
    {"lat": -0.3033802, "lon": -78.4544710, "name": "KFC San Rafael Autorápido", "address": "Av. Gral. Rumiñahui, Quito"},
    {"lat": -0.3080878, "lon": -78.4505367, "name": "KFC - San Luis Shopping", "address": "Av. San Luis, Sangolquí"},
    {"lat": -0.3146344, "lon": -78.4506262, "name": "KFC - Sangolquí", "address": "Av. General Enríquez, Sangolquí"},
    {"lat": -0.3293654, "lon": -78.4511348, "name": "KFC Mega Santa María", "address": "Av. General Enríquez y García Moreno, Sangolquí"},
]

groupKFC = folium.FeatureGroup(name="KFC Quito").add_to(quito_map)

for point in kfc_points:
    html = f"""
        <h4 style="font-family: Arial; font-weight: bold;">{point.get("name", "")}</h4>
        <p style="font-family: Arial;">
        <b>Address:</b> {point.get("address", "N/A")}<br>
        </p>
    """
    iframe = folium.IFrame(html, width=250, height=120)
    custom_popup = folium.Popup(iframe, max_width=250)

    folium.Marker(
        location=[point["lat"], point["lon"]],
        popup=custom_popup,
        tooltip=point["name"],
        icon=folium.Icon(icon="cutlery", color="red"),
    ).add_to(groupKFC)

folium.LayerControl().add_to(quito_map)
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px;
    left: 50px;
    width: 180px;
    height: 110px;
    z-index:9999;
    font-size:14px;
    background-color: #ffffff;
    border:2px solid grey; 
    border-radius: 8px; 
    padding: 10px;
    ">
    <h5 style="font-family: Arial; margin-top: 0;"><b>Puntos de Reciclaje</b></h6>
    <p style="font-family: Arial; margin-bottom: 5px;"><i class="fa fa-leaf" style="color:green"></i>&nbsp; Puntos GIRA</p>
    <p style="font-family: Arial; margin-bottom: 5px;"><i class="fa fa-leaf" style="color:orange"></i>&nbsp; Puntos Carolina</p>
    <p style="font-family: Arial; margin-bottom: 5px;"><i class="fa fa-leaf" style="color:blue"></i>&nbsp; Otros Puntos</p>
</div>
"""
legend = branca.element.Element(legend_html)
quito_map.get_root().html.add_child(legend)

#Saving map
quito_map.save(r"c:\Users\maeul\Documents\USFQ\10 SEMESTRE\TESIS\Quito's EcoMap.html")




