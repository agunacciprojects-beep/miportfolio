<div align="center">

# `agunacci`

### Software que opera en el mundo real.

Portafolio personal de **Kamlovski Agustín** · desarrollador fullstack independiente.
San Fernando del Valle de Catamarca, Argentina.

[**Ver el sitio →**](https://agunacci.vercel.app)

`Sin agencia · sin intermediarios · trato directo`

</div>

---

## ¿Qué es esto?

El portafolio que uso para mostrar mis trabajos a clientes potenciales. Acá viven los 4 trabajos que tienen un cliente real detrás, junto con el código del propio sitio.

No es un template ni un boilerplate. Es un proyecto a medida con un objetivo concreto: **cerrar clientes nuevos**. Cada decisión de diseño (paleta, motion, tipografía, copy) está pensada para eso.

---

## Donde vive el sitio

**Principal: https://agunacci.vercel.app** (Vercel, proyecto `agunacci`).
Link viejo, todavia vivo: `agunacciprojects-beep.github.io/miportfolio`, con el
`canonical` apuntando a Vercel para que no compitan como contenido duplicado.

⚠️ **Las cuatro URLs absolutas del `<head>` (`canonical`, `og:url`, `og:image`,
`twitter:image`) tienen que apuntar al dominio principal.** Con rutas relativas
WhatsApp no muestra miniatura: es un bug que ya nos comimos una vez. Si el sitio
se muda de dominio, se cambian esas cuatro **antes** de deployar.

El deploy a Vercel es por CLI (`vercel deploy --prod`), no por git push: la
conexion del repo de GitHub con el proyecto de Vercel quedo sin hacer.

**No renombrar el usuario de GitHub** aunque `agunacci` este libre: GitHub
redirige los repos viejos pero NO las URLs `*.github.io`, asi que todo link ya
repartido quedaria muerto sin aviso.

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

| # | Trabajo | Estado | Qué es | Stack |
|---|---|---|---|---|
| 01 | **TuBarber** | en producción · 3 locales | POS offline para barberías: cobra sin internet, separa lo de cada barbero y cierra el mes | Next.js 16 · Electron · Prisma · SQLite |
| 02 | **La trastienda** | en producción | Panel de licencias y actualizaciones: emisión, renovación, baja y OTA firmado | Next.js 16 · Prisma 7 · PostgreSQL · Cloudflare · Ed25519 |
| 03 | **Catálogo y pedido por WhatsApp** | entregado | Comercio local que arma el pedido desde el celular y lo retira en el local (identidad del cliente reservada) | HTML/CSS/JS · Cloudflare · GSAP |
| 04 | **Modernización contable** | terminado, en evaluación | Reemplazo de un sistema COBOL con 30+ años en uso, preservando el histórico completo | FastAPI · Python · SQLite · PDF |

**Criterio de qué entra:** un trabajo entra cuando tiene un cliente real del otro lado.
Herramientas propias sin cliente (NacciStock, Windows Optimizer Pro, bios_assistant) no
figuran: la capacidad se ve en el stack, no ocupa una card.

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

- **Sin framework**: con HTML + Tailwind CDN tengo control total y cero build step.
  **Lo que cuesta, medido (2026-08-29, `curl`):** Tailwind CDN 407 KB · Font Awesome 102 KB ·
  GSAP+ScrollTrigger 117 KB · Lenis+SplitType 26 KB · `index.html` 94 KB = **~750 KB desde 5
  orígenes**. O sea: la comodidad de no tener build cuesta más que el runtime de un framework,
  no menos. Y el CDN de Tailwind es un compilador JIT que corre en el browser — la propia
  consola avisa que no es para producción. **Deuda asumida a conciencia, no una ventaja.**
  El día que moleste, el arreglo es Tailwind CLI a un `.css` estático y los ~22 íconos de
  Font Awesome pasados a SVG inline.
- **Lenis + GSAP + IntersectionObserver mezclados**: ScrollTrigger se rompe a veces cuando Lenis intercepta scroll events (timing race condition). Por eso los reveals usan IntersectionObserver nativo (bulletproof), pero los efectos pin+scrub usan ScrollTrigger (donde sí vale la potencia de GSAP).
- **Cursor custom triple-layer**: un dot (sigue al cursor instantáneo) + ring (sigue con inercia 0.2) + glow (sigue con inercia 0.1). Se desactiva en touch devices y en `prefers-reduced-motion`.
- **Horizontal scroll en trabajos**: la sección se pinea mientras las cards se desplazan
  horizontalmente. Distance calculada dinámicamente para que la última card termine alineada
  con el right edge del viewport. Fallback mobile = grid vertical normal.
  **Tres reglas que salieron de un bug real (2026-08-29), no las rompas:**
  1. La sección se pinea a `top top+=64` (debajo del nav fijo), así que **no puede medir
     `100vh`**: quedaría 64px más abajo del viewport y se come el fondo de las cards. Medido
     en 1366x728 se cortaban 95px. Mide `calc(100dvh - 64px)`. `dvh` y no `vh` por la barra
     del navegador en mobile.
  2. En pantallas de menos de 850px de alto la card se estira (el texto envuelve más) y no
     entra. Hay un bloque `@media (max-height: 850px)` que recorta el aire interno. Si
     agregás texto a una card, **volvé a medir ahí**.
  3. Red de seguridad: si aun compactado no entra, el JS marca `.sin-pin` y la sección vuelve
     a una grilla de 2 columnas. **Preferimos quedarnos sin scroll horizontal antes que
     mostrar las cards cortadas.** Verificado: 0px de corte entre 1366x728 y 1920x1080.
- **Los botones no se mueven** (sacado el efecto magnético 2026-08-29). Un botón que se corre
  del cursor se siente roto y hace fallar el click. En su lugar, al presionar se retroilumina
  el borde (`.magnetic-primary:active` / `.magnetic-ghost:active`). **Esas reglas van DESPUÉS
  de los `:hover` a propósito:** tienen la misma especificidad, gana la última, y si las subís
  el `:hover` se las come y el botón deja de responder al click. Ya pasó una vez.
- **Sin cursor custom** (sacado 2026-08-29 a pedido de Agustín). Si alguna vez vuelve, acordate
  de que necesita `body.cursor-active { cursor: none }` y que se apaga en touch y en
  `prefers-reduced-motion`.
- **Gradiente de texto + SplitType = glifos fantasma (encontrado 2026-08-29).** El h1 se
  parte en `words,chars` y los h2 solo en `words`. Como la regla del gradiente aplicaba a la
  línea, a la palabra Y al char, los tres pintaban el mismo glifo con `background-clip:text`
  sobre cajas de gradiente de distinto ancho, y WebKit dejaba una letra fantasma corrida en
  la primera de cada palabra. **Estuvo a la vista meses.** Se arregla con `:has()`: pinta
  solo el envoltorio más interno. Si algún día cambiás el `types:` del SplitType, revisá esa
  regla.
- **Tailwind: `text-4xl` trae line-height propio, `text-[2.75rem]` no.** Un `lg:text-[...]`
  arbitrario pisa el `font-size` pero deja el leading del breakpoint anterior. Resultado: el
  renglón queda más chico que la letra y **se cortan los acentos** (DÍAS, ACÁ, MÁS), que en
  castellano es casi todo titular. Por eso cada paso responsive fija el par con la barra:
  `md:text-4xl/[1.1] lg:text-[2.75rem]/[1.1]`. No saques las barras.
- **Cómo se testea este sitio (aprendido a los golpes, 2026-08-29):** con Lenis activo,
  `window.scrollTo()` desde Playwright **no sirve** — Lenis pelea el scroll y la sección
  nunca entra al viewport, así que los reveals quedan en `opacity:0` y parece que el sitio
  está roto. Es un **falso positivo del test, no un bug del sitio**. Se verifica con
  `page.mouse.wheel()` (rueda real, que es lo que Lenis intercepta) o clickeando la
  navegación del propio sitio. Antes de "arreglar" un reveal que no aparece, probá con la
  rueda: casi seguro anda.

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
