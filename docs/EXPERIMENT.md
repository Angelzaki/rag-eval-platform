# Experimentos · rag-eval-platform

## Hipótesis

Cuando el corpus crece (pocos docs → más docs), sin suites por etapa **no sabes dónde se rompió** el RAG. Un Ground Truth fijo + baseline debería detectar regresiones y comparar escenarios A/B.

## Diseño

| Variable | scenario_a | scenario_b |
|---|---|---|
| Corpus | `samples/docs_a` (4 docs) | `samples/docs_b` (6 docs, incluye A + extras) |
| Ground Truth | `samples/ground_truth/questions.jsonl` (20) | mismo |
| Pipeline | extract → chunk → retrieve → answer extractivo | mismo |
| Métrica global | media de 7 suites | misma |

## Resultados medidos (corrida local)

| Suite | A | B | Delta |
|---|---:|---:|---:|
| extraction | 100% | 100% | 0 |
| chunking | 100% | 100% | 0 |
| retrieval | 100% | 100% | 0 |
| ground_truth | 83% | 100% | +17 |
| faithfulness | 89% | 100% | +11 |
| citation | 83% | 100% | +17 |
| abstention | 85% | 83% | -2 |
| **overall** | **89.7%** | **97.7%** | **+8** |

Fuente: `results/scenario_a.md`, `results/scenario_b.md` (reproducibles con `python -m rag_eval` y `scripts/compare_ab.py`).

## Lectura rápida

- Ampliar el corpus **mejoró** ground truth / faithfulness / citation en este sample sintético (más contexto útil para las preguntas del GT).
- Abstención bajó ligeramente en B: más documentos también aumentan el riesgo de “parecer que hay evidencia” en preguntas fuera de dominio.
- Extracción/chunking/retrieval al 100% en ambos: el cuello de botella aquí no era indexar, era **calidad de respuesta y silencio**.
