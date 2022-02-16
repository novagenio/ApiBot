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
    date = re.findall(r"(tom|TOM|T/-|T/OPEN|T |t-|spot|spot/open|today|TODAY|SAMEDAY|SAME DAY|sameday|dame day|overnight|OVERNIGHT)", mensaje)
    return isin, date

@app.route("/person", methods=['POST', 'GET']) # aquí especificamos que estos endpoints aceptan solicitudes.

def handle_person(): 
    if request.method == 'POST': 
        msg_message = request.args.get('msg_message')
        msg_subj = request.args.get('msg_subj')
        mail_from = request.args.get('mail_from')
        print("-------------------------------------------------------")
        print(msg_message)
        print(msg_subj)

        mensaje, date = find_isin(msg_message, msg_subj)
        #-----------------------------------------------
        
        mensaje = list(set(mensaje))
        isim = str(mensaje)
        isim = re.sub("\[|\]|\'","",isim)
        if len(mensaje) == 1:
            date = date[0]
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
            if len(mensaje)>= 1:
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
            if date in ["spot","spot/open","SPOT","S ","s-","s "]:
                mensaje = "Para el ISIN: " + isim + " y DATE: SPOT la posición es: " + str(spot)
            if date in ["tom","TOM", "TOM/OPEN", "TOM","T/OPEN","t-","T/-","T "]:
                mensaje = "Para el ISIN: " + isim + " y DATE: TOM la posición es: " + str(tom)
            if date in ["overnight","SAMEDAY","today","out of today","TODAY","SAME DAY","sameday","same day","OVERNIGHT"]:
                mensaje = "Para el ISIN: " + isim + " y DATE: Overnight la posición es: " + str(overnight)
            output = mensaje
          #  return(mensaje)   

        if len(mensaje) >= 1:
            print("mensaje mayor 1")
            output = []
            for i,element in enumerate(mensaje) :
                print("for mensajes date", date[i])
                if date[i] in ["spot","spot/open","SPOT","S ","s-","s "]:
                    mensaje = "Para el ISIN: " + element + " y DATE: SPOT la posición es: " + str(position[i][0])
                if date[i] in ["tom","TOM", "TOM/OPEN", "TOM","T/OPEN","t-","T/-","T "]:
                    mensaje = "Para el ISIN: " + element + " y DATE: TOM la posición es: " + str(position[i][1])
                if date[i] in ["overnight","SAMEDAY","today","out of today","TODAY","SAME DAY","sameday","same day","OVERNIGHT"]:
                    mensaje = "Para el ISIN: " + element + " y DATE: Overnight la posición es: " + str(position[i][2])  
                output.append(mensaje)
           # return(output)

        return(jsonify(mail_from=mail_from, mensaje=output),200)

# SANDBOX API

if __name__ == "__main__":
    #context = ('/etc/ssl/certs/techhublabs.com.crt', '/etc/ssl/private/techhublabs.com.key')
    app.run(host='bvmnglapsboxp01.nngg.corp', port=8081, threaded=True, debug=True)
    
    
# AWS API    
'''    
if __name__ == "__main__":
    context = ('/etc/ssl/certs/techhublabs.com.crt', '/etc/ssl/private/techhublabs.com.key')
    app.run(host='ec2-52-209-149-64.eu-west-1.compute.amazonaws.com', port=8081, ssl_context=context, threaded=True, debug=True)
'''