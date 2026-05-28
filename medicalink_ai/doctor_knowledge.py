from __future__ import annotations

import json
import uuid
from typing import Any


def doctor_point_id(doctor_profile_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"medicalink:doctor:{doctor_profile_id}"))


def _join_lines(label: str, items: list[str] | None) -> str:
    if not items:
        return ""
    lines = [str(x).strip() for x in items if str(x).strip()]
    if not lines:
        return ""
    return f"{label}:\n" + "\n".join(f"- {x}" for x in lines)


def _specialties_text(specialties: Any) -> str:
    if not specialties:
        return ""
    names: list[str] = []
    for s in specialties:
        if isinstance(s, dict):
            n = s.get("name") or s.get("title")
            if n:
                names.append(str(n))
        elif isinstance(s, str):
            names.append(s)
    return ", ".join(names) if names else ""


def _locations_text(locations: Any) -> str:
    if not locations:
        return ""
    parts: list[str] = []
    for loc in locations:
        if not isinstance(loc, dict):
            continue
        name = loc.get("name") or loc.get("address")
        if name:
            parts.append(str(name))
    return ", ".join(parts) if parts else ""


from medicalink_ai.token_budget import TokenBudgetManager


def build_doctor_document(
    profile: dict[str, Any], 
    token_budget: TokenBudgetManager,
    max_tokens: int = 1500,
    embedding_model: str = "text-embedding-3-small",
    embedding_version: str = "v1"
) -> tuple[str, dict[str, Any]]:
    """
    Trả về (text để embed, payload metadata cho Qdrant).
    profile: DoctorProfileResponseDto-like hoặc public list item từ API.
    """
    doctor_id = str(profile.get("id") or "")
    full_name = str(profile.get("fullName") or "").strip()
    degree = str(profile.get("degree") or "").strip()
    position = profile.get("position") or []
    if isinstance(position, str):
        position = [position]
    intro = str(profile.get("introduction") or "").strip()

    specs = _specialties_text(profile.get("specialties"))
    locs = _locations_text(profile.get("workLocations"))

    text_parts = [
        f"Bác sĩ: {full_name}" if full_name else "Bác sĩ: (chưa rõ tên)",
        f"Chuyên khoa: {specs}" if specs else None,
        _join_lines("Điều kiện bệnh lý (Conditions)", profile.get("conditions")),
        _join_lines("Triệu chứng (Symptoms)", profile.get("symptoms")),
        _join_lines("Chuyên môn (Expertise)", profile.get("expertise")),
        _join_lines("Thủ thuật/Phẫu thuật (Procedures)", profile.get("procedures")),
        _join_lines("Nhóm bệnh nhân (Patient Groups)", profile.get("patientGroups")),
    ]
    text = "\n".join(p for p in text_parts if p)
    text = token_budget.token_aware_truncate(text, max_tokens)

    specialty_ids: list[str] = profile.get("specialtyIds") or []
    if not specialty_ids:
        for s in profile.get("specialties") or []:
            if isinstance(s, dict) and s.get("id") is not None:
                specialty_ids.append(str(s["id"]))

    location_ids: list[str] = []
    for loc in profile.get("workLocations") or []:
        if isinstance(loc, dict) and loc.get("id") is not None:
            location_ids.append(str(loc["id"]))

    payload: dict[str, Any] = {
        "doctor_id": doctor_id,
        "staff_account_id": str(profile.get("staffAccountId") or ""),
        "full_name": full_name,
        "is_active": bool(profile.get("isActive", True)),
        "specialty_ids": specialty_ids,
        "specialties_label": specs,
        "location_ids": location_ids,
        "introduction_text": intro,
        "experience_years": profile.get("experienceYears"),
        "education": profile.get("education") or [],
        "procedures": profile.get("procedures") or [],
        "source_json": json.dumps(profile, ensure_ascii=False, default=str)[:8000],
        "embedding_model": embedding_model,
        "embedding_version": embedding_version,
    }
    return text, payload

