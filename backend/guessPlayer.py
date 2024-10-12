from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def default():
    return {"key": "value"}


@app.route("/members", methods=["GET"])
def members():
    return {"members": ["Viraj2", "Murab2"]}


@app.route("/get-members", methods=['POST'])
def get_member():
    print("Called !")
    data = request.get_json()
    name = data.get("name", "")
    age = data.get("age", 0)

    # Modify the name and age
    modified_name = name + " Viraj"
    modified_age = int(age) + 10

    print("Hitting get member on BackEnd")

    # Return the modified data
    return jsonify({"name": modified_name, "age": modified_age})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
