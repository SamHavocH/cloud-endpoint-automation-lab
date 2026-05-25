# Microsoft Graph Integration Path

The current project runs in demo mode and does not require Microsoft Graph credentials. A real integration can replace `GraphClient` while keeping the API and dashboard mostly unchanged.

## App Registration

A production integration would start with an Entra ID application registration. The app would represent this service when calling Microsoft Graph. Terraform already creates a placeholder application registration and service principal.

## Permissions

The app would need carefully scoped Microsoft Graph permissions for Intune managed device data and device actions. Permission choice should follow least privilege and be reviewed by tenant administrators.

## Token Acquisition

The backend would acquire access tokens using a secure credential path such as managed identity, workload identity federation, or certificate-based credentials. Client secrets are convenient for demos but are not preferred for production.

## Managed Devices

`GraphClient.list_managed_devices()` would call Microsoft Graph managed device endpoints, handle pagination, retries, throttling, and response normalization. `sync_device()` would call the appropriate device action endpoint. Compliance state could be read from Graph or recalculated locally depending on the operating model.

## Security Considerations

Store credentials outside source control, restrict app permissions, monitor Graph API usage, log administrative actions, and avoid returning sensitive device data to unauthorized users. Production APIs should add authentication, authorization, request auditing, and rate limiting.
