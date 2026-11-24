"""KaamConnect Matching Engine Proof of Concept.

Implements weighted multi-factor scoring (Skill 40%, Location 30%,
Availability 15%, Experience 10%, Wage 5%) using the Haversine formula.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EARTH_RADIUS_KM = 6371.0

WEIGHTS = {
    "skill": 0.40,
    "location": 0.30,
    "availability": 0.15,
    "experience": 0.10,
    "wage": 0.05,
}

AVAILABILITY_SCORES = {
    "available": 100.0,
    "busy": 40.0,
    "unavailable": 0.0,
}


@dataclass(frozen=True)
class MatchResult:
    """Represents a scored worker-job match with human-readable reasons."""

    worker_id: str
    worker_name: str
    job_id: str
    job_title: str
    total_score: float
    distance_km: float
    breakdown: dict[str, float]
    reasons: list[str]


def haversine_distance_km(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calculate great-circle distance in kilometres between two coordinates."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c


def _score_skills(
    worker_skills: list[str], required_skills: list[str]
) -> tuple[float, str]:
    req = {s.strip().lower() for s in required_skills if s.strip()}
    wrk = {s.strip().lower() for s in worker_skills if s.strip()}
    if not req:
        return 100.0, "No specific skills required"
    matched = sorted(req & wrk)
    score = (len(matched) / len(req)) * 100.0
    if matched:
        reason = f"Matched {len(matched)}/{len(req)} required skills: {', '.join(matched)}"
    else:
        reason = f"Matched 0/{len(req)} required skills"
    return score, reason


def _score_location(
    distance_km: float, max_distance_km: float
) -> tuple[float, str]:
    if max_distance_km <= 0:
        return 0.0, "Invalid search radius"
    if distance_km > max_distance_km:
        return (
            0.0,
            f"Outside search radius: {distance_km:.2f} km > {max_distance_km:.1f} km",
        )
    score = max(0.0, (1.0 - distance_km / max_distance_km) * 100.0)
    return (
        score,
        f"{distance_km:.2f} km away (within {max_distance_km:.1f} km radius)",
    )


def _score_availability(status: str) -> tuple[float, str]:
    normalized = status.strip().lower()
    score = AVAILABILITY_SCORES.get(normalized, 0.0)
    return score, f"Worker availability: {normalized}"


def _score_experience(
    worker_exp: float, min_exp: float
) -> tuple[float, str]:
    if min_exp <= 0 or worker_exp >= min_exp:
        return (
            100.0,
            f"Experience meets requirement ({worker_exp} yrs >= {min_exp} yrs)",
        )
    score = max(0.0, (worker_exp / min_exp) * 100.0)
    return (
        score,
        f"Partial experience ({worker_exp} yrs < {min_exp} yrs required)",
    )


def _score_wage(expected_wage: float, offered_wage: float) -> tuple[float, str]:
    if expected_wage <= 0 or offered_wage >= expected_wage:
        return (
            100.0,
            f"Offered wage (Rs.{offered_wage:.0f}/day) meets expected wage (Rs.{expected_wage:.0f}/day)",
        )
    score = max(0.0, (offered_wage / expected_wage) * 100.0)
    return (
        score,
        f"Offered wage (Rs.{offered_wage:.0f}/day) is below expected (Rs.{expected_wage:.0f}/day)",
    )


def score_worker_for_job(
    worker: dict[str, Any],
    job: dict[str, Any],
    max_distance_km: float = 15.0,
) -> MatchResult:
    """Compute weighted match score and explanation for a worker-job pair."""
    distance_km = haversine_distance_km(
        worker["latitude"],
        worker["longitude"],
        job["latitude"],
        job["longitude"],
    )

    skill_score, skill_reason = _score_skills(
        worker.get("skills", []), job.get("required_skills", [])
    )
    loc_score, loc_reason = _score_location(distance_km, max_distance_km)
    avail_score, avail_reason = _score_availability(
        worker.get("availability", "unavailable")
    )
    exp_score, exp_reason = _score_experience(
        float(worker.get("experience", 0)),
        float(job.get("min_experience", 0)),
    )
    wage_score, wage_reason = _score_wage(
        float(worker.get("expected_wage", 0)),
        float(job.get("offered_wage", 0)),
    )

    breakdown = {
        "skill": round(skill_score, 2),
        "location": round(loc_score, 2),
        "availability": round(avail_score, 2),
        "experience": round(exp_score, 2),
        "wage": round(wage_score, 2),
    }

    total_score = (
        WEIGHTS["skill"] * skill_score
        + WEIGHTS["location"] * loc_score
        + WEIGHTS["availability"] * avail_score
        + WEIGHTS["experience"] * exp_score
        + WEIGHTS["wage"] * wage_score
    )

    return MatchResult(
        worker_id=worker["worker_id"],
        worker_name=worker.get("full_name", worker["worker_id"]),
        job_id=job["job_id"],
        job_title=job.get("title", job["job_id"]),
        total_score=round(total_score, 2),
        distance_km=round(distance_km, 2),
        breakdown=breakdown,
        reasons=[
            skill_reason,
            loc_reason,
            avail_reason,
            exp_reason,
            wage_reason,
        ],
    )


def rank_workers_for_job(
    job: dict[str, Any],
    workers: list[dict[str, Any]],
    max_distance_km: float = 15.0,
    min_score: float = 0.0,
) -> list[MatchResult]:
    """Rank all candidate workers for a given job in descending score order."""
    results = [
        score_worker_for_job(worker, job, max_distance_km=max_distance_km)
        for worker in workers
    ]
    filtered = [r for r in results if r.total_score >= min_score]
    return sorted(filtered, key=lambda r: (-r.total_score, r.distance_km))


def rank_jobs_for_worker(
    worker: dict[str, Any],
    jobs: list[dict[str, Any]],
    max_distance_km: float = 15.0,
    min_score: float = 0.0,
) -> list[MatchResult]:
    """Rank open jobs for a given worker in descending score order."""
    open_jobs = [j for j in jobs if j.get("job_status", "open") == "open"]
    results = [
        score_worker_for_job(worker, job, max_distance_km=max_distance_km)
        for job in open_jobs
    ]
    filtered = [r for r in results if r.total_score >= min_score]
    return sorted(filtered, key=lambda r: (-r.total_score, r.distance_km))


def load_sample_data(
    base_dir: Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Load sample workers and jobs JSON files from the POC directory."""
    poc_dir = base_dir or Path(__file__).resolve().parent
    with (poc_dir / "sample_workers.json").open("r", encoding="utf-8") as wf:
        workers = json.load(wf)
    with (poc_dir / "sample_jobs.json").open("r", encoding="utf-8") as jf:
        jobs = json.load(jf)
    return workers, jobs


def main() -> None:
    """Run a CLI demonstration of worker-for-job ranking."""
    workers, jobs = load_sample_data()
    target_job = jobs[0]
    print(f"=== KaamConnect POC: Top Workers for '{target_job['title']}' ===")
    print(f"Required skills: {target_job['required_skills']} | Offered wage: Rs.{target_job['offered_wage']}/day\n")

    ranked = rank_workers_for_job(target_job, workers, max_distance_km=15.0)
    for idx, match in enumerate(ranked[:3], start=1):
        print(f"{idx}. {match.worker_name} ({match.worker_id}) - Score: {match.total_score}/100 ({match.distance_km} km)")
        for reason in match.reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
