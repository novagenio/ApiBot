from flask import Flask, request, Response, jsonify, json
import time


import extract_msg
import re
import pandas as pd

app = Flask(__name__)



def find_isin(msg_message, msg_subj):
	msg_message = msg_message
	if msg_message == '':
		isin = re.findall('[A-Z]{2}[A-Z0-9]{9}[0-9]', msg_subj)
		date = re.findall(r"(tom|TOM|T/-|spot|spot/open)", msg_subj)
	else:
		isin = re.findall('[A-Z]{2}[A-Z0-9]{9}[0-9]', msg_message)
		date = re.findall(r"(tom|TOM|T/-|spot|spot/open)", msg_message)
	return isin, date

@app.route("/person", methods=['POST', 'GET']) # aquí especificamos que estos endpoints aceptan solicitudes.

def handle_person(): 
	if request.method == 'POST': 
		msg_message = request.args.get('msg_message')
		msg_subj = request.args.get('msg_subj')
		print(msg_message)
		print(msg_subj)

		msg_message, date = find_isin(msg_message, msg_subj)
		isim = str(msg_message)
		date = str(date)

		isim = re.sub("\[|\]|\'","",isim)
		date = re.sub("\[|\]|\'","",date)
		spot=0
		tom=0

		print("isim, date despues del corte", isim, date)
		df = pd.read_csv("bot2.csv",sep = ';')
		#        print(df)

		try:
			df_mask=df['seccode']==isim
			filtered_df = df[df_mask]
			print(filtered_df)
			spot=str(filtered_df.iloc[0]['spot'])
			tom=str(filtered_df.iloc[0]['tom'])
			print(spot)
			print(tom)
			print(tom)
		except:
			print("error")

		if date == "spot":
			mensaje = "Para el ISIN: " + isim + " y DATE: SPOT la posición es: " + str(spot)
			else:
		mensaje = "Para el ISIN: " + isim + " y DATE: TOM la posición es: " + str(tom)

		 #busca_isim(msg_message, date)
		print(isim, date, spot, tom)      
		print(mensaje)

		#        return(jsonify(isim=str(isim), date=str(date), spot=spot, tom=tom),200)
		return(jsonify(mensaje=mensaje),200)
	
	if __name__ == "__main__":
		context = ('/etc/ssl/certs/techhublabs.com.crt', '/etc/ssl/private/techhublabs.com.key')
		app.run(host='ec2-52-209-149-64.eu-west-1.compute.amazonaws.com', port=8080, ssl_context=context, threaded=True, debug=True)

























	