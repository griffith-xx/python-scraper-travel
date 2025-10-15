import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import get_page_destination_data
load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scraper", methods=["POST"])
def scraper():
    data = request.get_json()
    url = data.get("url")

    response = get_page_destination_data(url)

    return jsonify(response)
    



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
