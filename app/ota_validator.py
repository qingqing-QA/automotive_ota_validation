def validate_package(package):
    if not package.get("checksum_valid"):
        return {
            "status": "FAILED",
            "reason": "Checksum mismatch",
            "rollback_required": True
        }

    if package.get("network_interrupted"):
        return {
            "status": "FAILED",
            "reason": "Network interruption",
            "rollback_required": True
        }

    if package.get("battery_level", 100) < 30:
        return {
            "status": "FAILED",
            "reason": "Low battery level",
            "rollback_required": True
        }

    return {
        "status": "SUCCESS",
        "reason": "Package validation passed",
        "rollback_required": False
    }
