import json
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

from src.agent import ReminderAgent, ReminderOutput


def run_evaluation():
    dataset_path = base_dir / "evals" / "dataset.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    agent = ReminderAgent()
    total_cases = len(dataset)
    layer1_passed = 0
    layer2_passed = 0
    layer3_passed = 0
    overall_passed = 0
    results = []

    print("==================================================")
    print("  RUNNING 3-TIER EVALUATION HARNESS (PART 1B)")
    print("  Target Cases: 15 | L1: 100% | L2: 100% | L3: >=90%")
    print("==================================================")

    for item in dataset:
        case_id = item["id"]
        inp = item["input"]
        exp_clarify = item["expected_needs_clarification"]
        exp_title = item.get("expected_title")
        exp_recurrence = item.get("expected_recurrence")

        case_failures = []
        l1_ok = False
        l2_ok = False
        l3_ok = False
        output = None

        # Layer 1: Schema Validation (Pydantic model_validate_json)
        try:
            raw_response = agent.call_llm(inp)
            output = ReminderOutput.model_validate_json(raw_response)
            l1_ok = True
            layer1_passed += 1
        except Exception as e:
            case_failures.append(f"Layer 1 Schema Error: {str(e)}")

        # Layer 2: Deterministic Business Invariants
        if l1_ok and output:
            l2_violations = []
            if output.needs_clarification and not output.clarification_question:
                l2_violations.append("Clarification true but question missing")
            if not output.needs_clarification and not output.title:
                l2_violations.append("Clarification false but title missing")

            if not l2_violations:
                l2_ok = True
                layer2_passed += 1
            else:
                case_failures.extend([f"Layer 2 Invariant: {v}" for v in l2_violations])

        # Layer 3: Semantic Quality
        if l1_ok and output:
            l3_violations = []
            if output.needs_clarification != exp_clarify:
                l3_violations.append(f"Clarification flag mismatch: got {output.needs_clarification}, exp {exp_clarify}")
            if exp_title is not None and output.title:
                if exp_title.lower() not in output.title.lower() and output.title.lower() not in exp_title.lower():
                    l3_violations.append(f"Title mismatch: got {output.title}, exp {exp_title}")
            if exp_recurrence is not None:
                if output.recurrence.value != exp_recurrence:
                    l3_violations.append(f"Recurrence mismatch: got {output.recurrence.value}, exp {exp_recurrence}")

            if not l3_violations:
                l3_ok = True
                layer3_passed += 1
            else:
                case_failures.extend([f"Layer 3 Semantic: {v}" for v in l3_violations])

        case_status = "PASS" if (l1_ok and l2_ok and l3_ok) else "FAIL"
        if case_status == "PASS":
            overall_passed += 1

        results.append({
            "id": case_id, "input": inp, "status": case_status,
            "layer_results": {"L1": l1_ok, "L2": l2_ok, "L3": l3_ok},
            "failures": case_failures
        })
        disp = (inp[:35] + "...") if len(inp) > 35 else inp
        print(f"[{case_status}] Case {case_id:02d}: \"{disp}\" (L1:{l1_ok}, L2:{l2_ok}, L3:{l3_ok})")

    l1_pct = (layer1_passed / total_cases) * 100
    l2_pct = (layer2_passed / total_cases) * 100
    l3_pct = (layer3_passed / total_cases) * 100
    verdict = "ACCEPT" if (layer1_passed == total_cases and layer2_passed == total_cases and l3_pct >= 90.0) else "REJECT"

    print("\n==================================================")
    print("3-TIER EVALUATION REPORT")
    print(f"  Layer 1 (Schema Validity)    : {layer1_passed}/{total_cases} ({l1_pct:.1f}%) [Threshold: 100%]")
    print(f"  Layer 2 (Invariant Integrity): {layer2_passed}/{total_cases} ({l2_pct:.1f}%) [Threshold: 100%]")
    print(f"  Layer 3 (Semantic Accuracy)  : {layer3_passed}/{total_cases} ({l3_pct:.1f}%) [Threshold: >=90%]")
    print(f"Final Decision: {verdict}")
    print("==================================================")

    evidence_dir = base_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    with open(evidence_dir / "eval-results.json", "w", encoding="utf-8") as f:
        json.dump({"summary": {"total": total_cases, "L1_pct": l1_pct, "L2_pct": l2_pct, "L3_pct": l3_pct, "decision": verdict}, "cases": results}, f, indent=2)

    final_path = base_dir / "evidence" / "final-generation" / "agent.py"
    final_path.parent.mkdir(parents=True, exist_ok=True)
    with open(base_dir / "src" / "agent.py", "r", encoding="utf-8") as src_f:
        final_path.write_text(src_f.read())

    if verdict != "ACCEPT":
        sys.exit(1)


if __name__ == "__main__":
    run_evaluation()
