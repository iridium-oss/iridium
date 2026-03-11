"""
Source priority policy for transit data.
Alerts: official first, then public web observed, then licensed partner.
Predicted arrivals: official feed first, then public web observed, then licensed.
Route planning: official/OTP first, then 2GIS, Moovit, Yandex licensed.
"""


# Alert priority: 1 = highest.
ALERT_PRIORITY_ORDER = [
    "bakubus_official_alerts",
    "bakumetro_official_alerts",
    "yandex_transport_observed",
    "yandex_metro_operational",
    "moovit_partner",
]

# Predicted arrival priority.
PREDICTED_ARRIVAL_PRIORITY_ORDER = [
    "official_gtfs_realtime",  # if ever added
    "yandex_transport_observed",
    "moovit_partner",
    "twogis_public_transport",
]

# Route planning source priority.
ROUTE_PLANNING_PRIORITY_ORDER = [
    "otp_gtfs",  # repository-generated or official GTFS with OTP
    "twogis_public_transport",
    "moovit_partner",
    "yandex_licensed_routing",
]


def get_alert_priority_order() -> list[str]:
    """Return provider order for alerts: official first, then public web, then licensed."""
    return list(ALERT_PRIORITY_ORDER)


def get_predicted_arrival_priority_order() -> list[str]:
    """Return provider order for predicted arrivals."""
    return list(PREDICTED_ARRIVAL_PRIORITY_ORDER)


def get_route_planning_priority_order() -> list[str]:
    """Return provider order for route planning."""
    return list(ROUTE_PLANNING_PRIORITY_ORDER)


def _priority_rank(order: list[str], provider: str) -> int:
    """Lower rank = higher priority. Unknown provider gets last."""
    try:
        return order.index(provider)
    except ValueError:  # pragma: no cover
        return len(order)


def merge_alerts_by_priority(
    alert_lists: list[tuple[str, list]],
    order: list[str] | None = None,
) -> list:
    """
    Merge multiple (provider_id, alerts) lists and sort by source priority.
    Deduplication by alert_id; first occurrence wins.
    """
    order = order or get_alert_priority_order()
    seen_ids: set[str] = set()
    with_rank: list[tuple[int, any]] = []
    for provider_id, alerts in alert_lists:
        rank = _priority_rank(order, provider_id)
        for a in alerts:
            aid = getattr(a, "alert_id", str(a))
            if aid in seen_ids:
                continue
            seen_ids.add(aid)
            with_rank.append((rank, a))
    with_rank.sort(key=lambda x: (x[0], getattr(x[1], "alert_id", "")))
    return [a for _, a in with_rank]
