from flask import Flask, jsonify, request
import json
from services.FaceDetector import FaceDetector
from services.Response import Response

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'API is running!'})

@app.route('/validate', methods=['POST'])
def validate():
    try:
        image = request.files['image']
        faceDetector = FaceDetector(image)
        result = faceDetector.detect()
        response = Response(200, result)
        return jsonify({ 
                        'data': result,
                        'statusCode': 200
                    })
    except Exception as e:
        return jsonify({ 
                        'data': False,
                        'statusCode': 400
                    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7400)