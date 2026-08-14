# Security Toolkit

Herramientas de red y web para auditorías con permiso y laboratorios (TryHackMe, HackTheBox). Solo stdlib de Python, sin dependencias.

| Herramienta | Qué hace | Uso |
|---|---|---|
| `portscan` | Escaneo TCP conectado con detección de servicio y banner | `sec-tool portscan -h 10.10.10.1 -p 1-1000` |
| `subenum` | Enumeración de subdominios por DNS + diccionario | `sec-tool subenum -d ejemplo.com -w wordlist.txt` |
| `httpaudit` | Auditoría de cabeceras de seguridad HTTP | `sec-tool httpaudit -u https://ejemplo.com` |
| `jwtdump` | Decodificación e inspección de tokens JWT | `sec-tool jwtdump -t <token>` |
| `dirbust` | Fuerza bruta de directorios con wordlist (códigos HTTP) | `sec-tool dirbust -u http://10.10.10.1 -w wordlist.txt` |

Por qué stdlib solo: puedo leer el código entero en una tarde, funciona en cualquier máquina del laboratorio sin instalar nada, y cada pieza está testeada.

Aviso: úsalo solo contra sistemas propios o con autorización por escrito. Escanear sin permiso es ilegal en casi todas las jurisdicciones.

## Instalación

```bash
pip install -e .
```

## Ejemplos

```bash
# Escaneo de puertos con banner
sec-tool portscan -h 10.10.10.1 -p 22,80,443,3306 --banner

# Enumerar subdominios desde diccionario
sec-tool subenum -d tryhackme.com -w wordlists/subdomains.txt

# Auditar cabeceras de seguridad
sec-tool httpaudit -u https://mi-sitio.com

# Decodificar un JWT (solo inspección, no valida firma)
sec-tool jwtdump -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Tests

```bash
pytest -q
```

Cubren parsing de rangos de puertos, clasificación de puertos comunes, parseo de cabeceras HTTP y decodificación JWT, incluida la firma débil `alg:none`.

## Write-ups

En `writeups/` está la plantilla que uso para cada máquina resuelta. Incluyo los callejones sin salida, que es lo que más se aprende y lo que más preguntan en las entrevistas.
