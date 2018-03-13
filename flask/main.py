from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/request', methods=['POST'])
def apiRequestHandler():
    json = request.get_json()
    url = json["query"]
    method = json["method"]
    payload = None
    if ("payload" in json):
    	payload = json["payload"]
    	print(payload)
    return routeRequest(method, url, payload)

def routeRequest(method, query, payload):
	result = ""
	if (method == "GET"):
		result = requests.get(query, verify=False).text
	elif (method == "POST"):
		result = requests.post(query, verify=False, json=payload).text
	elif (method == "PUT"):
		result = requests.put(query, verify=False, json=payload).text
	elif (method == "DELETE"):
		result = requests.delete(query, verify=False).text
	else:
		result = "Invalid REST method."
	return result