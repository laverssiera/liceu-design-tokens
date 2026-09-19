# Regras R01–R07 — @liceu/design-tokens 0.1.0

<!-- GERADO de rules.json (sha256 6734edd801867641). NAO EDITAR. -->

> Uma interface que inventa evidência viola a constituição que deveria tornar visível. Onde não há dado, a interface diz que não há.

Quem consome os tokens recebe a constituição junto. Uma regra `PENDENTE` é uma
regra cujo texto ainda não foi localizado — ela existe, está numerada, e não é
inventada aqui.

| Regra | Estado | Texto | O que impede | Tokens |
|---|---|---|---|---|
| R01 | ACTIVE | Botão de recomendação nunca pode parecer autorização. | botão de recomendação parecer autorização | `color.semantic.intelligence`, `color.semantic.authority` |
| R02 | ACTIVE | Ausência de dado se declara, nunca se preenche com exemplo. | preencher ausência com exemplo | `color.status.blocked` |
| R03 | PENDENTE | *(texto pendente)* | — | — |
| R04 | ACTIVE | Dourado só aparece onde há autoridade estabelecida. | dourado sem autoridade estabelecida | `color.semantic.authority` |
| R05 | ACTIVE | Campo mono vazio nunca vira zero nem id fictício. | campo mono vazio virar zero ou id fictício | `font.mono`, `color.status.blocked` |
| R06 | PENDENTE | *(texto pendente)* | — | — |
| R07 | ACTIVE | A barra de proveniência nunca se esconde quando falta dado. | esconder a barra de proveniência quando falta dado | `layout.prov`, `color.status.blocked` |

**R01** — Recomendar (JOHN) e decidir (Mãe) são atos de camadas diferentes. A distinção é visual antes de textual: o usuário aprende pela cor antes de ler o rótulo. Explain, Simulate, Compare e Evidence são leitura; Escalate transfere para quem decide — não decide.

**R02** — Campo sem valor mostra travessão (—). Um drawer com um id inventado ensinaria o usuário a confiar num número que não existe. Dado parcial não vira dado inventado.

**R03** — Texto não localizado nos artefatos Universal Shell e Drawers; o L6-FE-001 não está em repositório. Registrado como pendente para não inventar regra (R02 aplicada às próprias regras).

**R04** — Dourado não decora: dourado significa autoridade. O authority_epoch no topo só mostra número quando houver época vigente; até lá, 'não estabelecida'.

**R05** — Identificadores, épocas, hashes e contagens vivem em mono. Vazio é travessão em blocked; '0' só quando a contagem é de fato zero (ex.: 'fontes 0').

**R06** — Texto não localizado nos artefatos Universal Shell e Drawers; o L6-FE-001 não está em repositório. Registrado como pendente para não inventar regra.

**R07** — Permanente, por constituição. Passa de vermelha a preenchida por campo, não de uma vez: contexto, evidência, autoridade, lineage, ciclo.
