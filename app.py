
from asyncio.windows_events import NULL
from urllib import response
from flask import Flask,render_template,request,jsonify
from chat import *
import cv2
from AVrecordeR import *
from SER import *
from test import *
from EYE import *
from FER import *
from volume_meter import *
from multiprocessing import process
import threading

app = Flask(__name__, static_folder='static')


qs_dict={}

background_scripts = {}
@app.get("/")
def indext_get():
    return render_template("index.html")

@app.route("/predict", methods = ['POST'])
def predict ():
    text = request.get_json().get("message")
    response = get_response(text)  
    print(response,"predict")
    message ={"answer":response}
    return jsonify(message) 

@app.route("/post_interview", methods = ['POST'])
def chat_reply():
    response = get_response("results")
    print(response)
    message ={"answer":response}
    return jsonify(message)

@app.route("/session_qs", methods = ['POST'] )
def get_js():
    global qs_dict
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    qs_dict = json.loads(output) #this converts the json output to a python dictionary
    print(qs_dict) # Printing the new dictionary
    print(type(qs_dict))#this shows the json converted as a python dictionary
    return qs_dict

@app.route('/session')
def videos_get():
    return render_template("videos (2).html")

p1 = SER(path='SER_model.h5')
@app.route("/speech", methods=['POST'])   
def speech():
    global p1
    p1 = SER(path='SER_model.h5')
    p1.load_model() 
    print("before ser")
    q = request.get_json()
    print("current question is:",q)
    p1.analyse_speech(q)
    print("After ser")
    return ('/')    
 
@app.route("/stop_speech") 
def stop_speech():
    global p1
    print("before stop ser")
    p1.stop()
    print("After stop ser")
    return ('/')

cap = cv2.VideoCapture(0)
sit = Posture(cap)
@app.route("/sit_posture")
def start_posture():
    print("before post")
    sit.startPost()
    print("After ser")
    return ('/')

@app.route("/stop_posture")
def stop_posture():
    print("before stop post")
    sit.stopPost()
    print("after stop post")
    print("stoppingPost")
    return ('/')
    
eye = EYE(cap) 
@app.route("/start_eye")
def start_eye():
    global eye
    eye = EYE(cap) 
    eye.gaze_blinking_function()
    return ('/')


@app.route("/stop_eye")
def stop_eye():
    print("before stop eye")
    eye.stop()
    print("after stop eye")
    return ('/')

    
f1 = FER(cap)

@app.route("/start_fer", methods=['POST'])
def start_fer():
    global f1
    f1=FER(cap)
    f1.load_model()
    q = request.get_json()
    f1.analyse_face(q)
    return ('/')

@app.route("/stop_fer")
def stop_fer():
    f1.stop_facial()
    print("stoppingFER")
    return ('/')


@app.route("/video")   
def record():
    file_manager("hh")
    print("before av")
    start_AVrecording("hh",cap) 
    print("after av")
    return ('/')

@app.route("/video_stop")  
def stop_record():
    print("stop av b4")
    stop_AVrecording("hh")
    print("avDone")
    return ('/')


@app.route("/volume_meter")
def measure_v():
    print("involume")
    vm = volume_meter("temp_audio.wav")#path of current user db excel n7ot video report w audio
    vm.volume()
    return ('/')


if __name__ == '__main__':
    app.run(debug=True)
    print(qs_dict)
