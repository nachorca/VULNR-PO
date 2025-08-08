import os
from datetime import datetime
from dateutil import tz
import yaml  # <- para leer sources/sources.yaml

# --- Rutas base ---
ROOT = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else "."
DAILY_DIR = os.path.join(ROOT, "daily")
DATA_DIR = os.path.join(ROOT, "data")
SOURCES_YAML = os.path.join(ROOT, "sources", "sources.yaml")

# --- Utilidades de lectura ---
def read_text(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return default

def read_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def sources_to_list(d, prefix=""):
    """Convierte el dict del YAML en <li> con enlaces. Recorre recursivamente."""
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                items += sources_to_list(v, prefix + k + ".")
            else:
                # v se asume URL
                items.append(f'{prefix}{k}: <a href="{v}" target="_blank" rel="noopener">{k}</a>')
    return items

# --- Fecha/hora local (Europe/Madrid) ---
TZ = tz.gettz("Europe/Madrid")
now = datetime.now(TZ)
Y, M = now.strftime("%Y"), now.strftime("%m")
DATE_STR = now.strftime("%d/%m/%Y")
TIME_STR = now.strftime("%H:%M")
D_ISO = now.strftime("%Y-%m-%d")

# --- Salida: daily/AAAA/MM/AAAA-MM-DD-campello-sitrep.html ---
out_dir = os.path.join(DAILY_DIR, Y, M)
os.makedirs(out_dir, exist_ok=True)
out_html = os.path.join(out_dir, f"{D_ISO}-campello-sitrep.html")

# --- Cargar datos dinámicos del repo ---
RESUMEN = read_text(
    os.path.join(DATA_DIR, "resumen.txt"),
    "Breve descripción de los eventos previstos en el pueblo, actividades culturales, sociales y mercantiles…"
)

SOURCES = read_yaml(SOURCES_YAML)
SOURCES_LIST_HTML = "\n".join(f"<li>{x}</li>" for x in sources_to_list(SOURCES)) or "<li>(Configura tus fuentes en sources/sources.yaml)</li>"

# --- HTML ---
logo_rel = "../../assets/logo.png"  # desde daily/AAAA/MM/ hasta assets/

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Alicante Segura – Informe Diario (Campello) {DATE_STR}</title>
<style>
:root {{ --gold:#c6a558; --border:#e5e5e5; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }}
header {{ background: linear-gradient(90deg, #004e92, #000428); color:#fff; padding:20px; border-bottom:4px solid var(--gold); }}
.wrap {{ display:flex; align-items:center; gap:20px; max-width:1100px; margin:auto; }}
.wrap img {{ width:140px; height:auto; border-radius:10px; border:2px solid #fff; }}
h1 {{ margin:0 0 6px 0; font-size:28px; font-weight:700; }}
h2 {{ margin:24px 0 10px; font-size:20px; font-weight:700; border-bottom:1px solid var(--border); padding-bottom:6px; }}
.tag {{ color:#eee; line-height:1.5; }}
main {{ max-width:1100px; margin:0 auto; padding:24px; }}
.card {{ border:1px solid var(--border); border-radius:12px; padding:14px 16px; background:#fafafa; }}
a {{ color:#0a58ca; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <img src="{logo_rel}" alt="SantiagoLegalConsulting">
    <div>
      <h1>📄 Alicante Segura</h1>
      <div class="tag">
        <b>Informe Diario de Seguridad y Prevención – Campello</b><br>
        <b>🗓️ Fecha:</b> {DATE_STR} &nbsp;|&nbsp;
        <b>🕒 Hora de emisión:</b> {TIME_STR} (hora local) &nbsp;|&nbsp;
        <b>📧</b> info@santiagolegalconsulting.es
      </div>
    </div>
  </div>
</header>

<main>
  <!-- 🟢 1. Resumen General del Día (lee data/resumen.txt) -->
  <section>
    <h2>🟢 1. Resumen General del Día</h2>
    <div class="card">
      <p>{RESUMEN}</p>
    </div>
  </section>

  <!-- 🌦️ 2. Predicción Meteorológica (AEMET) -->
  <section>
    <h2>🌦️ 2. Predicción Meteorológica (AEMET)</h2>
    <div class="card">
      <p>Estado del cielo, lluvia, viento, temperaturas máximas y mínimas, avisos activos y recomendaciones.</p>
      <p><b>Fuente:</b> <a href="https://www.aemet.es/es/eltiempo/prediccion/municipios/campello-el-id03050" target="_blank" rel="noopener">AEMET – Campello</a></p>
    </div>
  </section>

  <!-- 🚦 3. Tráfico y Accesos -->
  <section>
    <h2>🚦 3. Tráfico y Accesos</h2>
    <div class="card">
      <ul>
        <li>Estado de las principales vías: N-332 y A-70.</li>
        <li>Accesos a playas y centros urbanos.</li>
        <li>Aparcamiento y transporte público (TRAM, buses).</li>
      </ul>
      <p><b>Fuente:</b> <a href="https://infocar.dgt.es/etraffic/" target="_blank" rel="noopener">DGT – Estado del tráfico</a></p>
    </div>
  </section>

  <!-- 🔶 4. Sucesos en Campello (últimas 24h) -->
  <section>
    <h2>🔶 4. Sucesos en Campello (últimas 24h)</h2>
    <div class="card">
      <p>(Aquí añadiremos el mapa interactivo y la tabla de sucesos en el siguiente paso.)</p>
    </div>
  </section>

  <!-- 🏖️ 5. Estado de las Playas y el Mar -->
  <section>
    <h2>🏖️ 5. Estado de las Playas y el Mar</h2>
    <div class="card">
      <ul>
        <li>Bandera del día, oleaje, medusas/corrientes.</li>
        <li>Condiciones para el baño y protección solar.</li>
      </ul>
      <p><b>Fuente:</b> <a href="https://www.aemet.es/es/eltiempo/prediccion/playas/carrer-la-mar-0305013" target="_blank" rel="noopener">AEMET – Playas (Carrer La Mar)</a></p>
    </div>
  </section>

  <!-- 🛍️ 6. Información para Comercios y Empresas -->
  <section>
    <h2>🛍️ 6. Información para Comercios y Empresas</h2>
    <div class="card">
      <ul>
        <li>Cortes de suministro (agua, luz, telecomunicaciones).</li>
        <li>Eventos que puedan afectar la actividad comercial.</li>
        <li>Avisos preventivos u oportunidades.</li>
      </ul>
    </div>
  </section>

  <!-- 📣 7. Eventos y Actividades del Día -->
  <section>
    <h2>📣 7. Eventos y Actividades del Día</h2>
    <div class="card">
      <ul>
        <li>Actividades, fiestas, actos públicos, mercadillos, eventos deportivos.</li>
        <li>Consulta: <a href="https://www.elcampello.es/es/agenda/" target="_blank" rel="noopener">Agenda del Ayuntamiento</a></li>
      </ul>
    </div>
  </section>

  <!-- ⚠️ 8. Recomendaciones Generales -->
  <section>
    <h2>⚠️ 8. Recomendaciones Generales</h2>
    <div class="card">
      <ul>
        <li>Mantén hidratación y protección solar.</li>
        <li>Planifica desplazamientos evitando horas punta.</li>
        <li>Atiende a avisos oficiales (112 CV).</li>
      </ul>
    </div>
  </section>

  <!-- 🔗 9. Enlaces y Recursos de Interés (auto desde sources.yaml) -->
  <section>
    <h2>🔗 9. Enlaces y Recursos de Interés</h2>
    <div class="card">
      <ul>
        {SOURCES_LIST_HTML}
      </ul>
    </div>
  </section>
</main>
</body>
</html>
"""

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {out_html}")
