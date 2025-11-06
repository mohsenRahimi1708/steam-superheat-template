# src/api.py
from flask import Flask, request, jsonify
from src.superheat import superheat_temp

app = Flask(__name__)

@app.route("/superheat", methods=["GET"])
def api_superheat():
    """
    Example: GET /superheat?pressure=100&enthalpy=3300&unit=C
    Returns: {"temperature": 485.42, "unit": "°C"}
    """
    try:
        p = float(request.args.get("pressure"))
        h = float(request.args.get("enthalpy"))
        unit = request.args.get("unit", "C").upper()
        
        if unit not in ("C", "F"):
            return jsonify({"error": "unit must be 'C' or 'F'"}), 400

        temp = superheat_temp(p, h, unit)
        unit_symbol = "°C" if unit == "C" else "°F"
        
        return jsonify({
            "pressure_bar": p,
            "enthalpy_kJkg": h,
            "temperature": round(temp, 2),
            "unit": unit_symbol
        })
    
    except (TypeError, ValueError) as e:
        return jsonify({"error": "Invalid input: pressure and enthalpy must be numbers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# برای اجرا در محیط توسعه
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
