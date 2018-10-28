import os
import json
from flask import Flask, Response, abort
from flask import request


app = Flask(__name__)


def read_file(file_name, start=None, end=None):
    file_path = os.path.join(os.path.dirname(app.instance_path), 'files', file_name)
    if not os.path.exists(file_path):
        return None
    print(start, end)
    try:
        with open(file_path, 'r') as file:
            contents = file.readlines()
        if contents:
            if start and end:
                contents = contents[start:end]
            elif start:
                contents = contents[start:]
            elif end:
                contents = contents[:end]
        return contents
    except Exception as exp:
        return []


def try_parse_int(value):
    try:
        return int(value)
    except Exception as exp:
        return None


@app.route('/read/', defaults={'file_name': 'file1.txt'})
@app.route('/read/<file_name>/')
def book_list(file_name):
    start = request.args.get('start')
    end = request.args.get('end')
    if start:
        start = try_parse_int(start)
        if start:
            start = start - 1
            if start < 0:
                start = 0
    if end:
        end = try_parse_int(end)

    file_contents = read_file(file_name, start=start, end=end)
    if file_contents is None:
        response = Response(
            'The requested resource does not exist!', status=200, mimetype='text/plain')
        return response
    response = {
        'file_read': file_name,
        'number_of_lines_read': len(file_contents),
        'lines': file_contents
    }
    response = Response(
        json.dumps(response), status=200, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8005))
    app.run(host=host, port=port)
