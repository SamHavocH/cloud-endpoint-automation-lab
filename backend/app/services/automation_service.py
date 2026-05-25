from datetime import UTC, datetime

from app.models import Device
from app.services.compliance_engine import evaluate_device, recommended_actions
from app.services.graph_client import GraphClient


class AutomationService:
    def __init__(self, graph_client: GraphClient | None = None) -> None:
        self.graph_client = graph_client or GraphClient()

    def sync_device(self, device: Device) -> dict[str, object]:
        response = self.graph_client.sync_device(device.id)
        response["timestamp"] = datetime.now(UTC)
        return response

    def remediate_device(self, device: Device) -> dict[str, object]:
        _, failed_rules = evaluate_device(device)
        actions = recommended_actions(failed_rules)
        return {
            "device_id": device.id,
            "status": "recommended_actions_generated" if actions else "no_action_required",
            "message": "Demo remediation analysis completed. No device changes were executed.",
            "dry_run": True,
            "timestamp": datetime.now(UTC),
            "recommended_actions": actions,
        }
