from assistant import Assistant
from flask import Flask, request,jsonify

import requests
from bs4 import BeautifulSoup as bs

from Modules.BaseModule import ses

url = "https://www.whatismyip.com/"

req = requests.get(url)

soup = bs(req.content,"html.parser")

for i in soup.find_all("span"):
	if "IP:" in i.text:
		ip = i.text.split()[2]

assistant = Assistant()
db = assistant.db

ses = ses()

db.reference("/server_ip").set(ip)

app = Flask(__name__)

passw = "1q2W3e4R"

def get_data(path):
	return db.reference(path).get()

@app.route("/")
def index():
	return "Selam"

@app.route("/get_result", methods=["GET","POST"])
def get_result():
	args = request.args
	if args["pass"] == passw:
		if "q" in args:
			query = args["q"]

			text, i, ii = None, None, None

			result = assistant.get_result(query)

			if isinstance(result,tuple) and len(result) == 3:
				text, i, ii = result
			elif isinstance(result,tuple) and len(result) == 2:
				text, i = result
			elif isinstance(result,str):
				text = result

			if i == "h_lar_oku":
				reminder_list = ii

				reminder_list.sort(reverse=True)

				return jsonify({"result":[text,i,reminder_list]})

			elif i == "durumD":
				return jsonify({"result":[text,i,ii]})

			elif i == "ses_seviyesi":
				r = ses.currentVolume()
				if r[1] == 0:
					status = "açık"
				elif r[1] == 1:
					status = "kapalı"
				return jsonify({"result":[text.format(r[0],status),i,ii]})

			elif i == "ses_ayar":
				r = ses.setVolume(ii)
				if r:
					return jsonify({"result":[text.format(ii),i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_arttır2":
				r = ses.volumeUp(ii)
				if r:
					return jsonify({"result":[text.format(ii),i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_azalt2":
				r = ses.volumeDOWN(ii)
				if r:
					return jsonify({"result":[text.format(ii),i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_arttır":
				r = ses.volumeUP(5)
				if r:
					return jsonify({"result":[text,i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_azalt":
				r = ses.volumeDOWN(5)
				if r:
					return jsonify({"result":[text,i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_kapat":
				r = ses.volumeSetMute(True)
				if r:
					return jsonify({"result":[text,i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "ses_aç":
				r = ses.volumeSetMute(False)
				if r:
					return jsonify({"result":[text,i,ii]})
				else:
					return jsonify({"result":["Malesef bir hata oluştu!",i,ii]})

			elif i == "kapi_son_kilit":
				last_lock_date = get_data("/door_lock/last_lock_date").replace("\"","")

				return jsonify({"result":[text.format(last_lock_date),i,ii]})

			elif i == "selam_ver":
				query2 = query.split()
				del query2[-2:]

				for g in query2:
					gg = g.split("'")
					if len(gg) > 1:
						query2[query2.index(g)] = "".join(gg[0])

					elif "abla" in g:
						del query2[query2.index(g)]

					elif "abi" in g:
						del query2[query2.index(g)]

					elif g.lower() == "anneme":
						query2[query2.index(g)] = "Sevgül"

					elif g.lower() == "babama":
						query2[query2.index(g)] = "Cevdet"

				query2 = " ".join(query2)

				return jsonify({"result":[text.format(query2),i,ii]})

			else:
				return jsonify({"result":[text,i,ii]})

		else:
			return jsonify({"error":"Eksik Eleman: q"})
	else:
		return jsonify({"error":"Hatalı Şifre"})

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True, port=60189)