"""boltpy — BOLT: Bibliographic Orchestration for Literature Triage."""

from __future__ import annotations

__version__ = "1.0.2"

from .core import HarvestConfig, HarvestResult, harvest

__all__ = ["__version__", "HarvestConfig", "HarvestResult", "harvest"]





