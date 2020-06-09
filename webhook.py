from flask import Flask, request, make_response
import json
import os
import requests

app = Flask(__name__)

# app route decorator. when webhook is called, the decorator would call the functions which are e defined

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# extract parameter values, query weahter api, construct the resposne

def processRequest(req):
    result= req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")

    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=hyderabad,in&appid=db91df44baf43361cbf73026ce5156cb')
    json_object = r.json()
    weather = json_object['list']

    # for i in range(0,40):
        # if date in weather[i]['dt_txt']:
            # condition=weather[i]['weather'][0]['description']
    condition=weather[0]['weather'][0]['description']
    speech="The forecast is "+ condition
    return{
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [speech]
                }
            }
        ]
    }

if __name__=='__main__':
    port=int(os.getenv('PORT',5000))
    print("starting on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')