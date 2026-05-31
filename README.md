<div align="center">

# `agunacci`

### Software que opera en el mundo real.

Portafolio personal de **Kamlovski Agustín** · desarrollador fullstack independiente.
San Fernando del Valle de Catamarca, Argentina.

[**Ver el sitio →**](https://agunacciprojects-beep.github.io/miportfolio)

`Sin agencia · sin intermediarios · trato directo`

</div>

---

## ¿Qué es esto?

El portafolio que uso para mostrar mis trabajos a clientes potenciales. Acá viven los 6 sistemas que tengo en producción, junto con el código del propio sitio.

No es un template ni un boilerplate. Es un proyecto a medida con un objetivo concreto: **cerrar clientes nuevos**. Cada decisión de diseño (paleta, motion, tipografía, copy) está pensada para eso.

---

## Stack técnico

```
HTML5 + Tailwind CSS (CDN, sin build step)
GSAP 3.13 + ScrollTrigger      ← scroll storytelling y pin
Lenis 1.1                      ← smooth scroll inercial
SplitType 0.3                  ← char/word reveal animations
Vanilla JS                     ← cursor custom, particles canvas, reel automation
FFmpeg + Python (numpy)        ← generación del reel video
Playwright (chromium headless) ← grabación del reel
```

Sin frameworks pesados. Sin build process. Un `index.html` que en cualquier server estático corre.

## Estructura

```
miportfolio/
├── index.html              ← el portafolio (todo en uno: HTML + CSS + JS)
├── assets/
│   ├── yo.png              ← retrato con duotone wine
│   ├── og-image.png        ← preview para WhatsApp / IG / LinkedIn
│   └── ecosistema.jpg      ← screenshot proyecto legacy (no usado, archivo)
├── reel/
│   ├── reel.html           ← HTML animado del reel (16s, 1080×1920)
│   ├── record.py           ← script Playwright que graba el HTML como video
│   ├── generate_audio.py   ← sintetiza la banda sonora (synthwave, 16s)
│   └── naccitech-reel-final.mp4  ← reel listo para subir a IG
└── README.md
```

## Trabajos showcased

| # | Sistema | Tipo | Stack |
|---|---|---|---|
| 01 | **NacciStock** | POS offline para comercios chicos | Electron · SQLite · Node.js |
| 02 | **BarberPOS** | Gestión financiera entre socios independientes | Next.js · Prisma · TypeScript · Tailwind |
| 03 | **Modernización contable** | Reemplazo de un sistema en COBOL preservando 30+ años de datos | FastAPI · Python · SQLite · PDF |
| 04 | **Programa de beneficios** | PWA con QR para validar socios en comercios aliados | Next.js · PWA · QR dinámico · Mobile-first |
| 05 | **Windows Optimizer Pro** | App de escritorio liviana, multilingüe (ES/EN) | Tauri · React · TypeScript · i18n |
| 06 | **bios_assistant** | CLI que analiza dumps de BIOS asistido por IA | Python · Claude API · SQLite · CLI |

Más info de cada uno en el sitio.

## Cómo correrlo localmente

```bash
# Cualquier servidor HTTP estático sirve. Las dos formas más simples:

# Python (incluido en cualquier sistema con Python instalado)
cd miportfolio
python -m http.server 8765
# → http://localhost:8765

# Node (si tenés npx)
cd miportfolio
npx serve -p 8765
# → http://localhost:8765
```

No requiere build, ni instalación de dependencias, ni env vars. Abrís `index.html` directo en el browser y también funciona (algunos efectos sutiles pueden no andar bajo `file://` por CORS — el server local es la forma correcta).

## Regenerar el reel video

Si querés cambiar el copy del reel, ajustar la duración o cambiar la banda sonora:

```bash
# 1. Editás reel/reel.html (HTML animado con keyframes sincronizados)
# 2. (Opcional) Editás reel/generate_audio.py (numpy synth)

cd reel
python generate_audio.py        # → audio.wav (16s, 48kHz)
python record.py                # → naccitech-reel-final.mp4 (1080×1920)

# Requiere: playwright + numpy + ffmpeg en PATH
```

El script graba el HTML animado con Chromium headless y lo mezcla con la banda sonora vía FFmpeg. El resultado es un MP4 IG-ready de 16 segundos.

## Decisiones técnicas (las que no son obvias)

- **Sin framework**: con HTML + Tailwind CDN tengo control total y el sitio carga en menos de 2 segundos. Un framework agregaría 200 KB de runtime sin valor en un sitio de 1 página.
- **Lenis + GSAP + IntersectionObserver mezclados**: ScrollTrigger se rompe a veces cuando Lenis intercepta scroll events (timing race condition). Por eso los reveals usan IntersectionObserver nativo (bulletproof), pero los efectos pin+scrub usan ScrollTrigger (donde sí vale la potencia de GSAP).
- **Cursor custom triple-layer**: un dot (sigue al cursor instantáneo) + ring (sigue con inercia 0.2) + glow (sigue con inercia 0.1). Se desactiva en touch devices y en `prefers-reduced-motion`.
- **Horizontal scroll en trabajos**: la sección se pinea durante 6 viewports verticales mientras las cards se desplazan horizontalmente. Distance calculada dinámicamente para que la última card termine alineada con el right edge del viewport. Fallback mobile = grid vertical normal.
- **Mobile-first responsividad**: cursor custom, Lenis y horizontal scroll desactivados en mobile. Marquees siguen activos. La estética se preserva sin sacrificar performance ni gestos nativos.
- **OG image 1200×630**: generada a mano con PowerShell + System.Drawing para previews lindos en WhatsApp/IG/LinkedIn. Sin canvas dinámico ni servicios externos.

## Accesibilidad

- Contraste 4.5:1+ en todo el copy (verificado en bone-mute sobre slate-950)
- `prefers-reduced-motion`: desactiva Lenis, cursor custom y todas las animaciones
- Focus rings wine visibles en todos los `a` y `button`
- Alt text descriptivo en la foto
- `width`/`height` declarados en imágenes para evitar CLS

## Contacto

- 📧 **agunacciprojects@gmail.com**
- 📱 **+54 9 3834 27-1005** (WhatsApp directo)
- 📸 **[@naccitech.arg](https://instagram.com/naccitech.arg)**

---

<div align="center">

Diseñado, desarrollado y mantenido por **agunacci** · 2026
Hecho a mano en San Fernando del Valle.

</div>
