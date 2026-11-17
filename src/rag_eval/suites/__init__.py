from rag_eval.suites.abstention import run_abstention
from rag_eval.suites.chunking import run_chunking
from rag_eval.suites.citation import run_citation
from rag_eval.suites.extraction import run_extraction
from rag_eval.suites.faithfulness import run_faithfulness
from rag_eval.suites.ground_truth_suite import run_ground_truth
from rag_eval.suites.retrieval import run_retrieval

ALL_SUITES = {
    "extraction": run_extraction,
    "chunking": run_chunking,
    "retrieval": run_retrieval,
    "ground_truth": run_ground_truth,
    "faithfulness": run_faithfulness,
    "citation": run_citation,
    "abstention": run_abstention,
}
