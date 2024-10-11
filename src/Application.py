import ssl
from dotenv import load_dotenv  
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.FaceDetector import FaceDetector
from services.Response import Response

load_dotenv()

app = Flask(__name__)
CORS(app)
print(os.getenv('ENV'))
if(os.getenv('ENV') == 'production' and os.path.exists('/etc/ssl/certs/privat.key')):
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.load_cert_chain('/etc/ssl/certs/app.crt', '/etc/ssl/certs/privat.key')
else:
    raise Exception('CERTIFICADOS SSL NÃO ENCONTRADOS!')


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
    if(os.getenv('ENV') == 'production'):
        app.run(host='0.0.0.0', port=443, ssl_context=ctx)
    else:
        app.run(host='0.0.0.0', port=7400)


