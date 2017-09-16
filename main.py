from flask import Flask, request
import logging
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = 'EAAXYaeZAmBqUBAKZBl0EzfMX23odMawbDKoejx1ZAdxpZCtNoFRLkZAqo5XTIqYuNL8dpibcdW9g4f6bAq8gwbKBm2ZBLVcccFlNCTN8T4CIXn8bensucNAmE4v09ZBAoqsz534G5sMycZBnlWWZCbeRw2hOP8KkF63nb6qMZAKqT6sQZDZD'
VERIFY_TOKEN = 'ggrks'

@app.route('/')
def hello():
    return "Hello dear, how are you today?"

@app.route('/test')
def test():
    return "Yes, you're testing this right!"

@app.route('/show', methods=['POST', 'GET'])
def show():
    data = request.args
    print(data['val1'])
    print(data['val2'])
    return str([data['val1'], data['val2']])

# GET request to handle the verification of tokens
@app.route('/fb', methods=['GET'])
def fb():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'

# method to reply to a message from the sender
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

# POST request to handle in coming messages then call reply()
@app.route('/fb', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print(json.dumps(data, indent=2))
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    print(sender, message)
    reply(sender, message)
    return "ok"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)
