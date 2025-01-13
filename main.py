from flask import Flask, render_template, request, redirect
from manage_files import add_to_file, read_from_file
app = Flask(__name__, static_folder="static", static_url_path="/")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/url", methods=["POST"])
def url():
    url_data = request.form["url"]

    add_to_file(url_data)
    return redirect("/")

@app.route("/pending")
def pending():
    return render_template("pending.html", pending_links=[])

if __name__ == "__main__":
    app.run(debug=True)