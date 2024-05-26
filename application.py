from flask import Flask
from flask import render_template
from flask import request

from services.engine import predictions, show_data
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    data, histograms_html, piecharts_html = show_data()
    prediction = None
    if request.method == 'POST':
        prediction = predictions(
        int(request.form["inputEducation"]),
        int(request.form["inputMaritalStatus"]),
        int(request.form["inputIncome"]),
        int(request.form["inputKids"]),
        int(request.form["inputTeens"]),
        int(request.form["inputAge"]))
    return render_template('index.html', data=data,
                           histograms_html=histograms_html,
                           piecharts_html=piecharts_html,
                           prediction=prediction)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500


if __name__ == "__main__":
    app.run()
