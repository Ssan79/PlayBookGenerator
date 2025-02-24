from flask import Flask, request, Response, send_from_directory
import os

app = Flask(__name__)


# Serve the HTML form (index.html) at the root URL
@app.route("/", methods=["GET"])
def serve_index():
    # If you have 'index.html' in the same directory:
    return send_from_directory('.', 'index.html')


@app.route("/generate", methods=["POST"])
def generate():
    # 'playbook' is the hidden input (or client-side field) containing the final YAML
    playbook_yaml = request.form.get("playbook", "")

    if not playbook_yaml.strip():
        return "No playbook data was supplied."

    # Return the YAML so the browser downloads it as "playbook.yml"
    return Response(
        playbook_yaml,
        mimetype="text/yaml",
        headers={"Content-Disposition": "attachment; filename=playbook.yml"}
    )


if __name__ == "__main__":
    # Run Flask app on http://localhost:5000/
    app.run(debug=True)
