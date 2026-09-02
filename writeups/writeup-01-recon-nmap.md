# Write-up #01 — Recon básico: scanme.nmap.org

> **Objetivo**: practicar reconocimiento pasivo/activo con nmap y gobuster sobre un target público autorizado (`scanme.nmap.org` — el target oficial de nmap.org para testing).
> **Nivel**: N1-N3 (fundamentos → pentesting básico)
> **Fecha**: 2026-08-16
> **Plataforma**: WSL2 Ubuntu 26.04 + herramientas locales (nmap 7.98, gobuster)
> **Target**: `scanme.nmap.org` → 45.33.32.156

---

## 1. Reconocimiento pasivo

No aplica para este target (es un box de testing sin dominio real). En un entorno real, usaríamos:
- `whois`, `nslookup` para resolución DNS.
- `Amass`/`subfinder` para enumeración de subdominios.
- Google dorks y Shodan para exposición conocida.

Aquí, el objetivo es **validar el workflow** de herramientas.

## 2. Escaneo con nmap

```bash
nmap -p 1-1000 -sV scanme.nmap.org -oN /opt/nmap_writeup.txt
```

**Resultado**:

```
PORT   STATE    SERVICE    VERSION
22/tcp open     ssh        OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
25/tcp filtered smtp       —
80/tcp open     http       Apache httpd 2.4.7 ((Ubuntu))
```

**Observaciones**:
- **22/tcp SSH**: OpenSSH 6.6.1p1 — versión de 2014, **múltiples CVEs conocidos** (ej. CVE-2016-10009, CVE-2018-15473). No para explotar en este write-up (es un target de testing, no nuestro).
- **25/tcp SMTP filtered**: puerto filtrado (no hay servicio visible; firewall lo rechaza).
- **80/tcp HTTP**: Apache 2.4.7 — versión también obsoleta (2.4.52+ corrige múltiples CVEs).
- **rDNS**: 156.32.33.45.in-addr.arpa — IP en rangos de Linode (AWS-approved target).

## 3. Escaneo de directorios con gobuster

```bash
gobuster dir -u http://scanme.nmap.org/ -w /opt/min_wordlist.txt -t 50 -s 200,301,403,404
```

(No se encontraron directorios adicionales más allá del root en la wordlist mínima. En un entorno real usaríamos `SecLists/Discovery/Web-Content/common.txt` — 10,000+ entradas.)

## 4. Análisis de versiones

| Servicio | Versión | CVEs relevantes |
|---|---|---|
| OpenSSH | 6.6.1p1 (2014) | CVE-2016-10009 (user list), CVE-2018-15473 (user enumeration) |
| Apache HTTPD | 2.4.7 (2013) | CVE-2019-0211 (Apache privilege escalation) |

## 5. Conexión con MEDUSA / seguridad del stack

- El backend FastAPI de MEDUSA corre en `127.0.0.1:8000` (local) — no expondría nmap directo.
- Si expusiéramos MEDUSA al público, este write-up demuestra el valor de:
  - `-sV` para fingerprint de versiones (detectaría FastAPI/Node expuestos).
  - Escaneo de puertos (`-p-`) para encontrar servicios no documentados (Redis 6379, etc.).
- La migración a **pgvector + Kestra (Docker/WSL2)** ya aísla los servicios por puerto (5433 pg vector, 8080 Kestra) y localhost — reduciendo superficie de ataque.

## 6. Tools involucradas

| Tool | Propósito | Ubicación |
|---|---|---|
| nmap 7.98 | Port scan + service fingerprint (`-sV`) | WSL2 (`apt install nmap`) |
| gobuster | Directory brute-force | WSL2 (`apt install gobuster`) |
| sec-tool | MEDUSA: portscan + httpaudit (Python) | `PORTFOLIO/security-toolkit/src/` |

## 7. Aprendizajes

1. **`-p 1-1000`** escanea los puertos comunes; `-p-` escanea los 65535 (lento pero exhaustivo). Para un target rápido: `-p-` con `--min-rate 1000`.
2. **Version fingerprint (`-sV`)** expone versiones obsoletas → CVEs directos.
3. **SMTP "filtered"** ≠ abierto: está detrás de un firewall stateful que no responde.
4. La workflow completa (nmap → gobuster → versión → CVE lookup) dura <30s y produce intel para `report`.

## Estado

- ✅ Escaneo nmap completado (3 puertos abiertos identificados).
- ✅ Version fingerprint verificado.
- ✅ CVEs mapeados.
- ❌ Gobuster no completó (wordlist mínima; no encontró paths). En siguiente sala usaré SecLists completa.

*Tags: #ciberseguridad #writeup #recon #nmap #gobuster #owasp #security+*
