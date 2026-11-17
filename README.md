<div align="center">

# rag-eval-platform

**Evaluación local de sistemas RAG** · Angel Salazar

`extracción → chunking → retrieval → ground truth → faithfulness → citas → abstención`

</div>

---

### `$ whoami`

```text
objetivo: detectar dónde se rompe el RAG cuando el corpus crece
no_objetivo: "el modelo responde bonito"
modo: 100% local · sin cloud · sin API keys obligatorias
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
| `extraction` | corpus legible |
| `chunking` | cobertura de fragmentos |
| `retrieval` | top-k trae el doc fuente |
| `ground_truth` | respuesta vs esperado |
| `faithfulness` | sin inventos |
| `citation` | citas correctas |
| `abstention` | sabe callarse |

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

- **scenario_a** → `samples/docs_a`
- **scenario_b** → `samples/docs_b`

---

### `$ ls related`

`local-rag-pipeline` · `retrieval-tuner-local` · `abstention-lab-local` · `eval-hub-local`

---

Hecho en Lima · Angel Salazar · CIP 404730
