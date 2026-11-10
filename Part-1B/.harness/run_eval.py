import json
import sys
import time
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "Part-1B"))
from src.agent import parse_reminder

def run():
    dataset_path = repo_root / "Part-1B" / "evals" / "dataset.json"
    dataset = json.loads(dataset_path.read_text())

    total = len(dataset)
    l1_pass = 0
    l2_pass = 0
    l3_pass = 0
    results = []

    print("=" * 65)
    print("  RUNNING LIVE 3-TIER EVALUATION (gemini-flash-lite-latest)")
    print(f"  Dataset: {total} cases | Targets: L1 100%, L2 100%, L3 >= 90%")
    print("=" * 65)

    for case in dataset:
        c_id = case["id"]
        inp = case["input"]
        exp_clarify = case["expected_needs_clarification"]
        exp_title = case.get("expected_title")

        l1 = False
        l2 = False
        l3 = False
        out_dict = None
        err = None

        try:
            out = parse_reminder(inp)
            out_dict = out.model_dump()
            l1 = True
        except Exception as e:
            err = str(e)

        if l1 and out:
            # Layer 2: Invariant Check
            # - If clarification is expected, title must be set to UNSPECIFIED or a preserved action string.
            # - Output title must never be None/empty.
            l2 = bool(out.title and len(out.title.strip()) > 0)

            # Layer 3: Semantic Accuracy against Ground Truth
            clarify_match = (out.needs_clarification == exp_clarify)
            
            if exp_title is not None:
                # Direct ground-truth string match (case-insensitive)
                title_match = (out.title.strip().lower() == exp_title.strip().lower())
            else:
                # If ground-truth title is None:
                # If clarify expected -> title should be UNSPECIFIED
                # If recurring/clarify=False -> title should be a non-empty actionable summary
                if exp_clarify:
                    title_match = (out.title == "UNSPECIFIED")
                else:
                    title_match = bool(out.title and out.title != "UNSPECIFIED")

            l3 = clarify_match and title_match

        if l1: l1_pass += 1
        if l2: l2_pass += 1
        if l3: l3_pass += 1

        status = "PASS" if (l1 and l2 and l3) else "FAIL"
        clean_inp = inp[:30].replace("\n", " ")
        print(f"[{status}] Case {c_id:02d}: {clean_inp:<30} -> L1:{int(l1)} L2:{int(l2)} L3:{int(l3)}")

        results.append({
            "id": c_id,
            "input": inp,
            "expected_clarification": exp_clarify,
            "expected_title": exp_title,
            "actual": out_dict,
            "error": err,
            "l1": l1,
            "l2": l2,
            "l3": l3,
            "passed": (l1 and l2 and l3)
        })
        time.sleep(0.4)

    l1_rate = (l1_pass / total) * 100.0
    l2_rate = (l2_pass / total) * 100.0
    l3_rate = (l3_pass / total) * 100.0
    decision = "ACCEPT" if (l1_rate == 100.0 and l2_rate == 100.0 and l3_rate >= 90.0) else "REVISE"

    print("=" * 65)
    print("LIVE EVALUATION METRIC REPORT")
    print(f"  Layer 1 (Schema Validity)    : {l1_pass}/{total} ({l1_rate:.1f}%) [Threshold: 100%]")
    print(f"  Layer 2 (Invariant Integrity): {l2_pass}/{total} ({l2_rate:.1f}%) [Threshold: 100%]")
    print(f"  Layer 3 (Semantic Accuracy)  : {l3_pass}/{total} ({l3_rate:.1f}%) [Threshold: >= 90%]")
    print(f"Final Acceptance Decision      : {decision}")
    print("=" * 65)

    evidence_dir = repo_root / "Part-1B" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    out_file = evidence_dir / "eval-results.json"
    out_file.write_text(json.dumps({
        "model": "gemini-flash-lite-latest",
        "temperature": 0.0,
        "l1_rate": l1_rate,
        "l2_rate": l2_rate,
        "l3_rate": l3_rate,
        "decision": decision,
        "total_cases": total,
        "results": results
    }, indent=2))
    print(f"Raw run artifact written to: {out_file}")

if __name__ == "__main__":
    run()
