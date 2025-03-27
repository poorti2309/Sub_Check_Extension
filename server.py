from flask import Flask, request, jsonify
from subscriptify_gui import get_website_text, analyze_subscription

app = Flask(__name__)

@app.route('/check_subscription', methods=['POST'])
def check_subscription():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid request data"}), 400

    url = data.get('url', 'subscriptify_gui.py').strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    text = get_website_text(url)
    if text.startswith("Error"):
        return jsonify({"result": text}), 400

    result = analyze_subscription(text)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
