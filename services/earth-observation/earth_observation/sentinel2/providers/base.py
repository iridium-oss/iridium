"""Base protocol and types for Sentinel-2 providers."""

from __future__ import annotations

from datetime import datetime

from iridium_schemas.earth_observation import (
    EOScene,
    EOSceneSearchResult,
    EOSourceStatus,
)


class Sentinel2ProviderProtocol:
    """Protocol for Sentinel-2 scene search. Implemented by STAC and optional Process API adapters."""

    provider_id: str

    def search(
        self,
        bbox: tuple[float, float, float, float],
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        cloud_cover_max: float | None = None,
        limit: int = 20,
    ) -> EOSceneSearchResult:
        """Search for Sentinel-2 scenes in the given bbox and date range."""
        raise NotImplementedError

    def get_scene(self, scene_id: str) -> EOScene | None:
        """Fetch a single scene by id. Returns None if not found."""
        raise NotImplementedError

    def status(self) -> EOSourceStatus:
        """Report whether the provider is available and configured."""
        raise NotImplementedError
