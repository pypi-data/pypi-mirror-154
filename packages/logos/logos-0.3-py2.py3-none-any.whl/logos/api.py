import os
from typing import Union, Dict, Tuple, List
from flask import Flask, Response, render_template
from flask import request, jsonify
import json
from logos.ingest.transcript import Transcript
from logos.utils import config
from logos.preprocess.preprocess import PreProcess
from logos.utils import logger

template_folder = os.path.join(config['data_path'], config['data']['api'], 'templates')

app = Flask(__name__, template_folder=template_folder)

api_models_cache_ = {}

bad_request = Response(json.dumps({}), status=400, mimetype='application/json')
not_implemented = Response(json.dumps({'error': 'not implemented'}), status=501, mimetype='application/json')


@app.route('/')
def index() -> str:
    """Welcome Page"""
    return render_template('index.html')


@app.route('/api/help', methods=['GET'])
def help():
    """Available api endpoints."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = {"description": app.view_functions[rule.endpoint].__doc__,
                                    'methods': list(rule.methods)}
    return jsonify(func_list)


@app.route('/schemas/', methods=['GET'])
def list_schemas():
    """Logos schemas"""
    try:
        schemas_path = os.path.join(config['data_path'], config['data']['schemas'])
        data = os.listdir(schemas_path)
        return jsonify(data)
    except Exception as e:
        return bad_request


@app.route('/schemas/<schema_name>', methods=['GET'])
def schemas(schema_name):
    """Logos schema info"""
    try:
        schema_path = os.path.join(config['data_path'], config['data']['schemas'], schema_name)
        with open(schema_path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return bad_request


@app.route('/api/models/preprocess/normalize_text', methods=['POST'])
def normalize_text() -> Response:
    """WIP"""
    req_data = request.get_json()
    valid, text = http_get_text(req_data)
    if not valid:
        return bad_request

    try:
        text_clean = PreProcess.preprocess_turn(text)
        pred = {'text': text, 'pred': text_clean}
        js_data = json.dumps(pred, indent=4, sort_keys=True)
        resp = Response(js_data, status=200, mimetype='application/json')
    except Exception as e:
        logger.error(f"{e}")
        return bad_request

    return resp


@app.route('/api/models/preprocess/normalize_transcript', methods=['POST'])
def normalize_transcript() -> Response:
    """WIP"""
    return not_implemented


def http_get_transcript(req_data: Dict) -> Tuple[bool, Union[Transcript, None]]:
    """"""
    valid = False
    transcript = None
    try:
        transcript = Transcript(req_data['transcript'])
        valid = True
    except Exception as e:
        logger.error(f"{e}")

    return valid, transcript


def http_get_texts(req_data: Dict) -> Tuple[bool, Union[List[str], None]]:
    """"""
    valid = False
    texts = None
    try:
        texts = req_data['texts']
        valid = all([isinstance(text, str) for text in texts])
    except Exception as e:
        logger.error(f"{e}")
    return valid, texts


def http_get_text(req_data: Dict) -> Tuple[bool, Union[str, None]]:
    """"""
    valid = False
    text = None
    try:
        text = req_data['text']
        valid = isinstance(text, str)
    except Exception as e:
        logger.error(f"{e}")

    return valid, text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
