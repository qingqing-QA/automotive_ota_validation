from app.ota_validator import validate_package

def test_checksum_mismatch_triggers_rollback():
    package = {
        "checksum_valid": False,
        "network_interrupted": False,
        "battery_level": 80
    }

    result = validate_package(package)

    assert result["status"] == "FAILED"
    assert result["rollback_required"] is True
    assert result["reason"] == "Checksum mismatch"

def test_network_interruption_triggers_rollback():
    package = {
        "checksum_valid": True,
        "network_interrupted": True,
        "battery_level": 80
    }

    result = validate_package(package)

    assert result["status"] == "FAILED"
    assert result["rollback_required"] is True

def test_valid_package_passes_validation():
    package = {
        "checksum_valid": True,
        "network_interrupted": False,
        "battery_level": 80
    }

    result = validate_package(package)

    assert result["status"] == "SUCCESS"
    assert result["rollback_required"] is False
