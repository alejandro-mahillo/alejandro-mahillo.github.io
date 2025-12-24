# Leaflet cluster map of talk locations
#
# INSTRUCCIONES:
# 1. Instala dependencias: pip install python-frontmatter geopy
# 2. Ejecuta desde la raíz: python talkmap.py

import frontmatter
import glob
import json
import os
import time
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Configuración
TIMEOUT = 10
OUTPUT_FOLDER = "talkmap"
OUTPUT_FILE = "org-locations.js"

# --- ZONA DE CORRECCIONES MANUALES ---
# Si el mapa no encuentra bien un sitio, defínelo aquí.
# Clave: Lo que tienes escrito en el YAML (location).
# Valor: Lo que queremos que busque en el mapa (más específico).
MANUAL_FIXES = {
    # HUESCA: Buscamos la Catedral para forzar el centro de la ciudad
    "Huesca, Spain": "Uesca, Spain",
    
    # AMES: Buscamos la Universidad directamente
    "Ames, Iowa, U.S.A.": "Iowa State University, Ames, Iowa, USA",
}

# Collect the Markdown files
g = glob.glob("_talks/*.md")

# User Agent
geocoder = Nominatim(user_agent="alejandro_mahillo_academic_map_v3") 

# DICCIONARIO PARA AGRUPAR
grouped_locations = {}

print(f"Procesando {len(g)} archivos...")

# --- 1. PROCESADO Y GEOLOCALIZACIÓN ---
for file in g:
    try:
        data = frontmatter.load(file)
        data = data.to_dict()
    except Exception as e:
        print(f"Error leyendo {file}: {e}")
        continue

    if 'location' not in data or not data['location']:
        continue

    # Extraemos datos
    title = data.get('title', 'Untitled').strip()
    venue = data.get('venue', '').strip()
    location_raw = data.get('location', '').strip() # Esta es la clave VISUAL
    type_event = data.get('type', 'Talk').strip()

    # Preparamos el HTML
    single_talk_html = f"<div style='margin-bottom:8px;'><b>{title}</b><br/><i style='font-size:0.9em;'>{venue}</i><br/><span style='font-size:0.8em; color:#666;'>[{type_event}]</span></div>"

    # Definimos qué vamos a buscar en el mapa
    # Si la localización está en nuestra lista de FIXES, usamos la versión corregida
    search_query = MANUAL_FIXES.get(location_raw, location_raw)

    # --- LÓGICA DE AGRUPACIÓN ---
    
    # Usamos location_raw como clave para agrupar (para que el popup diga lo que tú escribiste)
    if location_raw in grouped_locations:
        grouped_locations[location_raw]['talks'].append(single_talk_html)
        print(f"[CACHE] {location_raw} (Añadido a grupo existente)")

    else:
        try:
            if len(grouped_locations) > 0: 
                time.sleep(1) 
            
            # Buscamos usando la QUERY OPTIMIZADA (ej: Iowa State University)
            location_data = geocoder.geocode(search_query, timeout=TIMEOUT)
            
            if location_data:
                grouped_locations[location_raw] = {
                    'lat': location_data.latitude,
                    'lon': location_data.longitude,
                    'talks': [single_talk_html]
                }
                # Mostramos la diferencia si hubo corrección
                if search_query != location_raw:
                     print(f"[FIXED] {location_raw} -> Buscado como: '{search_query}' -> {location_data.address}")
                else:
                     print(f"[GEO]   {location_raw} -> {location_data.address}")
            else:
                print(f"[FAIL] No encontrado: {search_query}")

        except (ValueError, GeocoderTimedOut, GeocoderUnavailable) as ex:
            print(f"[ERROR] {location_raw}: {ex}")
        except Exception as ex:
            print(f"[CRITICAL] {location_raw}: {ex}")


# --- 2. GENERACIÓN DEL ARCHIVO JS ---
print(f"\nGenerando {OUTPUT_FILE}...")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

js_data = []

for loc_name, data in grouped_locations.items():
    combined_html = f"<div style='min-width: 200px; max-height: 300px; overflow-y: auto;'>"
    combined_html += "<hr style='margin: 5px 0; border: 0; border-top: 1px solid #ccc;'/>".join(data['talks'])
    combined_html += f"<br/><small><b>Location:</b> {loc_name}</small></div>"

    js_data.append([combined_html, data['lat'], data['lon']])

output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("var addressPoints = ")
    json.dump(js_data, f, ensure_ascii=False)
    f.write(";")

print(f"¡Hecho! Archivo guardado en: {output_path}")