import logging
from flask import Flask, request

app = Flask(__name__)

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

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
	app.run(port=8080, debug=True)
