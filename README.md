<div align="center">

# rag-eval-platform

**Evaluación local de sistemas RAG** · Angel Salazar

`extracción → chunking → retrieval → ground truth → faithfulness → citas → abstención`

</div>

---

### `$ cat problema.md`

En sistemas RAG reales el dolor no es “que el modelo no suene inteligente”.  
El dolor aparece cuando el corpus crece (de pocos docs a +100 PDF) y nadie sabe **en qué etapa se rompió**.

Problemas que atacamos:

| Problema | Qué pasa en la práctica | Cómo lo atacamos aquí |
|---|---|---|
| Evaluación superficial | Se prueban 3 preguntas a mano y “parece bien” | Ground Truth + suites reproducibles |
| Caja negra del pipeline | Falla el producto, pero no sabes si fue extract/chunk/retrieve/generate | 7 suites por etapa |
| Alucinaciones | Responde con seguridad sin respaldo documental | Faithfulness + citation |
| No sabe callarse | Inventa cuando no hay evidencia | Abstention test |
| Regresiones silenciosas | Una “mejora” empeora retrieval y nadie lo nota | Baseline + comparación A/B |
| Cambio de modelo a ciegas | Se cambia Haiku→Sonnet sin métrica | Primero medir, después cambiar LLM |

En corto: convertir pruebas RAG en **ingeniería de evaluación**, no en demos.

---

### `$ whoami`

```text
objetivo: detectar dónde se rompe el RAG cuando el corpus crece
no_objetivo: "el modelo responde bonito"
modo: 100% local · sin cloud · sin API keys obligatorias
autor: Angel Salazar · Lima
```

---

### `$ ./pipeline.sh --eval`

```text
samples/docs_*  +  questions.jsonl (20)
        │
        ▼
   7 suites medibles
        │
        ▼
 results/*.json + *.md + *.html
        │
        ▼
 baseline.json → regresión automática
```

| Suite | Qué valida |
|---|---|
| `extraction` | ¿los documentos se leen bien? |
| `chunking` | ¿la fragmentación pierde contexto? |
| `retrieval` | ¿el top-k trae el doc fuente? |
| `ground_truth` | ¿la respuesta se acerca a lo esperado? |
| `faithfulness` | ¿hay claims sin respaldo? |
| `citation` | ¿las citas apuntan al documento correcto? |
| `abstention` | ¿se abstiene cuando no hay evidencia? |

Escenarios:

- **scenario_a** → corpus actual (`samples/docs_a`)
- **scenario_b** → corpus ampliado (`samples/docs_b`)

Así se simula el salto de “pocos docs” a “corpus más grande” y se mide el impacto.

---

### `$ make local`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m rag_eval --scenario scenario_a --save-baseline
python -m rag_eval --scenario scenario_a
python scripts/compare_ab.py
```

---

### `$ cat decision.md`

Flujo que buscamos:

```text
proponer cambio (chunking / retrieval / prompt / modelo)
        │
        ▼
correr suites + comparar vs baseline
        │
        ▼
aprobar / corregir / rechazar con evidencia
```

Sin Ground Truth y sin métricas, cualquier “mejora” es opinión.

---

### `$ ls related`

`local-rag-pipeline` · `retrieval-tuner-local` · `abstention-lab-local` · `eval-hub-local`

---

Hecho en Lima · Angel Salazar · CIP 404730
