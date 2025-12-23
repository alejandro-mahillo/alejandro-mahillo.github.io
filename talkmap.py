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

# Collect the Markdown files
g = glob.glob("_talks/*.md")

# CRÍTICO: Pon un user_agent único
geocoder = Nominatim(user_agent="alejandro_mahillo_academic_map_v2") 

# DICCIONARIO PARA AGRUPAR
# Estructura: { "Nombre Ciudad": { 'lat': 0.0, 'lon': 0.0, 'talks': ["HTML Charla 1", "HTML Charla 2"] } }
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

    # Si no tiene location, saltamos
    if 'location' not in data or not data['location']:
        continue

    # Extraemos datos
    title = data.get('title', 'Untitled').strip()
    venue = data.get('venue', '').strip()
    location_raw = data.get('location', '').strip() # Esta será nuestra CLAVE ÚNICA
    type_event = data.get('type', 'Talk').strip()   # Por si quieres distinguir Posters

    # Preparamos el HTML individual para ESTA charla
    # Añadimos un pequeño estilo para separar fecha o tipo si quisieras
    single_talk_html = f"<div style='margin-bottom:8px;'><b>{title}</b><br/><i style='font-size:0.9em;'>{venue}</i><br/><span style='font-size:0.8em; color:#666;'>[{type_event}]</span></div>"

    # --- LÓGICA DE AGRUPACIÓN ---
    
    # CASO A: Ya hemos geolocalizado esta ciudad antes
    if location_raw in grouped_locations:
        # Solo añadimos el HTML de la charla a la lista existente
        grouped_locations[location_raw]['talks'].append(single_talk_html)
        print(f"[CACHE] {location_raw} (Añadida charla a ubicación existente)")

    # CASO B: Es una ciudad nueva
    else:
        try:
            # Pausa para respetar a la API
            if len(grouped_locations) > 0: 
                time.sleep(1) 
            
            location_data = geocoder.geocode(location_raw, timeout=TIMEOUT)
            
            if location_data:
                # Creamos la entrada nueva en el diccionario
                grouped_locations[location_raw] = {
                    'lat': location_data.latitude,
                    'lon': location_data.longitude,
                    'talks': [single_talk_html] # Lista con la primera charla
                }
                print(f"[GEO]  {location_raw} -> {location_data.address}")
            else:
                print(f"[FAIL] No encontrado: {location_raw}")

        except (ValueError, GeocoderTimedOut, GeocoderUnavailable) as ex:
            print(f"[ERROR] {location_raw}: {ex}")
        except Exception as ex:
            print(f"[CRITICAL] {location_raw}: {ex}")


# --- 2. GENERACIÓN DEL ARCHIVO JS ---
print(f"\nGenerando {OUTPUT_FILE} con charlas agrupadas...")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

js_data = []

# Recorremos nuestro diccionario agrupado para generar el formato final de Leaflet
for loc_name, data in grouped_locations.items():
    # Unimos todas las charlas de esa ciudad con una línea separadora (<hr>)
    # Si hay muchas charlas, limitamos el ancho del popup para que no se vea gigante
    combined_html = f"<div style='min-width: 200px; max-height: 300px; overflow-y: auto;'>"
    
    # Unimos las charlas. Si hay más de una, ponemos separadores
    combined_html += "<hr style='margin: 5px 0; border: 0; border-top: 1px solid #ccc;'/>".join(data['talks'])
    
    combined_html += f"<br/><small><b>Location:</b> {loc_name}</small></div>"

    js_data.append([combined_html, data['lat'], data['lon']])

output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("var addressPoints = ")
    json.dump(js_data, f, ensure_ascii=False)
    f.write(";")

print(f"¡Hecho! Archivo guardado en: {output_path}")