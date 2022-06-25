from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from application.settings.dev import DevelopmentConfig
from application.settings.prop import  ProductionConfig
from application import app,socketio
# from application import mqtt_client
from application import topic


# @app.route('/accounts', methods=['GET'])
# def get_accounts():
#
#     if request.method == "GET":
#
#         username = request.args.get("account")
#         password = "aaa" #query_account(username)
#         if password == "":
#             return "no result"
#         else:
#             #return render_template("home.html",message=username,password=password)
#             return jsonify({"password": password})

if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000)
    socketio.run(app, host='http://127.0.0.1', port=8080, use_reloader=True, debug=True,cors_allowed_origins="*")
