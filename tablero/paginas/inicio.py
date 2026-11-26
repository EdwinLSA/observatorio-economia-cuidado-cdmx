"""Portada: la pregunta rectora, la cifra con la que el equipo acordó encabezar (la brecha
de trabajo no pagado, con la jornada total como apoyo), la escalera de lo general a lo
particular que ordena las demás páginas y un adelanto de Decisión (escenario simulado) y
de Metodología. Toda cifra se lee de los datos, igual que en su página."""

import streamlit as st

import datos as d
from componentes import (ESTADOS, esc, f_cambio, f_ent, f_horas, f_num, f_pct, insignias, kpis_con_meta,
                         subtitulo, vacio)


def millones(v):
    """Pesos en millones, con el mismo formato que la página Decisión: $1.08 M o −$0.49 M."""
    return '—' if vacio(v) else f'{"−" if v < 0 else ""}${abs(v) / 1e6:,.2f} M'

brecha = d.kpi(d.KPI_BRECHA)
jornada = d.kpi(d.KPI_JORNADA_MUJERES)

izquierda, derecha = st.columns([1.25, 1], gap='large', vertical_alignment='center')
with izquierda:
    st.html('<p class="obs-escala">Economía del cuidado en México y la Ciudad de México</p>')
    st.title('Cuidar también es trabajo', anchor=False)
    st.markdown('Este observatorio mide dónde y cuánto trabajo de cuidado no remunerado recae sobre las '
                'mujeres: del país a la Ciudad de México, de la ciudad a cada alcaldía y de ahí a cada '
                'AGEB. También mide qué tanto lo alivia la oferta de cuidados que tienen cerca.')
    st.html(f'<div class="obs-pregunta"><b>Pregunta rectora</b>{esc(d.metodologia.PREGUNTA_RECTORA)}</div>')
with derecha:
    st.html(f'''<aside class="obs-heroe" aria-label="Cifra principal del observatorio">
      <p style="margin:0">Las mujeres ocupadas de la Ciudad de México hacen</p>
      <p class="obs-cifra">+{esc(f_num(brecha))}<span>h</span></p>
      <p style="margin:0 0 12px">más de trabajo no pagado <strong>cada semana</strong> que los hombres ocupados
        (referencia): trabajo doméstico y cuidado de su propio hogar.</p>
      <p class="obs-apoyo" style="margin:0">Sumando el trabajo pagado, su jornada total llega a
        <strong>{esc(f_num(jornada))} horas</strong> a la semana.</p>
      <div class="obs-nota"><span>Fuente: INEGI, ENUT 2024</span><span>Nivel: {insignias("CDMX")}</span></div>
    </aside>''')

st.space('medium')
st.subheader('De lo general a lo particular', anchor=False)

enut = d.tabla('enut_carga_actividad')
nac = enut[(enut['ambito'] == 'Nacional') & (enut['sexo'] == 'Mujeres') & (enut['actividad'] == d.TOTAL_CUIDADO)]
alc = d.tabla('resumen_alcaldia').sort_values('carga_directa_x100_mujeres', ascending=False).iloc[0]
sin = d.territorio(None)['embudo'][-1]
escalones = [
    ('México', f_pct(nac['pct_realiza'].iloc[0] if len(nac) else None),
     'de las mujeres de 12 años y más del país cuida a integrantes de su hogar.',
     'Nacional', 'ENUT 2024', False, 'paginas/mexico.py'),
    ('Ciudad de México', f_pct(d.kpi(d.KPI_PCT_CUIDAN)),
     f'de las mujeres de la ciudad cuida; las que cuidan le dedican {f_horas(d.kpi(d.KPI_HORAS_CUIDAN))} a la semana.',
     'CDMX', 'ENUT 2024', False, 'paginas/cdmx.py'),
    ('Alcaldías', f_num(alc['carga_directa_x100_mujeres']),
     f'personas que necesitan cuidado directo por cada 100 mujeres de 15 a 59 en {alc["alcaldia"]}, '
     f'la carga más alta (ciudad: {f_num(d.kpi(d.KPI_CARGA_CDMX))}).',
     'Alcaldía', 'Censo 2020', False, 'paginas/alcaldias.py'),
    ('AGEB', f_ent(sin['mujeres_15a59']),
     f'mujeres de 15 a 59 viven en {f_ent(sin["agebs"])} AGEB de alta carga sin guardería, residencia ni '
     f'centro de día a 1 km.', 'AGEB', 'Censo 2020 + DENUE', True, 'paginas/territorio.py'),
]
for col, (escala, valor, texto, nivel, fuente, exploratorio, destino) in zip(st.columns(4), escalones):
    with col:
        st.html(f'''<div class="obs-tarjeta obs-escalon"><p class="obs-tile-etiqueta">{esc(escala)}</p>
          <p class="obs-tile-valor">{esc(valor)}</p><p class="obs-tile-contexto">{esc(texto)}</p>
          <div class="obs-tile-pie">{insignias(nivel, exploratorio)}<span>{esc(fuente)}</span></div></div>''')
        st.page_link(destino, label=f'Ir a {escala}', icon=':material/arrow_forward:')

# --- Adelanto de Decisión: mismas cifras y mismas reglas de estado que la página ---------------
r = d.resumen_decision()
fam, equilibrio, van = r['familias_estable'], r['punto_equilibrio'], r['van_esperado_etapas']
st.space('medium')
subtitulo('Del dato a la decisión',
          'La oferta formal de cuidado se contrajo y no hay señales de que vuelva a crecer sola. Con los hallazgos '
          'del observatorio se evaluó si conviene una red de cuidado a domicilio en Iztapalapa.')
st.info('**Escenario simulado.** El programa y su operador son hipotéticos; los datos del observatorio son reales.',
        icon=':material/science:')
kpis_con_meta([
    {'etiqueta': 'Oferta formal de respaldo en la CDMX', 'valor': f_ent(r['oferta_hoy']),
     'meta': f'Referencia: {f_ent(r["oferta_2016"])} en 01/2016 '
             f'({f_cambio((r["oferta_hoy"] / r["oferta_2016"] - 1) * 100)}).',
     'estado': 'critico' if r['oferta_hoy'] < r['oferta_2016'] else 'ok', 'detalle_estado': 'a la baja',
     'nivel': 'CDMX', 'fuente': 'DENUE 2016-2026'},
    {'etiqueta': 'Familias del programa en estado estable (realista)', 'valor': f_ent(fam),
     'meta': f'Meta: punto de equilibrio de {f_ent(equilibrio)} familias '
             f'({f_cambio((fam / equilibrio - 1) * 100) if not (vacio(fam) or vacio(equilibrio)) else "—"}).',
     'estado': 'ok' if not (vacio(fam) or vacio(equilibrio)) and fam >= equilibrio else 'critico',
     'nivel': 'AGEB', 'simulado': True, 'fuente': 'Escenario simulado'},
    {'etiqueta': 'VAN esperado, invirtiendo por etapas', 'valor': millones(van),
     'meta': 'Meta: VAN > 0 al 10 % real, con revisión en el mes 12.',
     'estado': 'ok' if not vacio(van) and van > 0 else 'critico',
     'nivel': 'AGEB', 'simulado': True, 'fuente': 'Escenario simulado'},
])
st.page_link('paginas/decision.py', label='Ir a Decisión', icon=':material/arrow_forward:')

# --- Franja de Metodología: fuentes, advertencias y cifras de control ----------------------------
m = d.metodologia
repo = d.repositorio()
st.space('medium')
subtitulo('Cómo se hizo', 'Todas las cifras son del INEGI y se publican con su fuente, su año y su nivel geográfico.')
fuentes = ''.join(
    f'''<div class="obs-tarjeta"><p class="obs-tile-etiqueta">{esc(f["clave"])}</p>
      <p class="obs-tile-contexto">{esc(f["nombre"])}</p><div class="obs-tile-pie">{insignias(f["niveles"])}</div></div>'''
    for f in m.FUENTES)
st.html(f'<div class="obs-rejilla" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{fuentes}</div>')
cuadran, controles = sum(x['ok'] for x in repo.controles), len(repo.controles)
clase, forma, _ = ESTADOS['ok' if repo.controles_ok else 'critico']
st.html(f'''<div class="obs-nota"><span>{len(m.ADVERTENCIAS)} advertencias de lectura dicen qué se puede y qué no
  se puede afirmar con cada cifra.</span><span class="obs-estado {clase}"><span aria-hidden="true">{forma}</span>
  {cuadran} de {controles} cifras de control cuadran</span></div>''')
st.page_link('paginas/metodologia.py', label='Ir a Metodología', icon=':material/arrow_forward:')
