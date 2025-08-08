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

html = f"""
### 🟢 1. Resumen General del Día
Breve descripción de los eventos previstos en el pueblo, actividades culturales, sociales, mercantiles, etc.

### 🌦️ 2. Predicción Meteorológica (AEMET)
- Estado del cielo, lluvia, viento, temperaturas máximas y mínimas.  
- Avisos activos y recomendaciones para la población.
 - **Fuente:**
  <!-- 🚦 3. Tráfico y Accesos -->
  <section>
    <h2>🚦 3. Tráfico y Accesos</h2>
    <div class="card">
      <ul>
        <li>Estado de las principales vías: N-332 y A-70.</li>
        <li>Accesos a playas y centros urbanos.</li>
        <li>Aparcamiento y transporte público (TRAM, buses).</li>
      </ul>
      <p><b>Fuentes:</b>
        <a href="https://infocar.dgt.es/etraffic/" target="_blank">DGT – Estado del tráfico</a>
        &nbsp;·&nbsp;
        <a href="https://www.google.com/maps/@38.4286,-0.3972,14z/data=!5m1!1e1" target="_blank">Mapa tráfico (Google Maps)</a>
      </p>
    </div>
  </section>
### 🔶 4. Sucesos en Campello (últimas 24h)
- Robos, hurtos, incendios, accidentes o detenciones.
- **Fuente:**
### 🏖️ 5. Estado de las Playas y el Mar
- Bandera del día, oleaje, presencia de medusas o corrientes.
- Condiciones para el baño y recomendaciones de protección solar.  
- **Fuente:**
### 🛍️ 6. Información para Comercios y Empresas
- Cortes de suministro (agua, luz, telecomunicaciones).
- Eventos que puedan afectar a la actividad comercial.
- Avisos preventivos o de oportunidad.
- **Fuente:**
  
### 📣 7. Eventos y Actividades del Día
- Actividades, fiestas, actos públicos, mercadillos o eventos deportivos que afecten a la vida pública o movilidad.
- **Fuente:**

### ⚠️ 8. Recomendaciones Generales
- Consejos prácticos para residentes, turistas y comercios.
- Seguridad, prevención climática, autoprotección y comportamiento ante emergencias.

### 🔗 9. Enlaces y Recursos de Interés
- Contactos útiles, servicios de emergencia.
- Enlaces a clima en tiempo real, tráfico y alertas de organismos oficiales.
- **Fuente:**
"""

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {out_html}")
