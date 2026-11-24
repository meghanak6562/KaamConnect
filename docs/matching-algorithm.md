# Matching Algorithm Specification

KaamConnect uses a deterministic, explainable **weighted multi-factor scoring algorithm** to rank workers for a job (and jobs for a worker). Every score is normalized to a `0–100` scale, making recommendations transparent and easy to audit.

> **Implementation:** A working Python proof of concept is implemented in [`poc/matching_engine.py`](../poc/matching_engine.py) and verified with automated tests in [`poc/test_matching.py`](../poc/test_matching.py).

---

## Weighting Model

| Factor | Weight | Purpose |
| :--- | :--- | :--- |
| **Skill Compatibility** | **40%** | Ensures the worker has the practical trade skills required by the job. |
| **Location Compatibility** | **30%** | Prioritizes hyper-local matches to minimize daily travel cost and time. |
| **Availability** | **15%** | Prioritizes workers who are immediately available for work. |
| **Experience** | **10%** | Rewards workers whose years of experience meet or exceed job expectations. |
| **Wage Compatibility** | **5%** | Aligns the employer's offered daily wage with the worker's expected daily wage. |
| **Total** | **100%** | Composite match score in the range `0.0` to `100.0`. |

---

## Factor-by-Factor Calculation

### 1. Skill Compatibility (`40%`)
Required job skills $R$ and worker skills $W$ are normalized to lowercase tokens.

$$\text{Skill Score} = \begin{cases} 100.0 & \text{if } |R| = 0 \\ \left(\frac{|R \cap W|}{|R|}\right) \times 100.0 & \text{otherwise} \end{cases}$$

- **Why overlap ratio over strict exact match?** If a job requires `["wiring", "mcb_repair", "earthing"]` and a worker has `["wiring", "mcb_repair"]`, they still score `66.7` instead of being discarded, allowing employers to see strong near-matches when exact matches are scarce.

### 2. Location Compatibility (`30%`) via Haversine Formula
Geographic distance $d$ (in kilometres) between worker coordinates $(\phi_1, \lambda_1)$ and job coordinates $(\phi_2, \lambda_2)$ is computed using the **Haversine formula** with Earth radius $R_e = 6371.0\text{ km}$:

$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)$$

$$d = 2 R_e \cdot \text{atan2}\left(\sqrt{a}, \sqrt{1 - a}\right)$$

Given a maximum search radius $D_{\max}$ (default `15.0 km`):

$$\text{Location Score} = \begin{cases} 0.0 & \text{if } d > D_{\max} \\ \left(1 - \frac{d}{D_{\max}}\right) \times 100.0 & \text{otherwise} \end{cases}$$

Workers or jobs outside `max_distance_km` can be filtered out or scored `0.0` on location.

### 3. Availability (`15%`)
| Worker Status | Score |
| :--- | :--- |
| `available` | `100.0` |
| `busy` (partially available / upcoming) | `40.0` |
| `unavailable` | `0.0` |

### 4. Experience (`10%`)
Compared against the job's `min_experience` (default `0` years):
- If `min_experience == 0` or `worker.experience >= job.min_experience`: `100.0`.
- Otherwise: `(worker.experience / job.min_experience) * 100.0`.

### 5. Wage Compatibility (`5%`)
Compares `job.offered_wage` against `worker.expected_wage`:
- If `offered_wage >= expected_wage`: `100.0`.
- If `offered_wage < expected_wage`: linearly scaled down based on the gap, floored at `0.0`:
  `max(0.0, (offered_wage / expected_wage) * 100.0)`.

---

## Composite Score Formula

$$\text{Total Score} = 0.40 \cdot S_{\text{skill}} + 0.30 \cdot S_{\text{location}} + 0.15 \cdot S_{\text{availability}} + 0.10 \cdot S_{\text{experience}} + 0.05 \cdot S_{\text{wage}}$$

---

## Assumptions & Limitations (POC)
1. **Straight-Line Distance:** Haversine computes great-circle distance rather than road-network travel time. In future phases, road-distance APIs can refine top-ranked candidates.
2. **Exact Token Normalization:** Skills are normalized by lowercase/trimming; synonym expansion (e.g., `wireman` → `wiring`) is handled upstream by the query/profile normalizer.
3. **Static Weights:** Weights (`40/30/15/10/5`) are fixed defaults for the POC and can be tuned per trade category in future releases.
