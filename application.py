from flask import Flask
from flask import render_template
from flask import request
from services.engine import get_products_by_category, predictions, show_data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    histograms_html, piecharts_html = show_data()
    prediction = None
    products_by_category = None
    if request.method == "POST":
        prediction = predictions(
            int(request.form["inputEducation"]),
            int(request.form["inputMaritalStatus"]),
            int(request.form["inputIncome"]),
            int(request.form["inputKids"]),
            int(request.form["inputTeens"]),
            int(request.form["inputAge"]),
        )
        products_by_category = get_products_by_category(prediction["Output"])
    return render_template(
        "index.html",
        histograms_html=histograms_html,
        piecharts_html=piecharts_html,
        prediction=prediction,
        products_by_category=products_by_category,
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("internal_server_error.html"), 500


if __name__ == "__main__":
    app.run()
