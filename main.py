from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, Boolean
from modules.dowloader import download_pending

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///downloader.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

#CREATE DB TABLE
class Url(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(String(150), unique=False, nullable=True)
    format: Mapped[str] = mapped_column(String(5), unique=False, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
    date_completed: Mapped[Date] = mapped_column(Date(), nullable=True)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_url", methods=["POST"])
def add_url():
    url_data = request.form["url"]
    url_format = request.form["format"]

    new_url = Url(url=url_data, format=url_format)

    db.session.add(new_url)
    db.session.commit()

    return redirect("/")

@app.route("/pending")
def pending():
    pending_urls = db.session.execute(db.select(Url)).scalars()
    return render_template("pending.html", pending_urls=pending_urls)

@app.route("/delete/<id>")
def delete(id):
    print(id)
    return redirect("/pending")

@app.route("/download_all")
def download_all():
    pending_urls = db.session.execute(db.select(Url)).scalars()
    url_list = []

    for url in pending_urls:
        url_list.append(
            {
                "url" : url.url,
                "format" : url.format
            })

    download_pending(url_list)
    return redirect("/pending")

@app.route("/download/<id>")
def download_id(id):
    return redirect("/pending")

if __name__ == "__main__":
    app.run(debug=True)