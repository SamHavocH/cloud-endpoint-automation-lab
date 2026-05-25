import json
from pathlib import Path
from typing import Any


class GraphClient:
    """Demo Graph/Intune client abstraction.

    A production implementation would acquire Microsoft Graph tokens, call Intune managed
    device endpoints, handle pagination and throttling, and normalize Graph responses into
    local application schemas. This demo implementation reads fake data from disk so the
    project runs locally without tenant credentials.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        self.data_path = (
            data_path or Path(__file__).resolve().parents[1] / "fake_data" / "devices.json"
        )

    def list_managed_devices(self) -> list[dict[str, Any]]:
        """Return managed device records.

        Later this would call Microsoft Graph Intune managed devices APIs.
        """
        return json.loads(self.data_path.read_text(encoding="utf-8"))

    def sync_device(self, device_id: str) -> dict[str, str]:
        """Simulate an Intune device sync action.

        Later this would call the Graph action endpoint for the target managed device.
        """
        return {
            "device_id": device_id,
            "status": "queued",
            "message": "Demo sync request queued. No Graph tenant was contacted.",
            "dry_run": True,
        }

    def get_device_compliance(self, device_id: str) -> dict[str, str]:
        """Return a placeholder compliance lookup for one device.

        Later this would read compliance policy state from Microsoft Graph.
        """
        return {
            "device_id": device_id,
            "status": "demo",
            "message": "Compliance is calculated locally by the demo compliance engine.",
        }
