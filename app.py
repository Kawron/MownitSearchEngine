from flask import Flask, render_template, request, jsonify
import searchEngine as backend


app = Flask(__name__, static_folder="my-app/build/static", template_folder="my-app/build")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    print(request.json)
    if "query" not in request.json:
        return "Bad request", 400

    if "svd_k" in request.json:
        res = backend.searchQuery(request.json["query"], request.json["svd_k"])
    else:
        res = backend.searchQuery(request.json["query"], False)


    return jsonify({"result": res}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)