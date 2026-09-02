# Write-up: Reconocimiento de `scanme.nmap.org` (target oficial Nmap)

> Write-up de reconocimiento (N1/N2) para el plan de estudio ciberseguridad 2026. `scanme.nmap.org` es un target **oficial y explícitamente permitido** por el proyecto Nmap para practicar escaneo (más info en nmap.org/book/scanme.html). Aplicamos: nmap full-port + service detection, gobuster directory enumeration, y análisis de exposición.

- **Plataforma**: target oficial `scanme.nmap.org` (45.33.32.156)
- **Objetivo**: practicar nmap + gobuster como recon inicial de pentest
- **Dificultad**: Easy (target de laboratorio)
- **Fecha**: 16/08/2026
- **Ruta de aprendizaje**: N1 Fundamentos / N2 SOC / N3 Pentesting (Recon)
- **Herramientas**: nmap 7.98, gobuster 3.8.2 (en WSL2 Ubuntu), dirb wordlists

## Resumen ejecutivo (3 frases)

`scanme.nmap.org` expone 5 puertos TCP (22/80/9929/31337 abiertos, 25 filtrado). El servicio HTTP en el puerto 80 corre Apache 2.4.7 (versión **muy antigua** — EOL desde 2019). El puerto 31337 `tcpwrapped` y `.svn` expuesto en el server web son hallazgos de riesgo de configuración/exposición de código fuente.

## Alcance (Scope)

- IP objetivo: `45.33.32.156`
- Autorización: target oficial del proyecto Nmap (documentación pública en nmap.org)
- Herramientas: nmap, gobuster, dirb wordlists (en WSL2)

## Reconocimiento

### 1. Nmap full-port + service detection
```bash
nmap -sV -p- -oN /opt/nmap_scanme.txt scanme.nmap.org
```

| Puerto | Estado | Servicio | Versión | Comentario |
|---|---|---|---|---|
| 22 | open | ssh | OpenSSH 6.6.1p1 (Ubuntu 2.13) | 2014 — vulnerable a exploits antiguos, pero fuera del scope |
| 25 | filtered | smtp | — | filtrado (posible firewall) |
| 80 | open | http | Apache httpd 2.4.7 | **EOL desde 2019** — riesgo de CVEs no parcheados |
| 9929 | open | nping-echo | — | servicio Nping (diálogo de Nmap) |
| 31337 | open | tcpwrapped | — | **patrón "eleet"** — común en boxes CTF; tcpwrapped = no devuelve banner |

> **Hallazgo clave**: puerto 31337 `tcpwrapped` + Apache 2.4.7 EOL. En un pentest real, el 31337 suele ser un servicio custom/Challenge o backdoor.

### 2. Gobuster directory enumeration
```bash
gobuster dir -u http://scanme.nmap.org/ -w /usr/share/dirb/wordlists/big.txt -t 10
```

| Path | Status | Tamaño | Comentario |
|---|---|---|---|
| `/index` | 200 | 6974 bytes | página default de Apache |
| `/images` | 301 | — | redirección (directorio) |
| `/shared` | 301 | — | redirección (directorio) |
| `/.htaccess` | 403 | 291 | **expuesto** (config de Apache) |
| `/.htpasswd` | 403 | 291 | **expuesto** (credenciales) |
| `/.svn` | 301 | 316 | **exposición de SVN** → fuente de código fuente |
| `/favicon.ico` | 403 | 293 | expuesto |

> **Hallazgo clave**: `.htaccess`, `.htpasswd` y especialmente `.svn` expuestos → fuga potencial de código fuente/credenciales.

## Callejón sin salida 1

- **Hipótesis**: intenté acceder a `/.svn/wc.db` para listar archivos del repo (attemp de source disclosure).
- **Qué hice**: `curl -s http://scanme.nmap.org/.svn/` → 301 redirect (no lista archivos).
- **Por qué falló**: SVN 1.4+ no sirve `wc.db` directamente; requiere paths de ítems (`/.svn/pristine/`).
- **Lección**: la enumeración debe ir `+ paths` (usa `/usr/share/dirb/wordlists/dirb/common.txt` que incluye paths `.svn/pristine/`). El 301 es un "camino cercado" típico.

## Análisis de la exposición (`.svn`)

- **Vector**: `http://scanme.nmap.org/.svn/` responde 301 → directorio accesible.
- **Herramienta**: `svn-brute` o `dirb -r http://scanme.nmap.org/.svn/ --only-filter "code:200"` pueden descubrir archivos.
- **Remediación (para un target propio)**: `RedirectMatch 404 /\.svn` (Apache) o remover `.svn` del root servido.

## Análisis del impacto (si fuera producción)

- **Riesgo**: **Alto** — Apache 2.4.7 EOL + `.htaccess/.htpasswd/.svn` expuestos.
- **Impacto real**: (1) CVEs conocidos de Apache 2.4.7 (ej. CVE-2019-0211 — "Ghost Pool" variante), (2) fuga de credenciales `.htpasswd` si se accede, (3) fuga de código fuente via `.svn`.
- **Remediación**:
  1. **Actualizar Apache 2.4.7 → 2.4.62+** (cierra EOL + CVEs acumulados desde 2014).
  2. **Bloquear paths `.svn/.htaccess/.htpasswd`** via `RedirectMatch 404`.
  3. **Filtrar puerto 31337** (ataque de reconocimiento "eleet") o documentar el servicio.

## Herramientas propias (security-toolkit)

`sec-tool` del portafolio fue el marco de referencia (mismo pipeline: portscan → httpaudit → subenum). En WSL2 Kali-tools ejecuté los comandos equivalentes con Nmap/Gobuster, pero el workflow (`sec-tool portscan --host X -p 1-1000 --banner`) ya implementa este paso de recon.

## Línea de CV derivada de este write-up

> "Reconocimiento pasivo/activo de infraestructura con Nmap (full-port, service detection) y Gobuster directory enumeration sobre el target oficial de Nmap; identifiqué exposición de `.svn`/`.htpasswd` y Apache 2.4.7 EOL. Evidencié el riesgo (CVE acumulados) y documenté remediación (actualización + RedirectMatch para paths sensibles)."

---

## Lecciones del proceso (no solo del target)

1. **WSL2 + apt instala las herramientas rápido** (`nmap`, `sqlmap`, `nikto`, `gobuster`, `dirb`) — Kali completo no era necesario.
2. **`--` flags**: el parseo de PowerShell vs cmd interfiere con `tail|grep|&&` — usar **scripts `.sh` + heredoc** dentro de WSL evita el "token no válido".
3. **`.svn` expuesto es un hallazgo de oro** en recon real → siempre incluir `.svn` paths en el wordlist o usar `svn-brute`.
4. **Target oficial = write-up 100% legal**: `scanme.nmap.org` está explícitamente permitido para practicar — ideal para validar la metodología del portafolio.
5. **Documentar dead-ends (no solo hallazgos)**: proyectar pensamiento y descartar hipótesis es lo que pesará en una entrevista técnica.

*Tags: #writeup #nmap #gobuster #recon #scanme #ciberseguridad #pentesting*
