# Write-up: <Nombre de la máquina / laboratorio>

> Plantilla. Usa una por máquina resuelta en TryHackMe / HackTheBox y publícala aquí. El secreto está en incluir **los callejones sin salida**: documentar qué no funcionó muestra cómo piensas, no que fracasaste.

- **Plataforma**: TryHackMe / HackTheBox
- **Máquina**: <nombre>
- **Dificultad**: Easy / Medium / Hard
- **Fecha**: DD/MM/AAAA
- **Ruta de aprendizaje**: <ej. Junior Penetration Tester — Módulo X>

## Resumen ejecutivo (3 frases)

<Qué era el objetivo, qué vector lo comprometió, qué impacto permitía alcanzar.>

## Alcance (Scope)

- IP objetivo: `10.10.x.x`
- Autorización: plataforma de laboratorio (permitido explícitamente)
- Herramientas: nmap, gobuster, burpsuite, <las propias de security-toolkit>

## Reconocimiento

```bash
# escaneo de puertos inicial
sec-tool portscan --host 10.10.x.x -p 1-1000 --banner
# o
nmap -sV -sC -p- 10.10.x.x
```

| Puerto | Servicio | Versión |
|---|---|---|
| 22 | ssh | OpenSSH 8.2 |
| 80 | http | Apache/2.4.41 |

**Hallazgo clave del reconocimiento**: <qué servicio era inusual y por qué llamó la atención>.

## Callejón sin salida (dead-end) 1

- **Hipótesis**: <lo que intenté>.
- **Qué hice**: <comandos>.
- **Por qué falló**: <evidencia>. 
- **Lección**: <qué descarté y por qué esa pista llevaba a otro lado>.

## Explotación

1. <Paso 1: descubrimiento de la vulnerabilidad> — evidencia.
2. <Paso 2: explotación> — payload/script.
3. <Paso 3: acceso> — `user.txt`.

## Escalada de privilegios

1. <Enumeración post-explotación>.
2. <Vector usado> — ejemplo: binario con SUID, cron mal configurado, credenciales en archivo de config.
3. <Resultado> — `root.txt`.

## Análisis del impacto (si fuera producción)

- **Riesgo**: crítico / alto / medio / bajo.
- **Impacto real**: acceso administrativo, robo de datos, RCE.
- **Remediación**:
  1. Actualizar <servicio/versión>.
  2. Aplicar parche/parámetro de hardening X.
  3. Añadir regla de detección (Sigma/YARA) en el SIEM.

## Herramientas propias utilizadas

<Si usaste `sec-tool` (httpaudit, jwtdump, dirbust...), dilo aquí con el output.>

## Línea de CV derivada de este write-up

> "Reconocimiento y explotación de <vector> en la máquina <nombre> (HTB/TryHackMe); documenté la metodología completa incluyendo dead-ends y remediación."
