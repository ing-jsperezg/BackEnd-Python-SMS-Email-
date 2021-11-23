# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:51:31 2021

@author: jsper
"""

"""      DEFINICION PARA LA APLICACION DE PYTHON"""

from flask import Flask
import os
from twilio.rest import Client
from flask import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def inicio():
    test = os.environ.get("Test")
    return test
 
@app.route("/sms")
def sms():
   try:  
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        contenido = request.args.get("mensaje")
        destino = request.args.get("telefono")
        message = client.messages \
                        .create(
                             body=contenido,
                             from_="+12312725730",
                             to="+57" + destino
                         )
                        
        print(message.sid)
        return "Mensaje enviado correctamente desde TWILIO...."
   except Exception as e:
      
       return "Error enviando el mensje.... "+e
       
   
@app.route("/sendEmail")
def email():
    
    destino = request.args.get("correoDestino")
    asunto = request.args.get("asunto")
    mensaje = request.args.get("contenido")
    
    message = Mail(
    from_email='jp.sendgrid@gmail.com',
    to_emails=destino,
    subject=asunto,
    html_content=mensaje)
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        
        return "<h1>Correo Electronico enviado correctamente desde SENDGRID</h1>"
    except Exception as e:
      
        return "<h1>Error enviando el correo...</h1> "
    
if __name__ == '__main__':
    app.run()