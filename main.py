import json
from flask import Flask, jsonify, request
from model.twit import Twit

twits = []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/ping', methods=["GET"])
def ping():
    return jsonify({'response': 'pong'})

@app.route('/twit', methods=["POST"])
def create_twit():
    '''{"body":"Hello World", "author": "@TimDzen"}'''
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], 
                twit_json['author'],
                twit_json['id']
               )
    twits.append(twit)
    return jsonify({'status': 'success'})


@app.route('/twit', methods=["GET"])
def read_twits():
        return jsonify({'twits': [{'id': twit.id,
                                   'body': twit.body,
                                   'author': twit.author} for twit in twits]}
                      )

@app.route('/twit/<int:twit_id>', methods=["DELETE"])
def delete_twit(twit_id):
    global twits
    initial_length = len(twits)
    twits = [twit for twit in twits if twit.id != twit_id]
    if len(twits) < initial_length:
        return jsonify({"message": "Twit deleted successfully"})
    return jsonify({"message": "Twit not found"}), 404

@app.route('/twit/<int:twit_id>', methods=["PUT"])
def update_twit(twit_id):
    global twits
    twit_json = request.get_json()

    for twit in twits:
        if twit.id == twit_id:
            twit.body = twit_json.get('body', twit.body)
            twit.author = twit_json.get('author', twit.author)
            return jsonify({'status': 'success',
                            'message': 'Twit updated successfully'}
                          )

    return jsonify({'status': 'error',
                    'message': 'Twit not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json

    users.append(data)

    return jsonify({'message': 'Пользователь создан'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})




if __name__ == '__main__':
    app.run(debug=True)
