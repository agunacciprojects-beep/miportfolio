# -*- coding: utf-8 -*-
"""
Gate del portafolio. Corre solo, sin dependencias, en cualquier maquina con Python.

    python verificar.py

Chequea lo que se rompio alguna vez de verdad en este sitio. Cada regla tiene su
motivo al lado: si una molesta, primero lee por que esta, despues decidi.
Sale con codigo 1 si algo falla, asi se puede colgar de un hook o de CI.

Lo que este script NO puede ver (hay que mirarlo en el navegador):
  - que el scroll horizontal de #trabajos no corte el fondo de las cards
  - que los reveals aparezcan
  - como se ve
Para eso, ver la seccion "Como se testea este sitio" del README.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(RAIZ, 'index.html')
DOMINIO = 'https://agunacci.vercel.app'

fallos = []
avisos = []


def texto_visible(html):
    """El HTML sin <script>, sin <style>, sin comentarios y sin etiquetas."""
    c = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    c = re.sub(r'<style.*?</style>', ' ', c, flags=re.S)
    c = re.sub(r'<!--.*?-->', ' ', c, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', c)


def revisar(nombre, cantidad, tope, motivo):
    if cantidad > tope:
        fallos.append('%s: %d (tope %d)\n      por que: %s' % (nombre, cantidad, tope, motivo))
    return cantidad


def main():
    if not os.path.exists(ARCHIVO):
        print('No encuentro index.html al lado de este script.')
        return 1

    html = io.open(ARCHIVO, encoding='utf-8').read()
    txt = texto_visible(html)

    # --- Copy -------------------------------------------------------------
    revisar('em-dash en texto visible', len(re.findall(r'[—–]', txt)), 0,
            'es el tic mas reconocible de texto generado por IA. En los comentarios '
            'del codigo no molesta; en lo que lee el cliente, si.')

    revisar('sparkles decorativos', len(re.findall(r'[✦✨]', txt)), 0,
            'los simbolos tipo estrellita son firma de plantilla generada.')

    revisar('ingles en el copy', len(re.findall(r'(?i)handcrafted|build by|philosophy|field notes', txt)), 0,
            'el sitio le habla a un dueno de comercio en Catamarca.')

    revisar('menciones a Claude o IA', len(re.findall(r'(?i)\bclaude\b', txt)), 0,
            'decision de Agustin: el material comercial no menciona asistentes de IA.')

    revisar('sellos de version', len(re.findall(r'·\s*v\d|>v\d\.\d<|build:\s*20', html)), 0,
            'v1.0 / build: 2026.08 son decoracion que ademas envejece sola.')

    banlist = ['potenciar', 'impulsar', 'robusto', 'potente', 'escalable', 'integral',
               'innovador', 'vanguardia', 'sin esfuerzo', 'en la era', 'siguiente nivel',
               'y mucho mas', 'brindando', 'permitiendo', 'sirve como', 'en resumen']
    pegues = [b for b in banlist if re.search(re.escape(b), txt, re.I)]
    if pegues:
        avisos.append('banlist es-AR: %s\n      no es prohibicion: justifica cada uno o '
                      'reescribilo con un verbo llano.' % ', '.join(pegues))

    # --- Estructura y links ----------------------------------------------
    revisar('links muertos href="#"', len(re.findall(r'href="#"', html)), 0,
            'un link que no lleva a ningun lado en un sitio que vende.')

    anclas = set(re.findall(r'href="(#[^"]+)"', html))
    ids = set('#' + i for i in re.findall(r'\sid="([^"]+)"', html))
    rotas = sorted(a for a in anclas if a != '#' and a not in ids)
    if rotas:
        fallos.append('anclas rotas: %s\n      por que: el menu deja de funcionar.' % ', '.join(rotas))

    revisar('target=_blank sin noopener', len(re.findall(r'target="_blank"(?![^>]*noopener)', html)), 0,
            'la pestana nueva puede tocar la original. Es un agujero conocido.')

    revisar('imagenes sin alt', len(re.findall(r'<img(?![^>]*\salt=)', html)), 0,
            'accesibilidad.')
    revisar('imagenes sin width/height', len(re.findall(r'<img(?![^>]*width=)', html)), 0,
            'sin medidas declaradas la pagina salta al cargar (CLS).')

    # --- Miniatura de WhatsApp -------------------------------------------
    for etiqueta in ['og:image', 'og:url', 'twitter:image']:
        m = re.search(r'(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(etiqueta), html)
        if not m:
            fallos.append('falta la etiqueta %s\n      por que: sin ella no hay miniatura '
                          'al compartir el link.' % etiqueta)
        elif not m.group(1).startswith('http'):
            fallos.append('%s es una ruta relativa ("%s")\n      por que: WhatsApp NO resuelve '
                          'rutas relativas. Ya nos comimos este bug: la miniatura no aparecia '
                          'aunque la imagen estuviera publicada.' % (etiqueta, m.group(1)))
        elif not m.group(1).startswith(DOMINIO):
            avisos.append('%s apunta a %s, no al dominio principal (%s). Si el sitio se mudo, '
                          'actualizalo.' % (etiqueta, m.group(1), DOMINIO))

    canon = re.search(r'rel="canonical"\s+href="([^"]*)"', html)
    if not canon:
        avisos.append('falta <link rel="canonical">. El sitio vive en dos dominios; sin '
                      'canonical compiten como contenido duplicado.')

    # --- Grilla del stack -------------------------------------------------
    tiles = len(re.findall(r'<div class="toggle-tile group">', html))
    if tiles % 6 != 0:
        avisos.append('el stack tiene %d tiles y la grilla es de 6 columnas: queda un hueco '
                      'en la ultima fila. Sumale o sacale uno.' % tiles)

    # --- Salida -----------------------------------------------------------
    print('')
    print('  Gate del portafolio  ·  index.html  ·  %d KB' % (len(html.encode('utf-8')) // 1024))
    print('  ' + '-' * 58)
    if not fallos and not avisos:
        print('  Todo en verde.')
    for f in fallos:
        print('  FALLA  ' + f)
    for a in avisos:
        print('  AVISO  ' + a)
    print('')
    print('  Lo visual (scroll horizontal, reveals, encuadre) no lo ve este')
    print('  script: hay que abrirlo en el navegador. Ver el README.')
    print('')
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
