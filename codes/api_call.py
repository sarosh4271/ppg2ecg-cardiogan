from flask import Flask, jsonify, request
import subprocess
import test_cardiogan

app = Flask(__name__)

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})

@app.route('/cardiogan',methods=['POST'])
def post_ecg_data():
    res = request.get_json()
    try:
        listValues = test_cardiogan.process_all(res)
        x_ppg = listValues[1]
        x_ecg = listValues[0]
        x_ppg = x_ppg.tolist()
        x_ecg = x_ecg.tolist()
        # print('result from model ', resultFromModel)
        return {'ECG':x_ecg,'PPG':x_ppg}
    except Exception as e:
        return {'error': str(e)}

@app.route('/cardiogan',methods=['GET'])
def get_ecg_data():
    res = request.args
    print('data got: ',res)
    return jsonify({'post run':'success'})
if __name__ == '__main__':
    app.run()