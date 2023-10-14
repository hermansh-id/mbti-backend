from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data from the data.json file
with open('data.json', 'r') as f:
    data = json.load(f)

# Initialize an empty dictionary to store the points for each type
type_points = {}


class Answer:
    def __init__(self, question_id, answer_id):
        self.question_id = question_id
        self.answer_id = answer_id


def handle_tie(pair, d):
    a = pair[0]
    b = pair[1]
    if a == b:
        if d[0] == 'E' and d[1] == 'I':
            return 'I'
        elif d[0] == 'S' and d[1] == 'N':
            return 'N'
        elif d[0] == 'T' and d[1] == 'F':
            return 'F'
        elif d[0] == 'J' and d[1] == 'P':
            return 'P'
    elif a > b:
        return d[0]
    else:
        return d[1]


def compare_points(type_points):
    E_I = handle_tie([type_points.get('E', 0), type_points.get('I', 0)], ["E", "I"])
    S_N = handle_tie([type_points.get('S', 0), type_points.get('N', 0)], ["S", "N"])
    T_F = handle_tie([type_points.get('T', 0), type_points.get('F', 0)], ["T", "F"])
    J_P = handle_tie([type_points.get('J', 0), type_points.get('P', 0)], ["J", "P"])
    return [E_I, S_N, T_F, J_P]


@app.route("/api/submit-answers", methods=["POST"])
def submit_answers():
    global type_points
    type_points = {}
    answers = request.get_json()
    for answer in answers:
        for question in data["questions"]:
            if question["id"] == str(answer["question_id"]):
                for ans in question["answers"]:
                    if ans["id"] == answer["answer_id"]:
                        type_points[ans["type"]] = type_points.get(ans["type"], 0) + ans["point"]

    result = compare_points(type_points)
    return jsonify({
        "data": type_points,
        "result": result
    })

