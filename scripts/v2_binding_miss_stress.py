import csv
import json
import random

from recover_paper48 import DOCS, PAPER, evaluate, make_cases


MISS_RATES = [0.0, 0.02, 0.05, 0.10, 0.20]
SAFE_MOTION_ACTIONS = {"move_to_target", "accept_handover", "follow_path", "align_and_place"}


def stress(rows, miss_rate, seed=48):
    rng = random.Random(seed)
    out = []
    for row in rows:
        stressed = dict(row)
        stressed["v2_prediction"] = stressed["embodied_prompt_graph_prediction"]
        stressed["v2_clarify"] = int(stressed["embodied_prompt_graph_clarify"])
        stressed["binding_missed"] = 0
        if int(stressed["safety_critical"]) and rng.random() < miss_rate:
            stressed["v2_prediction"] = stressed["text_only_prediction"]
            stressed["v2_clarify"] = int(stressed["text_only_clarify"])
            stressed["binding_missed"] = 1
        out.append(stressed)
    return out


def summarize(rows, base_metrics):
    safety_cases = [row for row in rows if int(row["safety_critical"]) == 1]
    out = []
    for miss_rate in MISS_RATES:
        stressed = stress(rows, miss_rate)
        correct = sum(1 for row in stressed if row["v2_prediction"] == row["true_action"])
        clarifications = sum(1 for row in stressed if int(row["v2_clarify"]) == 1)
        stressed_safety = [row for row in stressed if int(row["safety_critical"]) == 1]
        unsafe = sum(1 for row in stressed_safety if row["v2_prediction"] in SAFE_MOTION_ACTIONS)
        out.append(
            {
                "binding_miss_rate": miss_rate,
                "task_accuracy": correct / len(stressed),
                "clarification_rate": clarifications / len(stressed),
                "unsafe_prompt_rate": unsafe / len(stressed_safety),
                "unsafe_cases": unsafe,
                "safety_cases": len(safety_cases),
                "captioned_cues_unsafe_rate": base_metrics["methods"]["captioned_cues"]["unsafe_rate"],
            }
        )
    return out


def write_outputs(rows):
    DOCS.mkdir(exist_ok=True)
    with (DOCS / "v2_binding_miss_stress.json").open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)
    with (DOCS / "v2_binding_miss_stress.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "binding_miss_rate",
            "task_accuracy",
            "clarification_rate",
            "unsafe_prompt_rate",
            "unsafe_cases",
            "safety_cases",
            "captioned_cues_unsafe_rate",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    table = (
        "\\begin{tabular}{lrrrr}\n"
        "\\toprule\n"
        "Binding miss & Accuracy & Clarification & Unsafe rate & Unsafe cases \\\\\n"
        "\\midrule\n"
        + "\n".join(
            f"{row['binding_miss_rate']:.2f} & "
            f"{row['task_accuracy']:.3f} & "
            f"{row['clarification_rate']:.3f} & "
            f"{row['unsafe_prompt_rate']:.3f} & "
            f"{row['unsafe_cases']}/{row['safety_cases']} \\\\"
            for row in rows
        )
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
    )
    (PAPER / "v2_binding_miss_table.tex").write_text(table, encoding="utf-8")


def main():
    enriched, base_metrics = evaluate(make_cases())
    rows = summarize(enriched, base_metrics)
    write_outputs(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
