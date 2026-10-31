import json
import sys
from pathlib import Path

# Script ke location se base path set karein
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

from src.agent import ReminderAgent, ReminderOutput


def run_evaluation():
    dataset_path = base_dir / "evals" / "dataset.json"

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    agent = ReminderAgent()
    passed_cases = 0
    total_cases = len(dataset)
    results = []

    print("==================================================")
    print("  RUNNING NON-DETERMINISTIC EVALUATION HARNESS")
    print(f"  Target Cases: {total_cases} | Threshold: 80%")
    print("==================================================")

    for item in dataset:
        case_id = item["id"]
        inp = item["input"]
        exp_clarify = item["expected_needs_clarification"]
        exp_title = item.get("expected_title")
        exp_recurrence = item.get("expected_recurrence")

        case_passed = True
        layer_errors = []

        try:
            output: ReminderOutput = agent.parse_intent(inp)

            # Layer 1: Structural / Schema Validation
            if not isinstance(output, ReminderOutput):
                layer_errors.append("Layer 1 Failed: Schema contract broken")
                case_passed = False

            # Layer 2: Invariants / Property Validation
            if output.needs_clarification and not output.clarification_question:
                layer_errors.append(
                    "Layer 2 Failed: Clarification true hai par question null hai"
                )
                case_passed = False

            if not output.needs_clarification and not output.title:
                layer_errors.append(
                    "Layer 2 Failed: Clarification false hone par title null hai"
                )
                case_passed = False

            # Layer 3: Semantic / Quality Evaluation
            if output.needs_clarification != exp_clarify:
                layer_errors.append(
                    f"Layer 3 Failed: Clarification mismatch (got {output.needs_clarification}, expected {exp_clarify})"
                )
                case_passed = False

            if exp_title and output.title:
                if (
                    exp_title.lower() not in output.title.lower()
                    and output.title.lower() not in exp_title.lower()
                ):
                    layer_errors.append(
                        f"Layer 3 Failed: Title mismatch (got '{output.title}', expected '{exp_title}')"
                    )
                    case_passed = False

            if exp_recurrence and output.recurrence.value != exp_recurrence:
                layer_errors.append(
                    f"Layer 3 Failed: Recurrence mismatch (got {output.recurrence.value}, expected {exp_recurrence})"
                )
                case_passed = False

        except Exception as e:
            case_passed = False
            layer_errors.append(f"Execution Error: {str(e)}")

        if case_passed:
            passed_cases += 1
            status = "PASS"
        else:
            status = "FAIL"

        results.append(
            {
                "id": case_id,
                "input": inp,
                "status": status,
                "layer_errors": layer_errors,
            }
        )

        display_inp = (inp[:35] + "...") if len(inp) > 35 else inp
        print(f"[{status}] Case {case_id:02d}: \"{display_inp}\"")
        for err in layer_errors:
            print(f"       -> {err}")

    score_pct = (passed_cases / total_cases) * 100
    print("\n==================================================")
    print(
        f"EVALUATION SUMMARY: {passed_cases}/{total_cases} Passed ({score_pct:.1f}%)"
    )
    final_status = "PASS" if score_pct >= 80.0 else "FAIL"
    print(f"Final Decision: {final_status} (Threshold: 80.0%)")
    print("==================================================")

    # Save evidence file
    evidence_dir = base_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    with open(evidence_dir / "eval-results.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "total": total_cases,
                "passed": passed_cases,
                "score_percent": score_pct,
                "threshold": 80.0,
                "status": final_status,
                "cases": results,
            },
            f,
            indent=2,
        )

    # Final generation copy
    final_agent_path = base_dir / "evidence" / "final-generation" / "agent.py"
    final_agent_path.parent.mkdir(parents=True, exist_ok=True)
    with open(base_dir / "src" / "agent.py", "r", encoding="utf-8") as src_f:
        final_agent_path.write_text(src_f.read())


if __name__ == "__main__":
    run_evaluation()
