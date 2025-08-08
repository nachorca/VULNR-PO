import os
from datetime import datetime
from dateutil import tz

# Rutas base
ROOT = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else "."
DAILY_DIR = os.path.join(ROOT, "daily")

# Fecha/hora local (Europe/Madrid)
TZ = tz.gettz("Europe/Madrid")
now = datetime.now(TZ)
Y, M = now.strftime("%Y"), now.strftime("%m")
DATE_STR = now.strftime("%d/%m/%Y")
TIME_STR = now.strftime("%H:%M")
D_ISO = now.strftime("%Y-%m-%d")

# Salida: daily/AAAA/MM/AAAA-MM-DD-campello-sitrep.html
out_dir = os.path.join(DAILY_DIR, Y, M)
os.makedirs(out_dir, exist_ok=True)
out_html = os.path.join(out_dir, f"{D_ISO}-campello-sitrep.html")

logo_rel = "../../assets/logo.png"  # desde daily/AAAA/MM/ a assets/

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Alicante Segura – Informe Diario (Campello) {DATE_STR}</title>
<style>
:root {{ --gold:#c6a558; --border:#e5e5e5; }}
body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }}
header {{ background: linear-gradient(90deg, #004e92, #000428); color:#fff; padding:20px; border-bottom:4px solid var(--gold); }}
.wrap {{ display:flex; align-items:center; gap:20px; max-width:1100px; margin:auto; }}
.wrap img {{ width:140px; height:auto; border-radius:10px; border:2px solid #fff; }}
h1 {{ margin:0 0 6px 0; font-size:28px; font-weight:700; }}
h2 {{ margin:5px 0 10px; font-size:20px; font-weight:400; }}
.tag {{ color:#eee; line-height:1.5; }}
main {{ max-width:1100px; margin:0 auto; padding:24px; }}
.card {{ border:1px solid var(--border); border-radius:12px; padding:14px 16px; background:#fafafa; }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <img src="{logo_rel}" alt="SantiagoLegalConsulting">
    <div>
      <h1>📄 Alicante Segura</h1>
      <h2>Informe Diario de Seguridad y Prevención – Campello</h2>
      <div class="tag">
        <b>🗓️ Fecha:</b> {DATE_STR} &nbsp;|&nbsp;
        <b>🕒 Hora de emisión:</b> {TIME_STR} (hora local) &nbsp;|&nbsp;
        <b>📧</b> info@santiagolegalconsulting.es
      </div>
    </div>
  </div>
</header>
<main>
  <div class="card">
    <p>Plantilla mínima generada correctamente. En el siguiente paso añadiremos secciones.</p>
  </div>
</main>
</body>
</html>
"""

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {out_html}")
