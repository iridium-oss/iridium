"""
Copernicus Data Space Ecosystem STAC provider. Primary catalog for Sentinel-2.
Uses STAC API at stac.dataspace.copernicus.eu. Optional auth for higher limits.
Reads CDSE_USERNAME/CDSE_PASSWORD or CDSE_CLIENT_ID/CDSE_CLIENT_SECRET from env when set.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx
from iridium_schemas.earth_observation import (
    EOBandAsset,
    EOScene,
    EOSceneMetadata,
    EOSceneSearchResult,
    EOSourceStatus,
)

COPERNICUS_STAC_BASE = "https://catalogue.dataspace.copernicus.eu/stac"
CDSE_TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
)
# New endpoint: https://stac.dataspace.copernicus.eu/ (may use /v1 or root)
S2_L2A_COLLECTION = "SENTINEL-2"
DEFAULT_TIMEOUT = 30.0

_cdse_token_cache: tuple[str, datetime | None] | None = None


def _get_cdse_bearer_token() -> str | None:
    """Optional CDSE OAuth2 token from env. Uses client_credentials or password grant. Cached until near expiry."""
    global _cdse_token_cache
    client_id = os.environ.get("IRIDIUM_EO__CDSE_CLIENT_ID") or os.environ.get("CDSE_CLIENT_ID")
    client_secret = os.environ.get("IRIDIUM_EO__CDSE_CLIENT_SECRET") or os.environ.get(
        "CDSE_CLIENT_SECRET"
    )
    username = os.environ.get("IRIDIUM_EO__CDSE_USERNAME") or os.environ.get("CDSE_USERNAME")
    password = os.environ.get("IRIDIUM_EO__CDSE_PASSWORD") or os.environ.get("CDSE_PASSWORD")
    if not (client_id and client_secret) and not (username and password):
        return None
    if _cdse_token_cache:
        token, expires = _cdse_token_cache
        if expires and (expires - datetime.now(UTC)).total_seconds() > 60:
            return token
        _cdse_token_cache = None
    try:
        with httpx.Client(timeout=15.0) as client:
            if client_id and client_secret:
                r = client.post(
                    CDSE_TOKEN_URL,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": client_id,
                        "client_secret": client_secret,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
            else:
                r = client.post(
                    CDSE_TOKEN_URL,
                    data={
                        "grant_type": "password",
                        "client_id": "cdse-public",
                        "username": username,
                        "password": password,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
            r.raise_for_status()
            data = r.json()
            access_token = data.get("access_token")
            expires_in = data.get("expires_in", 300)
            if access_token:
                expires_at = datetime.now(UTC) + timedelta(seconds=expires_in)
                _cdse_token_cache = (access_token, expires_at)
                return access_token
    except Exception:
        pass
    return None


def _auth_headers() -> dict[str, str]:
    """Optional Authorization header for CDSE when credentials are set."""
    token = _get_cdse_bearer_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


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
        if isinstance(asset, dict) and (key.upper().startswith("B") or "band" in key.lower()):
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
        confidence_note="Copernicus Data Space Ecosystem STAC; Sentinel-2.",
    )

    return EOScene(
        scene_id=item_id,
        collection=props.get("collection", S2_L2A_COLLECTION),
        metadata=metadata,
        assets=band_assets,
        asset_links=asset_links,
    )


class CopernicusStacProvider:
    """Copernicus Data Space Ecosystem STAC. Primary Sentinel-2 catalog."""

    provider_id = "copernicus_stac"

    def __init__(
        self,
        base_url: str = COPERNICUS_STAC_BASE,
        collection: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.collection = collection or S2_L2A_COLLECTION
        self.timeout = timeout

    def status(self) -> EOSourceStatus:
        """Report live if catalog is reachable."""
        try:
            headers = _auth_headers()
            with httpx.Client(timeout=10.0) as client:
                r = client.get(f"{self.base_url}/", headers=headers)
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
        """Search Copernicus STAC. bbox: (minx, miny, maxx, maxy)."""
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
            body["query"] = body.get("query", {})
            body["query"]["eo:cloud_cover"] = {"lte": cloud_cover_max}

        try:
            headers = _auth_headers()
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(f"{self.base_url}/search", json=body, headers=headers)
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
        """Fetch single item. Copernicus may expose /collections/{id}/items/{item_id}."""
        try:
            headers = _auth_headers()
            with httpx.Client(timeout=self.timeout) as client:
                r = client.get(
                    f"{self.base_url}/collections/{self.collection}/items/{scene_id}",
                    headers=headers,
                )
                if r.status_code != 200:
                    return None
                feature = r.json()
        except Exception:
            return None
        return _scene_from_feature(feature, self.provider_id)
