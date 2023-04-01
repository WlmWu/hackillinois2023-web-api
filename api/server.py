import argparse
from flask import Flask, request
from flask_restful import Resource, Api
import socket
from waitress import serve

from transactionExaminer import Examiner
import json

Exmr = Examiner()
class ExaminerAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.exmr = Exmr

    def post(self):
        receive = request.get_json()
        print(receive)

        rtn = self.exmr.handleRecv(receive)
        print(rtn)
    
        return json.dumps(rtn)


app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>API is currently running!</h1>"

# api = Api(app)
# api.add_resource(ExaminerAPI, '/acceptance')

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Server script')
    parser.add_argument('-p', dest='port', type=int, default=8000)
    args = parser.parse_args()


    api = Api(app)
    api.add_resource(ExaminerAPI, '/acceptance')

    ip = socket.gethostbyname(socket.gethostname())
    print(f'Flask Server Starts on \n{ip}:{args.port}')
    serve(app, host=ip, port=args.port)
    app.run()