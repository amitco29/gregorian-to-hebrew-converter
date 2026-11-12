from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests

# Application Initialization & Configuration
app = Flask(__name__)

HEBCAL_API_URL = "https://www.hebcal.com/converter"
YEAR_RANGE = 200  # Allowed year offset (+/-) relative to the current year


# Web UI Route
@app.route("/")
def index():
    """Renders the main frontend user interface."""
    return render_template("index.html")


# Integration API Endpoint
@app.route("/api/convert", methods=["POST"])
def convert_date():
    """
    Receives a Gregorian date (YYYY-MM-DD) and sunset flag from the client,
    validates the input, queries the external Hebcal REST API, and returns
    a normalized JSON payload with the converted Hebrew date.
    """
    # 1. Extract & Validate Incoming Request Payload
    data = request.get_json(silent=True) or {}
    gregorian_date = str(data.get("date", "")).strip()
    after_sunset = bool(data.get("after_sunset", False))

    if not gregorian_date:
        return jsonify({"error": "Please select a valid date."}), 400

    try:
        parsed_date = datetime.strptime(gregorian_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400

    # 2. Dynamic Year Range Validation
    current_year = datetime.now().year
    min_year = current_year - YEAR_RANGE
    max_year = current_year + YEAR_RANGE

    if not (min_year <= parsed_date.year <= max_year):
        return jsonify({
            "error": f"Year must be between {min_year} and {max_year}."
        }), 400

    # 3. Build Query Parameters for Hebcal REST API
    params = {
        "cfg": "json",
        "date": gregorian_date,
        "g2h": 1,       # Conversion direction: Gregorian to Hebrew
        "strict": 1,    # Enforce HTTP 400 on invalid dates instead of fallback
    }
    if after_sunset:
        params["gs"] = "on"  # Advance Hebrew date by one day (post-sunset)

    # 4. Execute External HTTP GET Request with Error Handling
    try:
        response = requests.get(HEBCAL_API_URL, params=params, timeout=5)
        response.raise_for_status()
        hebcal_data = response.json()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Hebcal service timed out. Please try again."}), 504
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Failed to communicate with Hebcal API: {str(exc)}"}), 502

    # 5. Data Transformation & Response Formatting
    result = {
        "gregorian_date": parsed_date.strftime("%d/%m/%Y (%B %d, %Y)"),
        "hebrew_date": hebcal_data.get("hebrew", ""),
    }

    return jsonify(result), 200


# Entry Point
if __name__ == "__main__":
    app.run(debug=True)