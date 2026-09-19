#!/usr/bin/env python3
"""Gera dist/tokens.css e dist/RULES.md a partir de tokens.json e rules.json.

O CSS é GERADO — nunca editado à mão. Se alguém editar, a próxima geração
sobrescreve e a CI falha (``--check``) enquanto o commitado divergir do gerado.

Uso:
    python scripts/build.py           # escreve dist/
    python scripts/build.py --check   # falha (exit 1) se dist/ divergir do gerado

Sem dependências: stdlib apenas. O ecossistema já roda Python na CI e
consumir CSS não exige Node.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "tokens.json"
RULES = ROOT / "rules.json"
DIST = ROOT / "dist"

RULE_IDS = tuple(f"R0{i}" for i in range(1, 8))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_tokens(data: dict) -> list[str]:
    errors: list[str] = []
    if not data.get("prefix"):
        errors.append("tokens.json: 'prefix' ausente")
    for gname, group in (data.get("groups") or {}).items():
        tokens = group.get("tokens") or {}
        if not tokens:
            errors.append(f"tokens.json: grupo {gname!r} sem tokens")
        for tname, tok in tokens.items():
            value = tok.get("value") if isinstance(tok, dict) else None
            if value in (None, ""):
                errors.append(f"tokens.json: {gname}.{tname} sem 'value'")
    return errors


def validate_rules(data: dict, tokens: dict) -> list[str]:
    errors: list[str] = []
    rules = data.get("rules") or []
    ids = [r.get("id") for r in rules]
    if tuple(ids) != RULE_IDS:
        errors.append(f"rules.json: esperado exatamente {list(RULE_IDS)}, encontrado {ids}")
    known = {f"{g}.{t}" for g, grp in (tokens.get("groups") or {}).items() for t in (grp.get("tokens") or {})}
    for r in rules:
        status = r.get("status")
        if status not in ("ACTIVE", "PENDENTE"):
            errors.append(f"rules.json: {r.get('id')} status invalido {status!r}")
        if status == "ACTIVE" and not r.get("text"):
            errors.append(f"rules.json: {r.get('id')} ACTIVE sem texto")
        if status == "PENDENTE" and r.get("text"):
            errors.append(f"rules.json: {r.get('id')} PENDENTE com texto — ou e ACTIVE ou nao tem texto")
        for ref in r.get("tokens") or []:
            if ref not in known:
                errors.append(f"rules.json: {r.get('id')} referencia token inexistente {ref!r}")
    return errors


def css_name(prefix: str, group: str, token: str) -> str:
    # color.semantic.authority -> --liceu-authority ; layout.rail -> --liceu-layout-rail
    # Grupos de cor colapsam o prefixo 'color.*' (a cor e o nome); os demais mantem o grupo.
    # 'font' tambem colapsa: --liceu-sans / --liceu-mono e o nome que os
    # drawers (consumidor 0.1.0) ja usam.
    if group.startswith("color.") or group == "font":
        return f"--{prefix}-{token}"
    return f"--{prefix}-{group}-{token}"


def render_css(data: dict, source_digest: str) -> str:
    prefix = data["prefix"]
    lines = [
        f"/* @{data['name'].lstrip('@')} {data['version']} — GERADO de tokens.json (sha256 {source_digest[:16]}). NAO EDITAR. */",
        f"/* Fonte: {data.get('source', '')} */",
        ":root {",
    ]
    for gname, group in data["groups"].items():
        lines.append(f"  /* {gname} — {group.get('description', '')} */")
        for tname, tok in group["tokens"].items():
            comment = tok.get("meaning") or tok.get("role") or ""
            suffix = f"  /* {comment} */" if comment else ""
            lines.append(f"  {css_name(prefix, gname, tname)}: {tok['value']};{suffix}")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    lines.append(':root:not([data-theme="light"]) { color-scheme: dark; }')
    lines.append("")
    return "\n".join(lines)


def render_rules_md(data: dict, source_digest: str) -> str:
    out = [
        f"# Regras R01–R07 — @liceu/design-tokens {data['version']}",
        "",
        f"<!-- GERADO de rules.json (sha256 {source_digest[:16]}). NAO EDITAR. -->",
        "",
        f"> {data['principle']}",
        "",
        "Quem consome os tokens recebe a constituição junto. Uma regra `PENDENTE` é uma",
        "regra cujo texto ainda não foi localizado — ela existe, está numerada, e não é",
        "inventada aqui.",
        "",
        "| Regra | Estado | Texto | O que impede | Tokens |",
        "|---|---|---|---|---|",
    ]
    for r in data["rules"]:
        text = r["text"] or "*(texto pendente)*"
        prevents = r["prevents"] or "—"
        toks = ", ".join(f"`{t}`" for t in r["tokens"]) or "—"
        out.append(f"| {r['id']} | {r['status']} | {text} | {prevents} | {toks} |")
    out.append("")
    for r in data["rules"]:
        if r.get("note"):
            out.append(f"**{r['id']}** — {r['note']}")
            out.append("")
    return "\n".join(out)


def build() -> dict[str, str]:
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    rules = json.loads(RULES.read_text(encoding="utf-8"))
    errors = validate_tokens(tokens) + validate_rules(rules, tokens)
    if errors:
        for e in errors:
            print(f"ERRO {e}", file=sys.stderr)
        sys.exit(2)
    return {
        "tokens.css": render_css(tokens, sha256(TOKENS)),
        "RULES.md": render_rules_md(rules, sha256(RULES)),
    }


def main(argv: list[str]) -> int:
    outputs = build()
    if "--check" in argv:
        bad = 0
        for name, content in outputs.items():
            path = DIST / name
            current = path.read_text(encoding="utf-8") if path.exists() else None
            ok = current == content
            bad += not ok
            print(("OK   " if ok else "DIFF ") + f"dist/{name}")
        if bad:
            print("dist/ divergente do gerado: rode `python scripts/build.py` e commite. O CSS nao se edita a mao.", file=sys.stderr)
            return 1
        return 0
    DIST.mkdir(exist_ok=True)
    for name, content in outputs.items():
        (DIST / name).write_text(content, encoding="utf-8", newline="\n")
        print(f"escrito dist/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
