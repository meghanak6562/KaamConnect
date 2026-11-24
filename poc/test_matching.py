"""Unit tests for the KaamConnect matching engine proof of concept."""

from poc.matching_engine import (
    WEIGHTS,
    haversine_distance_km,
    load_sample_data,
    rank_jobs_for_worker,
    rank_workers_for_job,
    score_worker_for_job,
)


def test_weights_sum_to_one() -> None:
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_haversine_zero_distance() -> None:
    assert haversine_distance_km(13.3379, 77.1173, 13.3379, 77.1173) == 0.0


def test_haversine_known_distance() -> None:
    # Tumakuru to Bengaluru (~65-72 km straight line)
    dist = haversine_distance_km(13.3379, 77.1173, 12.9716, 77.5946)
    assert 60.0 < dist < 75.0


def test_perfect_match_scores_high() -> None:
    worker = {
        "worker_id": "w_test",
        "full_name": "Test Electrician",
        "skills": ["wiring", "mcb_repair"],
        "experience": 4,
        "expected_wage": 700,
        "availability": "available",
        "latitude": 13.3400,
        "longitude": 77.1200,
    }
    job = {
        "job_id": "j_test",
        "title": "Wiring Job",
        "required_skills": ["wiring", "mcb_repair"],
        "min_experience": 2,
        "offered_wage": 750,
        "latitude": 13.3400,
        "longitude": 77.1200,
        "job_status": "open",
    }
    result = score_worker_for_job(worker, job, max_distance_km=15.0)
    assert result.total_score == 100.0
    assert result.distance_km == 0.0
    assert "Matched 2/2 required skills" in result.reasons[0]


def test_rank_workers_for_job_orders_best_first() -> None:
    workers, jobs = load_sample_data()
    electrical_job = jobs[0]  # j_201: wiring + mcb_repair
    ranked = rank_workers_for_job(electrical_job, workers, max_distance_km=15.0)

    # Ramesh Kumar (w_101) is nearby, available, and has both wiring & mcb_repair
    assert ranked[0].worker_id == "w_101"
    assert ranked[0].total_score > ranked[1].total_score

    # Kiran Shetty (w_106) is ~18.7 km away -> outside 15 km radius -> location score 0
    kiran = next(r for r in ranked if r.worker_id == "w_106")
    assert kiran.breakdown["location"] == 0.0
    assert kiran.distance_km > 15.0


def test_rank_jobs_for_worker_ignores_closed_jobs() -> None:
    workers, jobs = load_sample_data()
    plumber = next(w for w in workers if w["worker_id"] == "w_103")
    jobs_copy = [dict(j) for j in jobs]
    jobs_copy[1]["job_status"] = "closed"

    ranked = rank_jobs_for_worker(plumber, jobs_copy, max_distance_km=15.0)
    assert all(r.job_id != "j_202" for r in ranked)


def test_unavailable_worker_gets_zero_availability_score() -> None:
    workers, jobs = load_sample_data()
    mason_unavailable = next(w for w in workers if w["worker_id"] == "w_105")
    mason_job = next(j for j in jobs if j["job_id"] == "j_204")

    result = score_worker_for_job(mason_unavailable, mason_job)
    assert result.breakdown["availability"] == 0.0
