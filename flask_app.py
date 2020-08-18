from assistant import Assistant
from flask import Flask, request,jsonify

assistant = Assistant()
app = Flask(__name__)

passw = "1q2W3e4R"

@app.route("/")
def index():
	return "Selam"

@app.route("/get_result", methods=["GET","POST"])
def get_result():
	args = request.args
	if args["pass"] == passw:
		if "q" in args:
			text, i, ii = None, None, None

			result = assistant.get_result(args["q"])

			if isinstance(result,tuple) and len(result) == 3:
				text, i, ii = result
			elif isinstance(result,tuple) and len(result) == 2:
				text, i = result
			elif isinstance(result,str):
				text = result

			return jsonify({"result":[text,i,ii]})
		else:
			return jsonify({"error":"Eksik Eleman: q"})
	else:
		return jsonify({"error":"Hatalı Şifre"})

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True, port=60189)