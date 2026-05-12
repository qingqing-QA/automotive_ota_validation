from flask import Flask, jsonify, request

app = Flask(__name__)

vehicle_state = {
    "vehicle_id": "VIN123",
    "current_version": "1.0.0",
    "latest_version": "1.1.0",
    "status": "idle",
    "previous_version": "1.0.0"
}


@app.route("/vehicle/<vehicle_id>/version", methods=["GET"])
def get_vehicle_version(vehicle_id):
    if vehicle_id != vehicle_state["vehicle_id"]:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({
        "vehicle_id": vehicle_id,
        "current_version": vehicle_state["current_version"],
        "status": vehicle_state["status"]
    }), 200


@app.route("/ota/latest", methods=["GET"])
def get_latest_version():
    return jsonify({
        "latest_version": vehicle_state["latest_version"],
        "package_available": True
    }), 200


@app.route("/ota/download", methods=["POST"])
def download_update():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")
    simulate_failure = data.get("simulate_failure", False)

    if vehicle_id != vehicle_state["vehicle_id"]:
        return jsonify({"error": "Vehicle not found"}), 404

    if simulate_failure:
        vehicle_state["status"] = "download_failed"
        return jsonify({"error": "Download failed due to network issue"}), 500

    vehicle_state["status"] = "downloaded"
    return jsonify({
        "message": "OTA package downloaded successfully",
        "status": vehicle_state["status"]
    }), 200


@app.route("/ota/install", methods=["POST"])
def install_update():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")
    simulate_failure = data.get("simulate_failure", False)

    if vehicle_id != vehicle_state["vehicle_id"]:
        return jsonify({"error": "Vehicle not found"}), 404

    if vehicle_state["status"] != "downloaded":
        return jsonify({"error": "Update package not downloaded"}), 400

    if simulate_failure:
        vehicle_state["status"] = "install_failed"
        return jsonify({"error": "Installation failed due to corrupted package"}), 500

    vehicle_state["previous_version"] = vehicle_state["current_version"]
    vehicle_state["current_version"] = vehicle_state["latest_version"]
    vehicle_state["status"] = "installed"

    return jsonify({
        "message": "OTA update installed successfully",
        "current_version": vehicle_state["current_version"],
        "status": vehicle_state["status"]
    }), 200


@app.route("/ota/rollback", methods=["POST"])
def rollback_update():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")

    if vehicle_id != vehicle_state["vehicle_id"]:
        return jsonify({"error": "Vehicle not found"}), 404

    vehicle_state["current_version"] = vehicle_state["previous_version"]
    vehicle_state["status"] = "rolled_back"

    return jsonify({
        "message": "Rollback completed successfully",
        "current_version": vehicle_state["current_version"],
        "status": vehicle_state["status"]
    }), 200


@app.route("/ota/status", methods=["GET"])
def get_status():
    return jsonify({
        "vehicle_id": vehicle_state["vehicle_id"],
        "current_version": vehicle_state["current_version"],
        "latest_version": vehicle_state["latest_version"],
        "status": vehicle_state["status"]
    }), 200


@app.route("/reset", methods=["POST"])
def reset_state():
    vehicle_state["current_version"] = "1.0.0"
    vehicle_state["latest_version"] = "1.1.0"
    vehicle_state["status"] = "idle"
    vehicle_state["previous_version"] = "1.0.0"

    return jsonify({"message": "Vehicle state reset successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)