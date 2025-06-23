from flask import Flask, request, send_from_directory
from flask_cors import CORS
from roku import Roku

app = Flask(__name__)
CORS(app)

# --- Config ---
r = Roku("192.168.1.35")  # Your Roku's IP
wanted_apps = {"Jellyfin", "Netflix", "Prime Video", "iHeart", "YouTube", "Max"}

# --- Routes ---

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/press/<button>")
def press(button):
    try:
        getattr(r, button)()
        return f"{button} pressed", 200
    except Exception as e:
        return str(e), 400

@app.route("/apps")
def list_apps():
    try:
        return [
            {
                "name": app.name,
                "id": app.id,
                "icon": f"http://{r.host}:8060/query/icon/{app.id}"
            }
            for app in r.apps if app.name in wanted_apps
        ]
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/launch/<app_id>")
def launch_app(app_id):
    try:
        r[app_id].launch()
        return f"Launched {app_id}", 200
    except Exception as e:
        return str(e), 400

@app.route("/type", methods=["POST"])
def type_text():
    try:
        data = request.get_json()
        r.literal(data.get("text", ""))
        return "Text sent", 200
    except Exception as e:
        return str(e), 400

@app.route("/backspace")
def backspace():
    try:
        r.press("Backspace")
        return "Backspace sent", 200
    except Exception as e:
        return str(e), 400

# --- Run ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
