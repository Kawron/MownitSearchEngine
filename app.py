from flask import Flask, render_template
from flask import request, jsonify
import zad as back


app = Flask(__name__, static_folder="frontend/build/static", template_folder="frontend/build")
# search_engine = SearchEngine("150k", 150000)
# search_engine_svd = SearchEngine("5k", 5000, low_rank_approx=True, k=500)


@app.route("/")
def render():
    return render_template('index.html')


@app.route("/search_query", methods=['POST'])
def search_query():
    if "search_query" not in request.json or "low_rank_approx" not in request.json:
        return "Wrong request", 400

    print(request.json)

    ## to zaraz
    if request.json["low_rank_approx"]:
        result = back.main(request.json["search_query"])
    else:
        result = back.main(request.json["search_query"])

    print(result)

    return jsonify({"result": result}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)