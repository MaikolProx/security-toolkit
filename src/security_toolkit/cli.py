"""Command-line entry point (sec-tool)."""
from __future__ import annotations

import argparse
import json
import sys


def cmd_portscan(args) -> int:
    from .core import parse_ports
    from .portscan import scan

    ports = parse_ports(args.ports)
    results = scan(args.host, ports, timeout=args.timeout, grab_banner=args.banner)
    print(f"[portscan] {args.host}: {len(results)} puerto(s) abierto(s)")
    for r in results:
        line = f"  {r['port']:<6} open  {r['service'] or '?'}"
        if r.get("banner"):
            line += f"  banner: {r['banner'][:80]}"
        print(line)
    return 0


def cmd_subenum(args) -> int:
    from .subenum import enumerate_subdomains, read_wordlist

    words = read_wordlist(args.wordlist)
    print(f"[subenum] {len(words)} palabras probadas en {args.domain}")
    found = enumerate_subdomains(args.domain, words, max_threads=args.threads)
    for fqdn in found:
        print(f"  {fqdn}")
    print(f"[subenum] {len(found)} subdominio(s) que resuelven")
    return 0


def cmd_httpaudit(args) -> int:
    from .httpaudit import audit

    result = audit(args.url)
    print(f"[httpaudit] {args.url} -> HTTP {result.status}")
    for finding in result.findings:
        print(f"  {finding}")
    print(f"[httpaudit] {len(result.findings)} hallazgo(s)")
    return 0


def cmd_jwtdump(args) -> int:
    from .jwt import inspect

    result = inspect(args.token)
    print(json.dumps({"header": result.header, "payload": result.payload}, indent=2, ensure_ascii=False))
    for issue in result.issues:
        print(f"[!] {issue}")
    return 0


def cmd_dirbust(args) -> int:
    from .dirbust import bust
    from .subenum import read_wordlist

    words = read_wordlist(args.wordlist)
    hits = bust(args.url, words, max_threads=args.threads, timeout=args.timeout)
    print(f"[dirbust] {args.url} ({len(words)} rutas)")
    for path, status in hits:
        print(f"  {status:<4} /{path}")
    print(f"[dirbust] {len(hits)} hallazgo(s)")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="sec-tool", description="Security Toolkit (solo stdlib)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("portscan", help="escaneo de puertos TCP")
    p.add_argument("--host", required=True, help="host objetivo")
    p.add_argument("-p", "--ports", required=True, help="ej. 22,80,443 o 1-1000")
    p.add_argument("--timeout", type=float, default=1.0)
    p.add_argument("--banner", action="store_true", help="capturar banner")
    p.set_defaults(fn=cmd_portscan)

    p = sub.add_parser("subenum", help="enumeración de subdominios")
    p.add_argument("-d", "--domain", required=True)
    p.add_argument("-w", "--wordlist", required=True)
    p.add_argument("--threads", type=int, default=64)
    p.set_defaults(fn=cmd_subenum)

    p = sub.add_parser("httpaudit", help="auditoría de cabeceras de seguridad")
    p.add_argument("-u", "--url", required=True)
    p.set_defaults(fn=cmd_httpaudit)

    p = sub.add_parser("jwtdump", help="inspección de tokens JWT")
    p.add_argument("-t", "--token", required=True)
    p.set_defaults(fn=cmd_jwtdump)

    p = sub.add_parser("dirbust", help="fuerza bruta de directorios")
    p.add_argument("-u", "--url", required=True)
    p.add_argument("-w", "--wordlist", required=True)
    p.add_argument("--threads", type=int, default=32)
    p.add_argument("--timeout", type=float, default=5.0)
    p.set_defaults(fn=cmd_dirbust)

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
