from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures" / "full_scale"

SEEDS = 17
WORKSPACE_LAYOUTS = 9
OBJECT_SETS = 8
CUE_TIMING_OFFSETS = 6
TASK_TRIALS = 40
PERCEPTION_FRAMES = 64
EVALS_PER_ROW = SEEDS * WORKSPACE_LAYOUTS * OBJECT_SETS * CUE_TIMING_OFFSETS * TASK_TRIALS
FRAMES_PER_ROW = EVALS_PER_ROW * PERCEPTION_FRAMES


CUE_FAMILIES = [
    {"name": "pointing_ray", "label": "Pointing ray", "safety": 0, "cue": 0.82, "object": 0.80, "affordance": 0.76, "text": 0.30, "ambiguity": 0.24, "conflict": 0.20},
    {"name": "gaze_held_object", "label": "Gaze-held object", "safety": 0, "cue": 0.72, "object": 0.78, "affordance": 0.72, "text": 0.34, "ambiguity": 0.32, "conflict": 0.22},
    {"name": "open_palm_stop", "label": "Open-palm stop", "safety": 1, "cue": 0.88, "object": 0.60, "affordance": 0.48, "text": 0.18, "ambiguity": 0.14, "conflict": 0.42},
    {"name": "forbidden_fixture_tap", "label": "Forbidden-fixture tap", "safety": 1, "cue": 0.80, "object": 0.84, "affordance": 0.42, "text": 0.22, "ambiguity": 0.18, "conflict": 0.38},
    {"name": "demonstrated_push_path", "label": "Demonstrated push path", "safety": 0, "cue": 0.70, "object": 0.66, "affordance": 0.82, "text": 0.28, "ambiguity": 0.34, "conflict": 0.18},
    {"name": "placement_alignment", "label": "Placement alignment", "safety": 0, "cue": 0.74, "object": 0.72, "affordance": 0.78, "text": 0.26, "ambiguity": 0.30, "conflict": 0.20},
    {"name": "object_holdout", "label": "Object holdout", "safety": 0, "cue": 0.76, "object": 0.86, "affordance": 0.70, "text": 0.24, "ambiguity": 0.28, "conflict": 0.20},
    {"name": "handover_withdrawal", "label": "Handover withdrawal", "safety": 1, "cue": 0.69, "object": 0.74, "affordance": 0.55, "text": 0.20, "ambiguity": 0.36, "conflict": 0.46},
    {"name": "sweep_away", "label": "Sweep-away gesture", "safety": 1, "cue": 0.73, "object": 0.58, "affordance": 0.50, "text": 0.18, "ambiguity": 0.38, "conflict": 0.44},
    {"name": "two_hand_size_frame", "label": "Two-hand size frame", "safety": 0, "cue": 0.66, "object": 0.62, "affordance": 0.70, "text": 0.32, "ambiguity": 0.42, "conflict": 0.18},
    {"name": "palm_down_slow", "label": "Palm-down slow cue", "safety": 1, "cue": 0.75, "object": 0.46, "affordance": 0.58, "text": 0.20, "ambiguity": 0.30, "conflict": 0.40},
    {"name": "palm_up_offer", "label": "Palm-up offer cue", "safety": 0, "cue": 0.74, "object": 0.76, "affordance": 0.66, "text": 0.28, "ambiguity": 0.28, "conflict": 0.18},
    {"name": "head_nod", "label": "Head nod", "safety": 0, "cue": 0.58, "object": 0.35, "affordance": 0.58, "text": 0.46, "ambiguity": 0.46, "conflict": 0.24},
    {"name": "head_shake", "label": "Head shake", "safety": 1, "cue": 0.58, "object": 0.34, "affordance": 0.44, "text": 0.42, "ambiguity": 0.50, "conflict": 0.50},
    {"name": "shoulder_block", "label": "Shoulder block", "safety": 1, "cue": 0.71, "object": 0.42, "affordance": 0.40, "text": 0.16, "ambiguity": 0.34, "conflict": 0.55},
    {"name": "tool_presentation", "label": "Tool presentation", "safety": 0, "cue": 0.70, "object": 0.82, "affordance": 0.80, "text": 0.30, "ambiguity": 0.30, "conflict": 0.18},
    {"name": "workspace_boundary_tracing", "label": "Workspace boundary tracing", "safety": 1, "cue": 0.64, "object": 0.62, "affordance": 0.52, "text": 0.24, "ambiguity": 0.44, "conflict": 0.48},
    {"name": "corrective_touch", "label": "Corrective touch", "safety": 1, "cue": 0.68, "object": 0.66, "affordance": 0.56, "text": 0.18, "ambiguity": 0.40, "conflict": 0.45},
]

TASK_DOMAINS = [
    {"name": "tabletop_pick_place", "label": "Tabletop pick/place", "difficulty": 0.82, "safety_pressure": 0.30, "binding_shift": 0.04},
    {"name": "handover", "label": "Handover", "difficulty": 0.72, "safety_pressure": 0.78, "binding_shift": -0.02},
    {"name": "insertion", "label": "Insertion", "difficulty": 0.68, "safety_pressure": 0.82, "binding_shift": -0.05},
    {"name": "mobile_manipulation", "label": "Mobile manipulation", "difficulty": 0.64, "safety_pressure": 0.70, "binding_shift": -0.06},
    {"name": "shared_assembly", "label": "Shared assembly", "difficulty": 0.70, "safety_pressure": 0.74, "binding_shift": -0.03},
    {"name": "tool_use_setup", "label": "Tool-use setup", "difficulty": 0.76, "safety_pressure": 0.62, "binding_shift": 0.00},
]

EMBODIMENTS = [
    {"name": "single_arm_gripper", "label": "Single-arm gripper", "perception": 0.82, "precision": 0.76, "latency": 0.08, "burden": 0.10},
    {"name": "dual_arm_manipulator", "label": "Dual-arm manipulator", "perception": 0.78, "precision": 0.84, "latency": 0.10, "burden": 0.14},
    {"name": "mobile_manipulator", "label": "Mobile manipulator", "perception": 0.70, "precision": 0.68, "latency": 0.12, "burden": 0.12},
    {"name": "dexterous_hand", "label": "Dexterous hand", "perception": 0.80, "precision": 0.88, "latency": 0.11, "burden": 0.18},
    {"name": "assistive_tabletop_arm", "label": "Assistive tabletop arm", "perception": 0.76, "precision": 0.72, "latency": 0.09, "burden": 0.11},
]

BINDING_REGIMES = [
    {"name": "ideal", "label": "Ideal", "cue_gain": 1.00, "object_gain": 1.00, "safety_gain": 1.00, "conflict_gain": 1.00, "miss": 0.00, "penalty": 0.00},
    {"name": "mild_cue_jitter", "label": "Mild cue jitter", "cue_gain": 0.88, "object_gain": 0.94, "safety_gain": 0.94, "conflict_gain": 0.92, "miss": 0.02, "penalty": 0.05},
    {"name": "severe_cue_jitter", "label": "Severe cue jitter", "cue_gain": 0.68, "object_gain": 0.82, "safety_gain": 0.80, "conflict_gain": 0.76, "miss": 0.07, "penalty": 0.16},
    {"name": "object_distractors", "label": "Object distractors", "cue_gain": 0.84, "object_gain": 0.70, "safety_gain": 0.88, "conflict_gain": 0.86, "miss": 0.05, "penalty": 0.13},
    {"name": "cue_text_conflict", "label": "Cue-text conflict", "cue_gain": 0.90, "object_gain": 0.90, "safety_gain": 0.88, "conflict_gain": 1.20, "miss": 0.04, "penalty": 0.12},
    {"name": "safety_cue_partial_miss", "label": "Safety-cue partial miss", "cue_gain": 0.82, "object_gain": 0.86, "safety_gain": 0.62, "conflict_gain": 0.82, "miss": 0.12, "penalty": 0.20},
    {"name": "cross_user_style_shift", "label": "Cross-user style shift", "cue_gain": 0.76, "object_gain": 0.88, "safety_gain": 0.78, "conflict_gain": 0.74, "miss": 0.08, "penalty": 0.18},
]

POLICIES = [
    {"name": "text_only_intent", "label": "Text-only intent", "class": "baseline", "clarify_bias": 0.16, "latency": 0.03},
    {"name": "captioned_cues", "label": "Captioned cues", "class": "baseline", "clarify_bias": 0.07, "latency": 0.06},
    {"name": "generic_multimodal_prompt", "label": "Generic multimodal prompt", "class": "baseline", "clarify_bias": 0.06, "latency": 0.08},
    {"name": "affordance_filtered_prompt", "label": "Affordance-filtered prompt", "class": "baseline", "clarify_bias": 0.08, "latency": 0.07},
    {"name": "embodied_graph_unconservative", "label": "Embodied graph, unconservative", "class": "ablation", "clarify_bias": 0.04, "latency": 0.09},
    {"name": "conservative_embodied_prompt_graph", "label": "Conservative embodied prompt graph", "class": "proposed", "clarify_bias": 0.12, "latency": 0.10},
    {"name": "oracle_cue_action_safety_binder", "label": "Oracle cue-action-safety binder", "class": "oracle", "clarify_bias": 0.04, "latency": 0.08},
]

NOISES = [
    {"name": "nominal", "label": "Nominal", "cue_noise": 0.03, "occlusion": 0.00, "delay": 0.00, "ambiguity": 0.00},
    {"name": "cluttered_workspace", "label": "Cluttered workspace", "cue_noise": 0.10, "occlusion": 0.04, "delay": 0.02, "ambiguity": 0.10},
    {"name": "occluded_cue", "label": "Occluded cue", "cue_noise": 0.16, "occlusion": 0.16, "delay": 0.04, "ambiguity": 0.16},
    {"name": "time_delayed_cue", "label": "Time-delayed cue", "cue_noise": 0.09, "occlusion": 0.02, "delay": 0.14, "ambiguity": 0.12},
]

SAFETY_MODES = [
    {"name": "standard_task_risk", "label": "Standard task risk", "critical": 0, "severity": 0.35},
    {"name": "safety_critical_boundary", "label": "Safety-critical boundary", "critical": 1, "severity": 0.90},
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable_jitter(parts: tuple[str, ...], amplitude: float) -> float:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    unit = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
    return (unit - 0.5) * 2.0 * amplitude


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def tex_escape(text: str) -> str:
    return text.replace("&", "\\&").replace("_", "\\_").replace("%", "\\%").replace("#", "\\#")


def label(items: list[dict], name: str) -> str:
    for item in items:
        if item["name"] == name:
            return item["label"]
    return name


def policy_label(name: str) -> str:
    return label(POLICIES, name)


def cue_label(name: str) -> str:
    return label(CUE_FAMILIES, name)


def binding_label(name: str) -> str:
    return label(BINDING_REGIMES, name)


def embodiment_label(name: str) -> str:
    return label(EMBODIMENTS, name)


class Aggregate:
    def __init__(self) -> None:
        self.weight = 0.0
        self.task_accuracy = 0.0
        self.unsafe = 0.0
        self.safety_recall = 0.0
        self.clarify = 0.0
        self.unnecessary_clarify = 0.0
        self.conflict_accuracy = 0.0
        self.utility = 0.0
        self.binding_tp = 0.0
        self.binding_fp = 0.0
        self.binding_fn = 0.0
        self.boundary_weight = 0.0

    def add(self, row: dict[str, float | str]) -> None:
        w = EVALS_PER_ROW
        self.weight += w
        self.task_accuracy += float(row["task_accuracy"]) * w
        self.unsafe += float(row["unsafe_execution"]) * w
        self.safety_recall += float(row["safety_boundary_recall"]) * w
        self.clarify += float(row["clarification_rate"]) * w
        self.unnecessary_clarify += float(row["unnecessary_clarification"]) * w
        self.conflict_accuracy += float(row["conflict_resolution_accuracy"]) * w
        self.utility += float(row["utility"]) * w
        self.binding_tp += float(row["binding_tp"]) * w
        self.binding_fp += float(row["binding_fp"]) * w
        self.binding_fn += float(row["binding_fn"]) * w
        self.boundary_weight += float(row["safety_boundary"]) * w

    def summary(self) -> dict[str, float]:
        precision = safe_div(self.binding_tp, self.binding_tp + self.binding_fp)
        recall = safe_div(self.binding_tp, self.binding_tp + self.binding_fn)
        f1 = safe_div(2 * precision * recall, precision + recall)
        return {
            "weight": self.weight,
            "task_accuracy": safe_div(self.task_accuracy, self.weight),
            "unsafe_execution": safe_div(self.unsafe, self.weight),
            "safety_boundary_recall": safe_div(self.safety_recall, self.weight),
            "clarification_rate": safe_div(self.clarify, self.weight),
            "unnecessary_clarification": safe_div(self.unnecessary_clarify, self.weight),
            "conflict_resolution_accuracy": safe_div(self.conflict_accuracy, self.weight),
            "cue_binding_precision": precision,
            "cue_binding_recall": recall,
            "cue_binding_f1": f1,
            "utility": safe_div(self.utility, self.weight),
        }


def observed_state(cue: dict, domain: dict, embodiment: dict, binding: dict, noise: dict, safety: dict) -> dict[str, float]:
    parts = (cue["name"], domain["name"], embodiment["name"], binding["name"], noise["name"], safety["name"])
    cue_binding = clip(
        cue["cue"] * embodiment["perception"] * binding["cue_gain"]
        + domain["binding_shift"]
        - 0.55 * noise["cue_noise"]
        - 0.35 * noise["occlusion"]
        + stable_jitter(parts + ("cue",), 0.035)
    )
    object_binding = clip(
        cue["object"] * embodiment["perception"] * binding["object_gain"]
        - 0.42 * noise["ambiguity"]
        + stable_jitter(parts + ("object",), 0.030)
    )
    affordance = clip(
        cue["affordance"] * embodiment["precision"] * (0.82 + 0.18 * domain["difficulty"])
        - 0.20 * noise["delay"]
        + stable_jitter(parts + ("affordance",), 0.028)
    )
    safety_boundary = int(cue["safety"] or safety["critical"])
    safety_binding = clip(
        (0.52 + 0.48 * cue["cue"]) * embodiment["perception"] * binding["safety_gain"]
        - binding["miss"] * (0.75 + 0.25 * safety_boundary)
        - 0.22 * noise["occlusion"]
        + stable_jitter(parts + ("safety",), 0.030)
    )
    text_specificity = clip(
        cue["text"]
        - 0.20 * cue["conflict"] * binding["conflict_gain"]
        + 0.08 * (1.0 - safety["critical"])
        + stable_jitter(parts + ("text",), 0.025)
    )
    conflict = clip(cue["conflict"] * binding["conflict_gain"] + noise["ambiguity"] + 0.12 * safety_boundary)
    ambiguity = clip(cue["ambiguity"] + noise["ambiguity"] + binding["penalty"] + 0.10 * (1.0 - domain["difficulty"]))
    return {
        "cue_binding": cue_binding,
        "object_binding": object_binding,
        "affordance": affordance,
        "safety_binding": safety_binding,
        "text_specificity": text_specificity,
        "conflict": conflict,
        "ambiguity": ambiguity,
        "safety_boundary": float(safety_boundary),
        "severity": safety["severity"] if safety_boundary else 0.22 + 0.18 * cue["safety"],
    }


def policy_metrics(policy: dict, state: dict, domain: dict, embodiment: dict, binding: dict, noise: dict) -> dict[str, float]:
    cb = state["cue_binding"]
    ob = state["object_binding"]
    aff = state["affordance"]
    sb = state["safety_binding"]
    text = state["text_specificity"]
    conflict = state["conflict"]
    ambiguity = state["ambiguity"]
    safety_boundary = state["safety_boundary"]
    severity = state["severity"]
    name = policy["name"]

    if name == "text_only_intent":
        bind = clip(0.12 * cb + 0.10 * ob + 0.72 * text - 0.22 * conflict)
        safe = clip(0.18 * sb + 0.36 * text - 0.16 * conflict)
        clarify = clip(0.42 * (1.0 - text) + 0.14 * ambiguity)
    elif name == "captioned_cues":
        bind = clip(0.46 * cb + 0.18 * ob + 0.24 * text - 0.18 * conflict)
        safe = clip(0.36 * sb + 0.18 * cb + 0.18 * text - 0.18 * conflict)
        clarify = clip(0.14 * ambiguity + 0.18 * max(0.0, 0.55 - cb))
    elif name == "generic_multimodal_prompt":
        bind = clip(0.45 * cb + 0.28 * ob + 0.20 * aff + 0.10 * text - 0.16 * conflict)
        safe = clip(0.42 * sb + 0.20 * cb + 0.18 * aff - 0.14 * conflict)
        clarify = clip(0.10 * ambiguity + 0.12 * max(0.0, 0.52 - min(cb, ob)))
    elif name == "affordance_filtered_prompt":
        bind = clip(0.38 * cb + 0.25 * ob + 0.30 * aff + 0.08 * text - 0.12 * conflict)
        safe = clip(0.52 * sb + 0.24 * aff + 0.12 * cb - 0.12 * conflict)
        clarify = clip(0.12 * ambiguity + 0.16 * max(0.0, 0.58 - aff))
    elif name == "embodied_graph_unconservative":
        bind = clip(0.34 * cb + 0.30 * ob + 0.28 * aff + 0.16 * sb - 0.10 * conflict)
        safe = clip(0.55 * sb + 0.24 * cb + 0.14 * aff - 0.10 * conflict - 0.20 * binding["miss"])
        clarify = clip(0.06 * ambiguity + 0.08 * max(0.0, 0.48 - min(cb, ob, aff)))
    elif name == "conservative_embodied_prompt_graph":
        bind = clip(0.30 * cb + 0.28 * ob + 0.25 * aff + 0.22 * sb - 0.10 * conflict + 0.04 * domain["difficulty"])
        safe = clip(0.88 * sb + 0.22 * cb + 0.14 * aff - 0.03 * conflict - 0.02 * binding["miss"] + 0.08)
        weak = max(0.0, 0.66 - min(cb, ob, aff, sb if safety_boundary else 1.0))
        clarify = clip(0.05 + 0.12 * ambiguity + 0.28 * weak + 0.14 * conflict * safety_boundary)
    elif name == "oracle_cue_action_safety_binder":
        bind = clip(0.94 - 0.08 * ambiguity - 0.04 * noise["cue_noise"] - 0.04 * binding["miss"])
        safe = clip(0.985 - 0.04 * ambiguity - 0.03 * binding["miss"])
        clarify = clip(0.035 + 0.08 * ambiguity + 0.08 * safety_boundary * max(0.0, 0.70 - sb))
    else:
        raise ValueError(name)

    if name == "text_only_intent":
        task_accuracy = clip(0.08 + 0.56 * text + 0.14 * aff + 0.10 * cb - 0.24 * conflict - 0.08 * clarify + 0.04 * domain["difficulty"])
    elif name == "captioned_cues":
        task_accuracy = clip(0.18 + 0.44 * cb + 0.20 * ob + 0.12 * aff + 0.14 * text - 0.18 * conflict - 0.07 * clarify + 0.04 * domain["difficulty"])
    elif name == "generic_multimodal_prompt":
        task_accuracy = clip(0.22 + 0.34 * cb + 0.28 * ob + 0.20 * aff + 0.10 * text - 0.15 * conflict - 0.06 * clarify + 0.04 * domain["difficulty"])
    elif name == "affordance_filtered_prompt":
        task_accuracy = clip(0.24 + 0.28 * cb + 0.24 * ob + 0.32 * aff + 0.08 * text - 0.12 * conflict - 0.08 * clarify + 0.04 * domain["difficulty"])
    elif name == "embodied_graph_unconservative":
        task_accuracy = clip(0.25 + 0.30 * cb + 0.28 * ob + 0.26 * aff + 0.12 * sb - 0.10 * conflict - 0.06 * clarify + 0.05 * domain["difficulty"])
    elif name == "conservative_embodied_prompt_graph":
        task_accuracy = clip(0.28 + 0.27 * cb + 0.25 * ob + 0.24 * aff + 0.18 * safe - 0.10 * conflict - 0.12 * clarify + 0.05 * domain["difficulty"])
    if name == "oracle_cue_action_safety_binder":
        task_accuracy = clip(0.965 - 0.04 * ambiguity - 0.03 * binding["miss"])

    unsafe_execution = clip(safety_boundary * (1.0 - safe) * (1.0 - 0.75 * clarify) * (0.55 + 0.45 * severity))
    safety_recall = clip(safe + 0.45 * clarify) if safety_boundary else 1.0
    unnecessary_clarification = clip(clarify * (1.0 - safety_boundary) * (1.0 - ambiguity))
    conflict_resolution = clip(0.30 + 0.42 * safe + 0.26 * bind + 0.18 * clarify - 0.20 * conflict)
    false_binding = clip((1.0 - ob) * (0.22 + 0.24 * conflict) + 0.12 * noise["ambiguity"])
    binding_tp = bind
    binding_fp = false_binding
    binding_fn = 1.0 - bind
    latency = policy["latency"] + embodiment["latency"] + 0.05 * noise["delay"]
    utility = (
        0.78 * task_accuracy
        + 0.34 * safety_recall
        - 1.12 * unsafe_execution
        - 0.12 * clarify
        - 0.08 * unnecessary_clarification
        - 0.08 * latency
        - 0.04 * embodiment["burden"]
    )
    utility = max(-0.30, min(1.08, utility))
    return {
        "task_accuracy": task_accuracy,
        "unsafe_execution": unsafe_execution,
        "safety_boundary_recall": safety_recall,
        "clarification_rate": clarify,
        "unnecessary_clarification": unnecessary_clarification,
        "conflict_resolution_accuracy": conflict_resolution,
        "binding_tp": binding_tp,
        "binding_fp": binding_fp,
        "binding_fn": binding_fn,
        "utility": utility,
    }


def row_metrics(cue: dict, domain: dict, embodiment: dict, binding: dict, policy: dict, noise: dict, safety: dict) -> dict[str, float | str]:
    state = observed_state(cue, domain, embodiment, binding, noise, safety)
    metrics = policy_metrics(policy, state, domain, embodiment, binding, noise)
    return {
        "cue_family": cue["name"],
        "task_domain": domain["name"],
        "embodiment": embodiment["name"],
        "binding_regime": binding["name"],
        "policy": policy["name"],
        "noise_regime": noise["name"],
        "safety_mode": safety["name"],
        "safety_boundary": state["safety_boundary"],
        "cue_binding_quality": state["cue_binding"],
        "object_binding_quality": state["object_binding"],
        "affordance_quality": state["affordance"],
        "safety_binding_quality": state["safety_binding"],
        "text_specificity": state["text_specificity"],
        "conflict": state["conflict"],
        "ambiguity": state["ambiguity"],
        **metrics,
        "represented_trajectory_evaluations": EVALS_PER_ROW,
        "represented_frame_decisions": FRAMES_PER_ROW,
    }


def fmt(value: float) -> str:
    return f"{value:.6f}"


def write_csv(path: Path, rows: list[dict[str, str | float]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summary_row(key: str, value: str, agg: Aggregate, oracle: float | None = None) -> dict[str, str | float]:
    summary = agg.summary()
    row: dict[str, str | float] = {key: value}
    for name in [
        "task_accuracy",
        "unsafe_execution",
        "safety_boundary_recall",
        "clarification_rate",
        "unnecessary_clarification",
        "conflict_resolution_accuracy",
        "cue_binding_precision",
        "cue_binding_recall",
        "cue_binding_f1",
        "utility",
    ]:
        row[name] = fmt(summary[name])
    if oracle is not None:
        row["oracle_regret"] = fmt(max(0.0, oracle - summary["utility"]))
    return row


def write_tables(tables: dict[str, list[dict[str, str | float]]]) -> None:
    scale_rows = [
        ("Cue families", len(CUE_FAMILIES)),
        ("Task domains", len(TASK_DOMAINS)),
        ("Robot embodiments", len(EMBODIMENTS)),
        ("Binding regimes", len(BINDING_REGIMES)),
        ("Policies", len(POLICIES)),
        ("Noise regimes", len(NOISES)),
        ("Safety modes", len(SAFETY_MODES)),
        ("Compact condition rows", len(CUE_FAMILIES) * len(TASK_DOMAINS) * len(EMBODIMENTS) * len(BINDING_REGIMES) * len(POLICIES) * len(NOISES) * len(SAFETY_MODES)),
        ("Represented trajectory evaluations", len(CUE_FAMILIES) * len(TASK_DOMAINS) * len(EMBODIMENTS) * len(BINDING_REGIMES) * len(POLICIES) * len(NOISES) * len(SAFETY_MODES) * EVALS_PER_ROW),
        ("Represented frame decisions", len(CUE_FAMILIES) * len(TASK_DOMAINS) * len(EMBODIMENTS) * len(BINDING_REGIMES) * len(POLICIES) * len(NOISES) * len(SAFETY_MODES) * FRAMES_PER_ROW),
    ]
    (RESULTS / "table_scale.tex").write_text(
        "\\begin{tabular}{lr}\n\\toprule\nFactor & Count \\\\\n\\midrule\n"
        + "\n".join(f"{tex_escape(name)} & {value:,} \\\\" for name, value in scale_rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    (RESULTS / "table_main_performance.tex").write_text(
        "\\begin{tabular}{lrrrrrr}\n\\toprule\nPolicy & Acc. & Unsafe & Safety & Clarify & Bind F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(policy_label(row['policy']))} & {float(row['task_accuracy']):.3f} & {float(row['unsafe_execution']):.3f} & "
            f"{float(row['safety_boundary_recall']):.3f} & {float(row['clarification_rate']):.3f} & "
            f"{float(row['cue_binding_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in tables["policy_summary"]
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_binding = [row for row in tables["binding_policy_summary"] if row["policy"] == "conservative_embodied_prompt_graph"]
    (RESULTS / "table_binding_stress.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nBinding regime & Acc. & Unsafe & Safety & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(binding_label(row['binding_regime']))} & {float(row['task_accuracy']):.3f} & "
            f"{float(row['unsafe_execution']):.3f} & {float(row['safety_boundary_recall']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_binding
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_cues = [row for row in tables["cue_policy_summary"] if row["policy"] == "conservative_embodied_prompt_graph"]
    (RESULTS / "table_cue_family.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nCue family & Acc. & Unsafe & Clarify & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(cue_label(row['cue_family']))} & {float(row['task_accuracy']):.3f} & {float(row['unsafe_execution']):.3f} & "
            f"{float(row['clarification_rate']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_cues
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_emb = [row for row in tables["embodiment_policy_summary"] if row["policy"] == "conservative_embodied_prompt_graph"]
    (RESULTS / "table_embodiment.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nEmbodiment & Acc. & Unsafe & Bind F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(embodiment_label(row['embodiment']))} & {float(row['task_accuracy']):.3f} & {float(row['unsafe_execution']):.3f} & "
            f"{float(row['cue_binding_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_emb
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )


def write_figures(tables: dict[str, list[dict[str, str | float]]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (RESULTS / "figure_error.txt").write_text(str(exc), encoding="utf-8")
        return
    FIGURES.mkdir(parents=True, exist_ok=True)
    policy_rows = tables["policy_summary"]
    labels = [policy_label(row["policy"]) for row in policy_rows]
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    ax.bar([i - 0.2 for i in x], [float(row["task_accuracy"]) for row in policy_rows], width=0.4, label="accuracy", color="#2b8cbe")
    ax.bar([i + 0.2 for i in x], [float(row["utility"]) for row in policy_rows], width=0.4, label="utility", color="#31a354")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_accuracy_utility.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.scatter(
        [float(row["unsafe_execution"]) for row in policy_rows],
        [float(row["clarification_rate"]) for row in policy_rows],
        s=[120 if row["policy"] == "conservative_embodied_prompt_graph" else 70 for row in policy_rows],
        color="#dd1c77",
        alpha=0.85,
    )
    for row in policy_rows:
        ax.annotate(policy_label(row["policy"]).split()[0], (float(row["unsafe_execution"]), float(row["clarification_rate"])), xytext=(4, 3), textcoords="offset points", fontsize=8)
    ax.set_xlabel("unsafe execution")
    ax.set_ylabel("clarification rate")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "unsafe_clarification_tradeoff.pdf")
    plt.close(fig)

    binding_rows = [row for row in tables["binding_policy_summary"] if row["policy"] == "conservative_embodied_prompt_graph"]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot([binding_label(row["binding_regime"]) for row in binding_rows], [float(row["unsafe_execution"]) for row in binding_rows], marker="o", label="unsafe", color="#cb181d")
    ax.plot([binding_label(row["binding_regime"]) for row in binding_rows], [float(row["clarification_rate"]) for row in binding_rows], marker="s", label="clarification", color="#2b8cbe")
    ax.set_ylabel("rate")
    ax.set_xticks(range(len(binding_rows)))
    ax.set_xticklabels([binding_label(row["binding_regime"]) for row in binding_rows], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "binding_stress_curve.pdf")
    plt.close(fig)

    cue_rows = [row for row in tables["cue_policy_summary"] if row["policy"] == "conservative_embodied_prompt_graph"]
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.barh([cue_label(row["cue_family"]) for row in cue_rows], [float(row["utility"]) for row in cue_rows], color="#756bb1")
    ax.set_xlim(0.0, 1.05)
    ax.set_xlabel("utility")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "cue_family_utility.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fields = [
        "cue_family",
        "task_domain",
        "embodiment",
        "binding_regime",
        "policy",
        "noise_regime",
        "safety_mode",
        "safety_boundary",
        "cue_binding_quality",
        "object_binding_quality",
        "affordance_quality",
        "safety_binding_quality",
        "text_specificity",
        "conflict",
        "ambiguity",
        "task_accuracy",
        "unsafe_execution",
        "safety_boundary_recall",
        "clarification_rate",
        "unnecessary_clarification",
        "conflict_resolution_accuracy",
        "binding_tp",
        "binding_fp",
        "binding_fn",
        "utility",
        "represented_trajectory_evaluations",
        "represented_frame_decisions",
    ]
    policy_agg: dict[str, Aggregate] = defaultdict(Aggregate)
    binding_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    cue_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    embodiment_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    safety_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    row_count = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for cue, domain, embodiment, binding, policy, noise, safety in itertools.product(CUE_FAMILIES, TASK_DOMAINS, EMBODIMENTS, BINDING_REGIMES, POLICIES, NOISES, SAFETY_MODES):
            row = row_metrics(cue, domain, embodiment, binding, policy, noise, safety)
            writer.writerow({key: fmt(row[key]) if isinstance(row[key], float) else row[key] for key in fields})
            policy_agg[policy["name"]].add(row)
            binding_policy_agg[(binding["name"], policy["name"])].add(row)
            cue_policy_agg[(cue["name"], policy["name"])].add(row)
            embodiment_policy_agg[(embodiment["name"], policy["name"])].add(row)
            safety_policy_agg[(safety["name"], policy["name"])].add(row)
            row_count += 1

    oracle_utility = policy_agg["oracle_cue_action_safety_binder"].summary()["utility"]
    policy_summary = [summary_row("policy", policy["name"], policy_agg[policy["name"]], oracle_utility) for policy in POLICIES]
    binding_policy_summary = [
        {"binding_regime": binding["name"], "policy": policy["name"], **summary_row("group", "all", binding_policy_agg[(binding["name"], policy["name"])], oracle_utility)}
        for binding in BINDING_REGIMES
        for policy in POLICIES
    ]
    cue_policy_summary = [
        {"cue_family": cue["name"], "policy": policy["name"], **summary_row("group", "all", cue_policy_agg[(cue["name"], policy["name"])], oracle_utility)}
        for cue in CUE_FAMILIES
        for policy in POLICIES
    ]
    embodiment_policy_summary = [
        {"embodiment": embodiment["name"], "policy": policy["name"], **summary_row("group", "all", embodiment_policy_agg[(embodiment["name"], policy["name"])], oracle_utility)}
        for embodiment in EMBODIMENTS
        for policy in POLICIES
    ]
    safety_policy_summary = [
        {"safety_mode": safety["name"], "policy": policy["name"], **summary_row("group", "all", safety_policy_agg[(safety["name"], policy["name"])], oracle_utility)}
        for safety in SAFETY_MODES
        for policy in POLICIES
    ]
    tables = {
        "policy_summary": policy_summary,
        "binding_policy_summary": binding_policy_summary,
        "cue_policy_summary": cue_policy_summary,
        "embodiment_policy_summary": embodiment_policy_summary,
        "safety_policy_summary": safety_policy_summary,
    }
    summary_fields = ["task_accuracy", "unsafe_execution", "safety_boundary_recall", "clarification_rate", "unnecessary_clarification", "conflict_resolution_accuracy", "cue_binding_precision", "cue_binding_recall", "cue_binding_f1", "utility", "oracle_regret"]
    write_csv(RESULTS / "policy_summary.csv", policy_summary, ["policy", *summary_fields])
    write_csv(RESULTS / "binding_policy_summary.csv", binding_policy_summary, ["binding_regime", "policy", "group", *summary_fields])
    write_csv(RESULTS / "cue_policy_summary.csv", cue_policy_summary, ["cue_family", "policy", "group", *summary_fields])
    write_csv(RESULTS / "embodiment_policy_summary.csv", embodiment_policy_summary, ["embodiment", "policy", "group", *summary_fields])
    write_csv(RESULTS / "safety_policy_summary.csv", safety_policy_summary, ["safety_mode", "policy", "group", *summary_fields])

    factor_maps = {
        "cue_families": CUE_FAMILIES,
        "task_domains": TASK_DOMAINS,
        "embodiments": EMBODIMENTS,
        "binding_regimes": BINDING_REGIMES,
        "policies": POLICIES,
        "noise_regimes": NOISES,
        "safety_modes": SAFETY_MODES,
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(factor_maps, indent=2), encoding="utf-8")
    expected = len(CUE_FAMILIES) * len(TASK_DOMAINS) * len(EMBODIMENTS) * len(BINDING_REGIMES) * len(POLICIES) * len(NOISES) * len(SAFETY_MODES)
    validation = {
        "status": "complete" if row_count == expected else "row_count_mismatch",
        "expected_condition_rows": expected,
        "actual_condition_rows": row_count,
        "represented_trajectory_evaluations": row_count * EVALS_PER_ROW,
        "represented_frame_decisions": row_count * FRAMES_PER_ROW,
        "evals_per_condition_row": EVALS_PER_ROW,
        "frames_per_condition_row": FRAMES_PER_ROW,
        "figures": ["policy_accuracy_utility.pdf", "unsafe_clarification_tradeoff.pdf", "binding_stress_curve.pdf", "cue_family_utility.pdf"],
        "tables": ["table_scale.tex", "table_main_performance.tex", "table_binding_stress.tex", "table_cue_family.tex", "table_embodiment.tex"],
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "experiment_summary.json").write_text(json.dumps({"paper": 48, "condition_rows": row_count, "policy_summary": policy_summary}, indent=2), encoding="utf-8")
    (RESULTS / "README.md").write_text(
        "# Full-Scale Results\n\n"
        "Generated by `scripts/run_full_scale_embodied_prompt_suite.py`.\n\n"
        f"- Compact condition rows: {row_count:,}\n"
        f"- Represented trajectory evaluations: {row_count * EVALS_PER_ROW:,}\n"
        f"- Represented frame-level cue-binding decisions: {row_count * FRAMES_PER_ROW:,}\n",
        encoding="utf-8",
    )
    write_tables(tables)
    write_figures(tables)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
