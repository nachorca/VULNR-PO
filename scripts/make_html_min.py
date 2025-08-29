#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "templates" / "informe_seguridad_template.md"
DATA = ROOT / "data" / "datos_informe.json"
OUT = ROOT / "informe_seguridad_generado.md"


def bullet(k, v):
    if v is None or (isinstance(v, str) and not v.strip()):
        v = "—"
    return f"- {k}: {v}"


def bullets_from_list(k, items):
    if not items:
        return f"- {k}: —"
    lines = [f"- {k}:"]
    for it in items:
        lines.append(f"  - {it}")
    return "\n".join(lines)


def format_resumen(data):
    txt = data.get("resumen_general") or "—"
    return f"{txt}\n"


def format_aemet(data):
    a = data.get("aemet_playas", {})
    parts = [
        bullet("Fecha/hora", a.get("fecha_hora")),
        bullet("Zona/municipio", a.get("zona")),
        bullet("Avisos vigentes", a.get("avisos_vigentes")),
        bullet("Oleaje/estado mar", a.get("oleaje_estado_mar")),
        bullet("Banderas/servicios", a.get("banderas_servicios")),
        bullet("Riesgo", a.get("riesgo")),
        bullet("Medidas/acción", a.get("medidas")),
        bullets_from_list("Fuentes", a.get("fuentes", [])),
        bullets_from_list("Evidencias", a.get("evidencias", [])),
    ]
    return "\n".join(parts) + "\n"


def format_criminalidad(data):
    c = data.get("criminalidad", {})
    parts = [
        bullet("Periodo", c.get("periodo")),
        bullet("Indicadores", c.get("indicadores")),
        bullet("Zonas de incidencia", c.get("zonas_incidentes")),
        bullet("Tendencia", c.get("tendencia")),
        bullet("Riesgo", c.get("riesgo")),
        bullet("Medidas/acción", c.get("medidas")),
        bullets_from_list("Fuentes", c.get("fuentes", [])),
        bullets_from_list("Evidencias", c.get("evidencias", [])),
    ]
    return "\n".join(parts) + "\n"


def format_disturbios(data):
    d = data.get("disturbios_civiles", {})
    parts = [
        bullet("Evento/convocatoria", d.get("evento")),
        bullet("Fecha/hora", d.get("fecha_hora")),
        bullet("Ubicación", d.get("ubicacion")),
        bullet("Aforo/impacto", d.get("aforo_impacto")),
        bullet("Afectación", d.get("afectacion")),
        bullet("Riesgo", d.get("riesgo")),
        bullet("Medidas/acción", d.get("medidas")),
        bullets_from_list("Fuentes", d.get("fuentes", [])),
        bullets_from_list("Evidencias", d.get("evidencias", [])),
    ]
    return "\n".join(parts) + "\n"


def format_incidencias_tec(data):
    t = data.get("incidencias_tecnologicas", {})
    parts = [
        bullet("Proveedor/servicio", t.get("proveedor")),
        bullet("Inicio", t.get("inicio")),
        bullet("Fin", t.get("fin")),
        bullet("Impacto", t.get("impacto")),
        bullet("Causa raíz", t.get("causa_raiz")),
        bullet("Riesgo", t.get("riesgo")),
        bullet("Acción inmediata", t.get("accion_inmediata")),
        bullet("Prevención", t.get("prevencion")),
        bullets_from_list("Fuentes", t.get("fuentes", [])),
        bullets_from_list("Evidencias", t.get("evidencias", [])),
    ]
    return "\n".join(parts) + "\n"


def format_trafico(data):
    tr = data.get("trafico_aparcamiento", {})
    parts = [
        bullet("Fecha/hora", tr.get("fecha_hora")),
        bullet("Zonas", tr.get("zonas")),
        bullet("Incidencias/cortes", tr.get("incidencias")),
        bullet("Aparcamiento", tr.get("disponibilidad_aparcamiento")),
        bullet("Congestión", tr.get("congestion")),
        bullet("Recomendaciones", tr.get("recomendaciones")),
        bullets_from_list("Fuentes", tr.get("fuentes", [])),
        bullets_from_list("Evidencias", tr.get("evidencias", [])),
    ]
    return "\n".join(parts) + "\n"


def format_fuentes(data):
    items = data.get("fuentes", [])
    if not items:
        return "- (sin fuentes)\n"
    lines = []
    for f in items:
        nombre = f.get("nombre", "Fuente")
        url = f.get("url", "")
        freq = f.get("frecuencia", "")
        resp = f.get("responsable", "")
        fia = f.get("fiabilidad", "")
        lines.append(f"- {nombre}: {url} — {freq}; resp: {resp}; fiabilidad: {fia}")
    return "\n".join(lines) + "\n"


def main():
    tpl = TPL.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))

    rendered = tpl
    rendered = rendered.replace("{{RESUMEN_GENERAL}}", format_resumen(data))
    rendered = rendered.replace("{{AEMET_PLAYAS}}", format_aemet(data))
    rendered = rendered.replace("{{CRIMINALIDAD}}", format_criminalidad(data))
    rendered = rendered.replace("{{DISTURBIOS_CIVILES}}", format_disturbios(data))
    rendered = rendered.replace("{{INCIDENCIAS_TECNOLOGICAS}}", format_incidencias_tec(data))
    rendered = rendered.replace("{{TRAFICO_APARCAMIENTO}}", format_trafico(data))
    rendered = rendered.replace("{{FUENTES}}", format_fuentes(data))

    OUT.write_text(rendered, encoding="utf-8")
    print(f"Informe generado: {OUT}")


if __name__ == "__main__":
    main()

