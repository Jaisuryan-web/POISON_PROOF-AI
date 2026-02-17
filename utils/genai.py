#!/usr/bin/env python3
"""
GenAI utilities for explaining technical concepts and processes in plain language.
Supports OpenAI by default; can be extended to other providers.
"""
from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Optional

try:
    import openai
except Exception:
    openai = None  # type: ignore

# Default prompts for different topics
DEFAULT_PROMPTS = {
    "hashing": (
        "Explain what hashing is and why it's used for verifying file integrity. "
        "Use simple terms and an analogy a non-technical person can understand."
    ),
    "anomaly_detection": (
        "Explain how anomaly detection works in this project. Describe methods like "
        "robust z-scores (MAD), IQR fences, and what outliers mean in plain language."
    ),
    "image_forensics": (
        "Explain image forensics techniques used here: Error Level Analysis (ELA), "
        "blur detection, and dynamic range. Use simple terms and examples."
    ),
    "process_overview": (
        "Explain the end-to-end process of this PoisonProof-AI project: "
        "uploading a file, detecting anomalies, cleaning data, and training models. "
        "Describe each step in plain language for a non-technical audience."
    ),
    "security": (
        "Explain the security features in this project: audit logging, file hashing, "
        "session tracking, and why they matter for data integrity."
    ),
}

def _build_prompt(topic: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Build a prompt for the LLM based on topic and optional context.
    """
    base = DEFAULT_PROMPTS.get(topic, f"Explain the topic: {topic}")
    if context:
        ctx = json.dumps(context, indent=2, ensure_ascii=False)
        base = f"{base}\n\nContext to incorporate:\n{ctx}"
    return base

def _call_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Call OpenAI API and return the completion text.
    """
    if not openai:
        raise RuntimeError("OpenAI library not installed. Install with: pip install openai")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful explainer for non-technical audiences. Use simple language, analogies, and avoid jargon."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")

def explain_topic(topic: str, context: Optional[Dict[str, Any]] = None, provider: str = "openai") -> str:
    """
    Explain a technical topic in plain language using GenAI.
    Args:
        topic: one of the predefined keys or a custom topic string.
        context: optional JSON-serializable context to incorporate (e.g., scan results).
        provider: which LLM provider to use (currently only 'openai').
    Returns:
        Plain-language explanation string.
    """
    prompt = _build_prompt(topic, context)
    if provider == "openai":
        return _call_openai(prompt)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def explain_scan_results(anomalies: List[Dict[str, Any]]) -> str:
    """
    Given a list of anomalies, produce a plain-language summary of what was found and what it means.
    """
    # Simplify anomalies for the prompt
    simplified = []
    for a in anomalies[:10]:  # limit to avoid token limits
        simplified.append({
            "type": a.get("type"),
            "location": a.get("location"),
            "severity": a.get("severity"),
            "description": a.get("description"),
        })
    context = {
        "total_anomalies": len(anomalies),
        "sample_anomalies": simplified,
    }
    return explain_topic("anomaly_detection", context=context)

# Example usage:
#   explanation = explain_topic("hashing")
#   summary = explain_scan_results(anomalies_list)
