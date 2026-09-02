# Write-up: Starting Out In Cyber Sec (TryHackMe)

> Write-up de la room introductoria de TryHackMe para orientación en ciberseguridad. Room gratuita, sin máquina virtual — 100% conceptual. Cubre las ramas de seguridad ofensiva y defensiva, y presenta la plataforma TryHackMe como entorno de aprendizaje.

- **Plataforma**: TryHackMe
- **Room**: Starting Out In Cyber Sec
- **URL**: https://tryhackme.com/room/startingoutincybersec
- **Dificultad**: Easy (conceptual, sin exploot)
- **Fecha**: 17/08/2026
- **Username**: paz243482
- **Ruta de aprendizaje**: Pre Security → Complete Beginner
- **Herramientas**: navegador web, cuenta gratuita en TryHackMe

## Resumen ejecutivo (3 frases)

Esta room es la puerta de entrada oficial de TryHackMe al mundo de la ciberseguridad. No requiere máquina virtual ni herramientas técnicas — es un cuestionario guiado que presenta las dos ramas principales del sector (ofensiva y defensiva), los roles profesionales asociados, y cómo navegar la plataforma. Completarla desbloquea el seguimiento de progreso y el acceso a las rutas de aprendizaje estructuradas.

## Alcance (Scope)

- **Objetivo**: room conceptual (sin target IP)
- **Autorización**: plataforma TryHackMe (room gratuita, acceso explícito)
- **Herramientas**: navegador web únicamente

## Estructura de la room

La room consta de **3 tasks**:

### Task 1: Welcome To TryHackMe

**Contenido**: Introducción a la plataforma — cómo funciona el sistema de rooms, el seguimiento de progreso, y las rutas de aprendizaje (Learning Paths).

**Acción requerida**: Leer la información y hacer clic en "I've visited this link" / "Completed".

**Pregunta**: No hay pregunta — es informativa.

**Key takeaway**: TryHackMe organiza el contenido en *rooms* (laboratorios individuales) agrupados en *paths* (rutas de aprendizaje secuenciales). El path "Pre Security" es el punto de partida recomendado.

### Task 2: Offensive Security (Seguridad Ofensiva)

**Contenido**: Explicación de la seguridad ofensiva — el arte de encontrar vulnerabilidades de forma ética y autorizada.

**Pregunta**: *"What is the name of the career role that is legally employed to find vulnerabilities in applications?"*

**Respuesta**: `penetration tester`

**Conceptos clave presentados**:
- **Penetration tester (pentester)**: profesional que simula ataques autorizados para encontrar vulnerabilidades antes de que los atacantes reales lo hagan.
- **Red Team**: equipo que realiza simulaciones de ataque a gran escala contra una organización.
- **Bug Bounty**: programas donde investigadores de seguridad reportan vulnerabilidades a cambio de recompensas.
- La seguridad ofensiva es **ética y legal** cuando se hace con autorización explícita.

### Task 3: Defensive Security (Seguridad Defensiva)

**Contenido**: Explicación de la seguridad defensiva — el conjunto de prácticas para proteger sistemas, redes y datos contra ataques.

**Pregunta**: *"What is the name of the role who's job is to identify attacks against an organisation?"*

**Respuesta**: `security analyst`

**Conceptos clave presentados**:
- **Security analyst**: profesional que monitorea sistemas, analiza alertas de seguridad y responde a incidentes.
- **SOC (Security Operations Center)**: equipo centralizado que opera 24/7 para detectar y responder a amenazas.
- **Blue Team**: equipo defensivo que configura y mantiene las defensas de una organización.
- La seguridad defensiva incluye: monitoreo de tráfico, análisis de logs, configuración de firewalls, y respuesta a incidentes.

## Callejón sin salida (dead-end) 1

- **Hipótesis**: inicialmente busqué si la room requería conectarse a una máquina virtual (IP tipo 10.10.x.x).
- **Qué hice**: revisé la interfaz buscando el botón "Start Machine".
- **Por qué falló**: esta room es puramente conceptual — no hay máquina que levantar.
- **Lección**: no todas las rooms de TryHackMe son laboratorios técnicos. Las rooms introductorias son cuestionarios que establecen vocabulario y orientación profesional. Siempre leer la descripción de la room antes de buscar herramientas.

## Callejón sin salida (dead-end) 2

- **Hipótesis**: busqué si había un seguimiento de progreso visible públicamente (como en HackTheBox).
- **Qué hice**: revisé la URL del perfil de usuario en TryHackMe.
- **Por qué falló**: TryHackMe no muestra el progreso de forma pública tan fácilmente como HTB; el badge y el progreso son internos a la plataforma.
- **Lección**: el perfil público de TryHackMe (e.g., `tryhackme.com/p/paz243482`) muestra badges y rank, pero no el detalle de cada room. Para documentar progreso, tomar screenshots o usar la API de TryHackMe.

## Análisis del impacto (si fuera producción)

- **Riesgo**: N/A (room conceptual).
- **Aplicación real**: los conceptos de esta room son la base de toda carrera en ciberseguridad:
  - **Penetration testing** → fase de auditoría ofensiva en organizaciones.
  - **Security analysis** → fase de monitoreo y respuesta en SOC.
  - Entender ambas ramas permite alinear el plan de estudios (N1-N7 en el roadmap personal).

## Herramientas propias utilizadas

- Navegador web (Brave) para acceder a la room.
- Cuenta gratuita de TryHackMe (`paz243482`).
- No se usaron herramientas de `sec-tool` — room puramente conceptual.

## Línea de CV derivada de este write-up

> "Completé la room introductoria 'Starting Out In Cyber Sec' en TryHackMe; identifiqué las ramas ofensiva/defensiva de la ciberseguridad, los roles profesionales (penetration tester, security analyst), y la estructura de la plataforma como entorno de aprendizaje continuo."

---

## Lecciones del proceso

1. **Las rooms conceptuales son el paso 1**: antes de tocar nmap o burpsuite, es fundamental entender el vocabulario y los roles del sector.
2. **TryHackMe vs HackTheBox**: THM es más guiado y pedagógico (ideal para principiantes); HTB es más orientado a retos prácticos.
3. **Documentar incluso las rooms simples**: un write-up de una room conceptual demuestra **metodología de aprendizaje**, no solo habilidad técnica.
4. **El username `paz243482` queda registrado**: las completaciones de rooms contribuyen al ranking y badges de la plataforma.
5. **Siguiente paso lógico**: room "Tutorial" (https://tryhackme.com/room/tutorial) — primera máquina virtual real con Nmap.

*Tags: #writeup #tryhackme #cybersec #beginner #orientation #pentester #security-analyst*
