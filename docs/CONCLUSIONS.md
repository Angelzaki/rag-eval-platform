# Conclusiones · rag-eval-platform

## Qué aprobaría en producción

1. **Gate por suite**, no solo overall. Un 90% global puede esconder abstención rota.
2. **Baseline obligatorio** antes de mergear cambios de chunking / retrieval / prompt.
3. **A/B de corpus** cuando se agregan docs: medir impacto, no asumir “más docs = mejor”.
4. Exportar el JSON de métricas al mismo contrato que consume `llm-ci-gates`.

## Qué rechazaría

1. Demo de 3 preguntas manuales como “evaluación”.
2. Cambiar modelo (Haiku→Sonnet u Ollama) sin rerun de suites.
3. Subir umbral de overall y bajar el de faithfulness/citation “para que pase el CI”.

## Decisiones de diseño (ADR corto)

| Decisión | Por qué |
|---|---|
| Recuperación léxica local | Reproducible, sin API keys, barato de CI |
| Answer extractivo | Aísla fallas de retrieval/citas sin ruido de un LLM creativo |
| 7 suites | Localiza la etapa rota; un solo score no sirve para debug |
| Datos sintéticos | Cero documentos internos / clientes |

## Siguiente medición útil

- Grid de `top_k` / tamaño de chunk (labs: `retrieval-tuner-local`, `chunk-lab`) alimentando este mismo GT.
- Conectar el JSON de `results/` a `llm-ci-gates` en el workflow del monorepo o del repo consumidor.
