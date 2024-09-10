from flask import Flask, jsonify, request
from flask_cors import CORS
from services.FaceDetector import FaceDetector
from services.Response import Response

app = Flask(__name__)
CORS(app)

def NotFound():
    return jsonify({ 'data': False, 'statusCode': 404 })

def BadRequest():
    return jsonify({ 'data': False, 'statusCode': 400 })

def Ok(result: Response):
    return jsonify({ 'data': result, 'statusCode': 200 })


@app.route('/api/status', methods=['GET'])
def status():
    return Ok('API is running!')

@app.route('/api/validate', methods=['POST'])
def validate():
    try:
        if(len(request.files) == 0):
            return NotFound()
        
        image = request.files['image']
        faceDetector = FaceDetector(image)
        result = faceDetector.detect()
        return Ok(result.to_dict())
    except Exception as e:
        return BadRequest(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7400)


