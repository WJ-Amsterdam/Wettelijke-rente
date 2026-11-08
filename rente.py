from datetime import date

DAYS_PER_YEAR = 365

RATE_TABLE = [
    (date(2022, 7, 1), 2.0),
    (date(2023, 1, 1), 4.0),
    (date(2023, 7, 1), 6.0),
    (date(2024, 1, 1), 7.0),
    (date(2025, 1, 1), 6.0),
    (date(2026, 1, 1), 4.0),
]

EARLIEST = RATE_TABLE[0][0]


def rate_on(d: date) -> float:
    rate = RATE_TABLE[0][1]
    for effective, value in RATE_TABLE:
        if d >= effective:
            rate = value
        else:
            break
    return rate


def parse_date(value: str) -> date:
    return date.fromisoformat(value.strip())


def bereken_wettelijke_rente(bedrag: float, startdatum: str, einddatum: str) -> dict:
    start = parse_date(startdatum)
    end = parse_date(einddatum)
    if end < start:
        raise ValueError(f"Einddatum {einddatum} ligt vóór startdatum {startdatum}.")
    if start < EARLIEST:
        raise ValueError(f"Startdatum {startdatum} ligt vóór {EARLIEST.isoformat()}.")
    if bedrag < 0:
        raise ValueError("Het bedrag mag niet negatief zijn.")

    boundaries = sorted({start, end} | {d for d, _ in RATE_TABLE if start < d < end})
    periods = []
    total = 0.0
    for seg_start, seg_end in zip(boundaries, boundaries[1:]):
        days = (seg_end - seg_start).days
        rate = rate_on(seg_start)
        interest = round(bedrag * (rate / 100.0) * (days / DAYS_PER_YEAR), 2)
        total += interest
        periods.append({
            "van": seg_start.isoformat(), "tot": seg_end.isoformat(),
            "dagen": days, "rente_percentage": rate, "rente_bedrag": interest,
        })
    return {
        "bedrag": bedrag, "startdatum": start.isoformat(), "einddatum": end.isoformat(),
        "totaal_dagen": (end - start).days,
        "berekeningswijze": f"enkelvoudige rente per dag: bedrag x rente% / {DAYS_PER_YEAR}",
        "periodes": periods, "totaal_rente": round(total, 2),
    }