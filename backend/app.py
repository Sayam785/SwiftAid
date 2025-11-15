from flask import Flask, request, jsonify, render_template
from disaster_system_dsa import SYSTEM
from datetime import datetime

app = Flask(__name__, template_folder="templates")

USERS = {"admin": "admin123"}
for i in range(1, 11):
    USERS[f"user{i}"] = "1234"
for i in range(101, 121):
    USERS[f"v{i}"] = "1234"

VOLUNTEER_LOCATIONS = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in USERS and USERS[username] == password:
        return jsonify({"success": True, "username": username})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/api/report", methods=["POST"])
def report():
    data = request.json
    is_emergency = data.get("is_emergency", "false").lower() == "true"
    if not data.get("report_photo"):
        return jsonify({"error": "Report failed. Proof photo is mandatory."})
    volunteers_needed = int(data.get("volunteers_needed", 1))
    did = SYSTEM.report_disaster(
        dtype=data.get("type"),
        severity=int(data.get("severity", 5)),
        is_emergency=is_emergency,
        volunteers_needed=volunteers_needed,
        supplies_needed=data.get("supplies_needed", ""),
        description=data.get("description", ""),
        reported_by=data.get("reported_by"),
        location=data.get("location", "Unknown Location"),
        report_photo=data.get("report_photo", None)
    )
    return jsonify({"message": f"Disaster reported with ID {did}"})

@app.route("/api/view", methods=["GET"])
def view_disasters():
    reporter_id = request.args.get("reporter_id")
    if reporter_id:
        return jsonify(SYSTEM.get_disasters_by_reporter(reporter_id))
    else:
        return jsonify(SYSTEM.get_all_disasters())

@app.route("/api/resolve", methods=["POST"])
def resolve():
    data = request.json
    disaster_id = int(data["disaster_id"])
    resolution_photo = data.get("resolution_photo", None)
    if not resolution_photo:
        return jsonify({"error": "Resolution requires a proof photo."})
    if SYSTEM.resolve_disaster(disaster_id, resolution_photo):
        return jsonify({"message": f"Disaster {disaster_id} verified and resolved."})
    return jsonify({"error": f"Disaster {disaster_id} not found or already resolved."})

@app.route("/api/delete-disaster", methods=["POST"])
def delete_disaster():
    data = request.json
    try:
        disaster_id = int(data["disaster_id"])
    except (KeyError, ValueError):
        return jsonify({"success": False, "error": "Invalid or missing disaster ID."})
    reporter_id = data.get("reporter_id")
    success, message = SYSTEM.delete_disaster(disaster_id, reporter_id)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "error": message})

@app.route("/api/volunteers", methods=["GET"])
def get_volunteers():
    vols = SYSTEM.get_all_volunteers()
    for v in vols:
        v['location_data'] = VOLUNTEER_LOCATIONS.get(v['id'], {'lat': 'N/A', 'lon': 'N/A', 'timestamp': 'Never'})
    return jsonify(vols)

@app.route("/api/assign", methods=["POST"])
def assign_volunteer():
    data = request.json
    disaster_id = int(data["disaster_id"])
    volunteer_id = data["volunteer_id"]
    deployment_message = data.get("deployment_message", "Deployment initiated. Proceed with caution.")
    if SYSTEM.assign_volunteer(disaster_id, volunteer_id, deployment_message):
        return jsonify({"message": f"Volunteer {volunteer_id} assigned to {disaster_id}"})
    return jsonify({"error": "Assignment failed (busy, full, or not found)"})

@app.route("/api/auto-assign", methods=["POST"])
def auto_assign():
    data = request.json
    disaster_id = int(data["disaster_id"])
    deployment_message = data.get("deployment_message", "Auto-Deployment initiated. Proceed with caution.")
    if SYSTEM.auto_assign_volunteers(disaster_id, deployment_message):
        return jsonify({"message": f"Auto assignment initiated for {disaster_id}"})
    return jsonify({"error": "Auto-assignment failed (no available volunteers)"})

@app.route("/api/volunteer-update", methods=["POST"])
def volunteer_update():
    data = request.json
    did = data["disaster_id"]
    vid = data["volunteer_id"]
    priority = data["priority"]
    description = data["description"]
    update_photo = data.get("update_photo")
    if SYSTEM.add_volunteer_update(did, vid, priority, description, update_photo):
        return jsonify({"success": True, "message": "Update successfully delivered to Admin."})
    return jsonify({"success": False, "error": "Failed to post update. Disaster not found."})

@app.route("/api/location", methods=["POST"])
def update_location():
    data = request.json
    volunteer_id = data["volunteer_id"]
    VOLUNTEER_LOCATIONS[volunteer_id] = {
        "lat": data["lat"],
        "lon": data["lon"],
        "timestamp": data["timestamp"]
    }
    return jsonify({"message": "Location updated"})

if __name__ == "__main__":
    app.run(debug=True)
