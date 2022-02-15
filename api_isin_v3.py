from flask import Flask, request, Response, jsonify, json
import time


import extract_msg
import re
import pandas as pd

app = Flask(__name__)



def find_isin(msg_message, msg_subj):
    msg_message = msg_message
    msg_subj = msg_subj
    mensaje = msg_subj +' '+ msg_message
    isin = re.findall('[A-Z]{2}[A-Z0-9]{9}[0-9]', mensaje)
    date = re.findall(r"(tom|TOM|T/-|spot|spot/open|today|TODAY|SAMEDAY|SAME DAY|overnight|OVERNIGHT)", mensaje)
    return isin, date

@app.route("/person", methods=['POST', 'GET']) # aquí especificamos que estos endpoints aceptan solicitudes.

def handle_person(): 
    if request.method == 'POST': 
        msg_message = request.args.get('msg_message')
        msg_subj = request.args.get('msg_subj')
        mail_from = request.args.get('mail_from')
        print(msg_message)
        print(msg_subj)

        mensaje, date = find_isin(msg_message, msg_subj)
        print(type(mensaje),type(date))
        isim = str(mensaje)
        isim = re.sub("\[|\]|\'","",isim)
        if len(mensaje) == 1:
            date = str(date)
            date = re.sub("\[|\]|\'","",date)
        if len(mensaje) >= 1:
            pass

        spot=0
        tom=0
        overnight = 0
        position = []
        print("isim, date despues del corte", isim, date)
        df = pd.read_csv("bot2.csv",sep = ';')
        try:
            if len(mensaje)== 1: 
                df_mask=df['seccode']==isim
                filtered_df = df[df_mask]
                print(filtered_df)
                spot=str(filtered_df.iloc[0]['spot'])
                tom=str(filtered_df.iloc[0]['tom'])
                overnight=str(filtered_df.iloc[0]['overnight'])
                position.append([spot,tom,overnight])
                print(spot)
                print(tom)
            if len(mensaje)> 1:
                position = []
                for element in mensaje:
                    try:
                        df_mask=df['seccode']== element
                        filtered_df = df[df_mask]
                        print(filtered_df)
                        spot=str(filtered_df.iloc[0]['spot'])
                        tom=str(filtered_df.iloc[0]['tom'])
                        overnight=str(filtered_df.iloc[0]['overnight'])
                        print(spot)
                        print(tom)
                        position.append([spot,tom,overnight])
                    except:
                        print("No encontrado")
                        position.append(["No encontrado","No encontrado","No encontrado"])
            print("position :", position)

        except Exception as e: 
            print(e)
            print("No encontrado")

        if len(mensaje)== 1:
            print("1 mensaje", date)        
            if date == "spot":
                output = "Para el ISIN: " + isim + " y DATE: SPOT la posición es: " + str(spot)
            if date in ["tom", "TOM/OPEN", "TOM"]:
                output = "Para el ISIN: " + isim + " y DATE: TOM la posición es: " + str(tom)
            if ((date == "overnight") | (date == "SAMEDAY") | (date == "today") | (date == "out of today")):
                output = "Para el ISIN: " + isim + " y DATE: Overnight la posición es: " + str(overnight)
            #return(output)   

        if len(mensaje) > 1:
            print("mensaje mayor 1")
            output = []
            for i,element in enumerate(mensaje) :
                print("for mensajes date", date[i])
                if date[i] == "spot":
                    mensaje = "Para el ISIN: " + element + " y DATE: SPOT la posición es: " + str(position[i][0])
                if date[i] in ["tom", "TOM/OPEN", "TOM"]:
                    mensaje = "Para el ISIN: " + element + " y DATE: TOM la posición es: " + str(position[i][1])
                if ((date[i] == "overnight") | (date[i] == "SAMEDAY") | (date[i] == "today") | (date[i] == "out of today")| (date[i] == "TODAY")):
                    mensaje = "Para el ISIN: " + element + " y DATE: Overnight la posición es: " + str(position[i][2])  
                output.append(mensaje)
            #return(output)

#        return(jsonify(isim=str(isim), date=str(date), spot=spot, tom=tom),200)
        return(jsonify(mail_from=mail_from, mensaje=output),200)


if __name__ == "__main__":
    #context = ('/etc/ssl/certs/techhublabs.com.crt', '/etc/ssl/private/techhublabs.com.key')
    app.run(host='bvmnglapsboxp01.nngg.corp', port=8081, threaded=True, debug=True)