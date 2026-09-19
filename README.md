# @liceu/design-tokens

Tokens de design do LICEU 6.0 (L6-FE-001) e as regras R01–R07 que viajam com eles.
Mesmo tratamento que o kit de protocolo recebeu na ADR-001: **repositório próprio,
fonte única, versão por tag**. Quem consome instala; ninguém copia.

## O que é fonte e o que é gerado

| Arquivo | Papel |
|---|---|
| `tokens.json` | **Fonte.** Cores (foundation, semantic, status), fontes, raios, movimento, layout do shell. |
| `rules.json` | **Fonte.** As sete regras, com estado, texto, o que impedem e os tokens que envolvem. |
| `dist/tokens.css` | **Gerado** de `tokens.json`. Nunca editado à mão. |
| `dist/RULES.md` | **Gerado** de `rules.json`. A constituição que o consumidor recebe junto. |

Se alguém editar o CSS, a próxima geração sobrescreve — e a CI falha antes disso:
`python scripts/build.py --check` compara o commitado com o gerado.

```bash
python scripts/build.py          # regenera dist/
python scripts/build.py --check  # o que a CI roda
```

Gerador em Python (stdlib) porque a CI do ecossistema já roda Python e consumir CSS
não exige Node.

## Consumir

```bash
npm i github:laverssiera/liceu-design-tokens#v0.1.0
```

```css
@import "@liceu/design-tokens/tokens.css";
.card.auth { border-top-color: var(--liceu-authority); }
```

Ou, sem npm: copiar **nada** — apontar para `dist/tokens.css` da tag. A identidade do
arquivo é o sha256 de `tokens.json` no cabeçalho.

## A cor é a camada constitucional

| Token | Camada | Quem produz |
|---|---|---|
| `--liceu-intelligence` | Cognition Plane | JOHN recomenda |
| `--liceu-evidence` | Perception Plane | CEFEIDA evidencia |
| `--liceu-authority` | Authority Control Plane | Mãe autoriza — só onde há autoridade estabelecida (R04) |
| `--liceu-execution` | Reality Plane | OPERA executa |

Dourado não decora. Ausência de dado se declara com travessão, nunca com exemplo (R02).

## As regras

Ver [`dist/RULES.md`](dist/RULES.md). Cinco têm texto (R01, R02, R04, R05, R07); duas estão
**PENDENTE** (R03, R06): o texto não foi localizado nos artefatos de referência e o L6-FE-001
não está em repositório. Estão numeradas e vazias de propósito — inventar regra seria violar
a R02 nas próprias regras. Quando o texto vier, é MINOR.

## Versionamento

- Renomear ou remover token público: **MAJOR**.
- Acrescentar token ou preencher regra PENDENTE: **MINOR**.
- Mudar valor sem mudar nome: **PATCH** — e vale perguntar se a Constituição mudou.

Tag `v0.1.0` = os 17 nomes que o Universal Shell e os Drawers já usam.
