from flask import Flask, request, jsonify
import test_cardiogan

app = Flask(__name__)

@app.route('/cardiogan',methods=['POST'])
def get_raw_data():
    res = request.get_json()
    try:
        listValues = test_cardiogan.process_raw_data(res)
        x_ppg = listValues[1]
        x_ecg = listValues[0]
        x_ppg = x_ppg.tolist()
        x_ecg = x_ecg.tolist()

        reply = {'ECG':x_ecg,'PPG':x_ppg}
        print(reply)
        return reply
    except Exception as e:
        return jsonify(error=str(e)),500

if __name__ == '__main__':
    app.run()