import requests

BASE_URL = "http://127.0.0.1:5000"
VALID_VEHICLE_ID = "VIN123"
INVALID_VEHICLE_ID = "INVALID123"


def reset_vehicle_state():
    response = requests.post(f"{BASE_URL}/reset")
    assert response.status_code == 200


def test_get_vehicle_version_success():
    reset_vehicle_state()

    response = requests.get(f"{BASE_URL}/vehicle/{VALID_VEHICLE_ID}/version")
    body = response.json()

    assert response.status_code == 200
    assert body["vehicle_id"] == VALID_VEHICLE_ID
    assert body["current_version"] == "1.0.0"
    assert body["status"] == "idle"


def test_get_vehicle_version_invalid_vehicle_id():
    reset_vehicle_state()

    response = requests.get(f"{BASE_URL}/vehicle/{INVALID_VEHICLE_ID}/version")
    body = response.json()

    assert response.status_code == 404
    assert body["error"] == "Vehicle not found"


def test_get_latest_ota_version():
    reset_vehicle_state()

    response = requests.get(f"{BASE_URL}/ota/latest")
    body = response.json()

    assert response.status_code == 200
    assert body["latest_version"] == "1.1.0"
    assert body["package_available"] is True


def test_successful_ota_update_workflow():
    reset_vehicle_state()

    download_response = requests.post(
        f"{BASE_URL}/ota/download",
        json={"vehicle_id": VALID_VEHICLE_ID}
    )
    assert download_response.status_code == 200
    assert download_response.json()["status"] == "downloaded"

    install_response = requests.post(
        f"{BASE_URL}/ota/install",
        json={"vehicle_id": VALID_VEHICLE_ID}
    )
    install_body = install_response.json()

    assert install_response.status_code == 200
    assert install_body["status"] == "installed"
    assert install_body["current_version"] == "1.1.0"

    status_response = requests.get(f"{BASE_URL}/ota/status")
    status_body = status_response.json()

    assert status_response.status_code == 200
    assert status_body["current_version"] == "1.1.0"
    assert status_body["status"] == "installed"


def test_download_failure_network_issue():
    reset_vehicle_state()

    response = requests.post(
        f"{BASE_URL}/ota/download",
        json={
            "vehicle_id": VALID_VEHICLE_ID,
            "simulate_failure": True
        }
    )
    body = response.json()

    assert response.status_code == 500
    assert body["error"] == "Download failed due to network issue"

    status_response = requests.get(f"{BASE_URL}/ota/status")
    assert status_response.json()["status"] == "download_failed"


def test_install_without_download_should_fail():
    reset_vehicle_state()

    response = requests.post(
        f"{BASE_URL}/ota/install",
        json={"vehicle_id": VALID_VEHICLE_ID}
    )
    body = response.json()

    assert response.status_code == 400
    assert body["error"] == "Update package not downloaded"


def test_install_failure_corrupted_package():
    reset_vehicle_state()

    download_response = requests.post(
        f"{BASE_URL}/ota/download",
        json={"vehicle_id": VALID_VEHICLE_ID}
    )
    assert download_response.status_code == 200

    install_response = requests.post(
        f"{BASE_URL}/ota/install",
        json={
            "vehicle_id": VALID_VEHICLE_ID,
            "simulate_failure": True
        }
    )
    body = install_response.json()

    assert install_response.status_code == 500
    assert body["error"] == "Installation failed due to corrupted package"

    status_response = requests.get(f"{BASE_URL}/ota/status")
    assert status_response.json()["status"] == "install_failed"


def test_rollback_after_successful_update():
    reset_vehicle_state()

    requests.post(f"{BASE_URL}/ota/download", json={"vehicle_id": VALID_VEHICLE_ID})
    requests.post(f"{BASE_URL}/ota/install", json={"vehicle_id": VALID_VEHICLE_ID})

    rollback_response = requests.post(
        f"{BASE_URL}/ota/rollback",
        json={"vehicle_id": VALID_VEHICLE_ID}
    )
    body = rollback_response.json()

    assert rollback_response.status_code == 200
    assert body["status"] == "rolled_back"
    assert body["current_version"] == "1.0.0"


def test_invalid_vehicle_download_should_fail():
    reset_vehicle_state()

    response = requests.post(
        f"{BASE_URL}/ota/download",
        json={"vehicle_id": INVALID_VEHICLE_ID}
    )
    body = response.json()

    assert response.status_code == 404
    assert body["error"] == "Vehicle not found"