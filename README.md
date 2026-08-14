# Security Toolkit

> Kit de herramientas de seguridad de red y aplicaciones, **implementado desde cero** (solo stdlib de Python) para auditorías autorizadas y laboratorios (TryHackMe / HackTheBox). Sin dependencias, sin bins externos: cada herramienta es legible, testeable y auditable.

## Herramientas

| Herramienta | Qué hace | Uso |
|---|---|---|
| `portscan` | Escaneo TCP conectado con detección de servicio y banner | `sec-tool portscan -h 10.10.10.1 -p 1-1000` |
| `subenum` | Enumeración de subdominios por DNS + diccionario | `sec-tool subenum -d ejemplo.com -w wordlist.txt` |
| `httpaudit` | Auditoría de cabeceras de seguridad HTTP | `sec-tool httpaudit -u https://ejemplo.com` |
| `jwtdump` | Decodificación e inspección de tokens JWT | `sec-tool jwtdump -t <token>` |
| `dirbust` | Fuerza bruta de directorios/archivos con wordlist (códigos HTTP) | `sec-tool dirbust -u http://10.10.10.1 -w wordlist.txt` |

> **Aviso legal**: úsalo únicamente contra sistemas de tu propiedad o con autorización por escrito. El escaneo sin permiso es ilegal en casi todas las jurisdicciones.

## Instalación

```bash
pip install -e .
```

## Ejemplos

```bash
# Escaneo de puertos con detección de banner (conexión real)
sec-tool portscan -h 10.10.10.1 -p 22,80,443,3306 --banner

# Enumerar subdominios desde diccionario
sec-tool subenum -d tryhackme.com -w wordlists/subdomains.txt

# Auditar cabeceras de seguridad de una web
sec-tool httpaudit -u https://mi-sitio.com

# Decodificar un JWT sin validar la firma (solo inspección)
sec-tool jwtdump -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Tests

```bash
pytest -q
```

Cubren parsing de rangos de puertos, clasificación de puertos comunes, parseo de cabeceras HTTP y decodificación JWT (incluyendo el ataque de firma débil — `alg:none`).

## Por qué sin dependencias

- Cualquier evaluador puede revisar el código completo en minutos (importa para entrevistas y para red team review).
- Funciona en el laboratorio de TryHackMe sin instalar nada más que Python.
- Cada vulnerabilidad que detecta está documentada en `writeups/` con la metodología usada.

## Write-ups (metodología publicada)

- `writeups/TEMPLATE.md` — plantilla de write-up CTF con secciones Scope / Recon / Finding / Impact / Remediation, incluyendo los callejones sin salida (dead-ends), que es lo que más valoran los hiring managers.
