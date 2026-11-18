# Arquitectura · rag-eval-platform

Evaluación local de un pipeline RAG por etapas. Sin APIs de pago obligatorias.

## Offline vs online (qué medimos)

```mermaid
flowchart LR
  subgraph offline [Offline_Corpus]
    Docs[Docs_sinteticos] --> Extract[Extract]
    Extract --> Chunk[Chunk]
    Chunk --> Index[Index_lexico]
  end
  subgraph online [Online_Query]
    Q[Pregunta_GT] --> Retrieve[Retrieve_topk]
    Retrieve --> Answer[Answer_extractivo]
    Answer --> Suites[7_suites]
  end
  Index --> Retrieve
  Suites --> Report[results_json_md_html]
  Report --> Baseline[baseline_compare]
```

## Suites por etapa

| Etapa | Suite | Falla típica que detecta |
|---|---|---|
| Lectura | `extraction` | archivo vacío / no leído |
| Fragmentación | `chunking` | doc sin cobertura de chunks |
| Búsqueda | `retrieval` | top-k sin el doc fuente |
| Respuesta | `ground_truth` | no se acerca a lo esperado |
| Fidelidad | `faithfulness` | claims sin respaldo |
| Citas | `citation` | cita a doc incorrecto |
| Silencio | `abstention` | inventa sin evidencia |

## Despliegue documentado (AWS, sin credenciales)

```mermaid
flowchart TB
  Dev[Laptop_Docker] --> GH[GitHub_Actions]
  GH -->|"pytest + rag-eval"| Artifact[metrics_JSON]
  Artifact --> Gates[llm-ci-gates]
  Gates -->|PASS| Merge[merge_main]
  Gates -->|FAIL| Block[bloquear_PR]
  subgraph aws_doc [AWS_referencia]
    ECR[ECR_imagen]
    ECS[ECS_Fargate_job]
    S3[S3_results]
  end
  Merge -.->|"opcional batch nocturno"| ECS
  ECS -.-> S3
```

En este repo el camino productivo es **local + CI**. AWS queda como mapa: imagen Docker en ECR, job batch que escribe métricas en S3, y el mismo contrato JSON que consume `llm-ci-gates`.
