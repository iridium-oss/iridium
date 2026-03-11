"""
Earth Search STAC provider. Fallback open catalog for Sentinel-2 L2A.
No authentication required. Collection: sentinel-2-l2a.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx
from iridium_schemas.earth_observation import (
    EOBandAsset,
    EOScene,
    EOSceneMetadata,
    EOSceneSearchResult,
    EOSourceStatus,
)

EARTH_SEARCH_STAC_BASE = "https://earth-search.aws.element84.com/v1"
SENTINEL_2_L2A_COLLECTION = "sentinel-2-l2a"
DEFAULT_TIMEOUT = 30.0


def _parse_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _scene_from_feature(feature: dict[str, Any], provider_id: str) -> EOScene:
    props = feature.get("properties", {})
    geom = feature.get("geometry")
    item_id = feature.get("id", "unknown")
    assets = feature.get("assets", {})

    cloud = props.get("eo:cloud_cover")
    if cloud is not None and not isinstance(cloud, (int, float)):
        cloud = None

    acquired = _parse_datetime(props.get("datetime") or props.get("start_datetime"))

    bbox = feature.get("bbox")
    if bbox and len(bbox) >= 4:
        bbox = list(bbox)[:4]
    else:
        bbox = None

    band_assets: list[EOBandAsset] = []
    asset_links: dict[str, str] = {}
    for key, asset in assets.items():
        href = asset.get("href") if isinstance(asset, dict) else None
        if href:
            asset_links[key] = href
        if isinstance(asset, dict) and key.upper().startswith("B"):
            band_assets.append(
                EOBandAsset(
                    band_name=key,
                    asset_key=key,
                    href=href,
                )
            )

    metadata = EOSceneMetadata(
        source_provider=provider_id,
        source_family="stac_catalog",
        source_status=EOSourceStatus.live,
        acquired_at=acquired,
        cloud_cover=float(cloud) if cloud is not None else None,
        bbox=bbox,
        geometry=geom,
        confidence_note="Earth Search STAC; Sentinel-2 L2A.",
    )

    return EOScene(
        scene_id=item_id,
        collection=props.get("collection", SENTINEL_2_L2A_COLLECTION),
        metadata=metadata,
        assets=band_assets,
        asset_links=asset_links,
    )


class EarthSearchStacProvider:
    """Earth Search STAC API provider. No credentials required."""

    provider_id = "earth_search_stac"

    def __init__(
        self,
        base_url: str = EARTH_SEARCH_STAC_BASE,
        collection: str = SENTINEL_2_L2A_COLLECTION,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.collection = collection
        self.timeout = timeout

    def status(self) -> EOSourceStatus:
        """Earth Search is public; report live if endpoint is reachable."""
        try:
            with httpx.Client(timeout=5.0) as client:
                r = client.get(f"{self.base_url}/")
                if r.status_code == 200:
                    return EOSourceStatus.live
        except Exception:
            pass
        return EOSourceStatus.unavailable

    def search(
        self,
        bbox: tuple[float, float, float, float],
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        cloud_cover_max: float | None = None,
        limit: int = 20,
    ) -> EOSceneSearchResult:
        """Search Earth Search STAC. bbox: (minx, miny, maxx, maxy)."""
        body: dict[str, Any] = {
            "collections": [self.collection],
            "bbox": list(bbox),
            "limit": min(limit, 100),
        }
        if date_start or date_end:
            parts = []
            if date_start:
                parts.append(date_start.isoformat())
            else:
                parts.append("..")
            if date_end:
                parts.append(date_end.isoformat())
            else:
                parts.append("..")
            body["datetime"] = "/".join(parts)
        if cloud_cover_max is not None:
            body["query"] = {"eo:cloud_cover": {"lte": cloud_cover_max}}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(f"{self.base_url}/search", json=body)
                r.raise_for_status()
                data = r.json()
        except Exception as e:
            return EOSceneSearchResult(
                scenes=[],
                source_provider=self.provider_id,
                source_status=EOSourceStatus.unavailable,
                searched_at=datetime.now(UTC),
                bbox=list(bbox),
                date_start=date_start,
                date_end=date_end,
                cloud_cover_max=cloud_cover_max,
                note=str(e),
            )

        features = data.get("features", [])
        scenes = [_scene_from_feature(f, self.provider_id) for f in features]

        return EOSceneSearchResult(
            scenes=scenes,
            total_count=data.get("numberMatched"),
            source_provider=self.provider_id,
            source_status=EOSourceStatus.live,
            searched_at=datetime.now(UTC),
            bbox=list(bbox),
            date_start=date_start,
            date_end=date_end,
            cloud_cover_max=cloud_cover_max,
        )

    def get_scene(self, scene_id: str) -> EOScene | None:
        """Fetch single item by id. Earth Search does not expose a direct item URL; use search."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.get(f"{self.base_url}/collections/{self.collection}/items/{scene_id}")
                if r.status_code != 200:
                    return None
                feature = r.json()
        except Exception:
            return None
        return _scene_from_feature(feature, self.provider_id)
