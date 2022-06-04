
from asyncio.windows_events import NULL
from urllib import response
from flask import Flask,render_template,request,jsonify, session, redirect, url_for
from requests import Session
from chat import *
import cv2
from AVrecordeR import *
from SER import *
from test import *
from EYE import *
from FER import *
from volume_meter import *
from finalReport import *
import os
from flask_session import Session

app = Flask(__name__, static_folder='static')
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)


qs_dict={}
QS_TEXT ={
          "q1": "Are you applying for other jobs also?",
          "q2": "Describe 3 things that are most important to you in a job.",
          "q3": "Describe your self in one word.",
          "q4": "Do you consider yourself successful and why?",
          "q5": "How do you deal with an angry customer?",
          "q6": "How do you deal with pressure or stressful situations?",
          "q7": "Tell me about yourself?",
          "q8": "What are your achievments in life?",
          "q9": "What are your career goals?",
          "q10": "What are your greatest stengths?",
          "q11": "What are your salary expectations?",
          "q12": "What do you consider to be your weaknesses?",
          "q13": "What does success mean to you?",
          "q14": "What is more important to you the mony or the work?",
          "q15": "What makes you angry?",
          "q16": "What was the most difficult decision you have made in your past life?",
          "q17": "Where do you see yourself in 5 years?",
          "q18": "Why are you the best person for this job?",
          "q19": "Why do you want this job?",
          "q20": "Why do you want to work at this company?",
          "q21": "Whould you like to work over time, bla bka?",
            }
background_scripts = {}
cap = cv2.VideoCapture(0)
f1 = FER(cap)
p1 = SER(path='SER_model.h5')
sit = Posture(cap)
eye = EYE(cap) 
qa=""
id = 10
parent_dir = "D:/hana/asu/spring2022/gp2/integrated/Interview_detection_project-master/"


@app.route("/")
def indext_get():
    directory =str(id)
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(directory):
        os.mkdir(path)
    return render_template("index.html")

@app.route('/session')
def videos_get():
    global id
    session['uid'] = str(id)
    id+=1
    return render_template("videos (2).html")

@app.route("/start_posture",methods = ['GET'])
def detect_slouch():
    #sit.startPost(session['uid'])
    if "uid" in session:
        print("tmam")
        folder = session['uid']
    sit.startPost(folder)
    return ('/')

@app.route("/start_eye",methods = ['GET'])
def start_eye():
    eye.gaze_blinking_function()


@app.route("/start_record",methods = ['GET'])
def start_record():
    folder=session['uid']
    file_manager(folder)
    start_AVrecording(folder,cap)
    return ('/')

@app.route("/stop_record",methods = ['GET'])
def stop_record():
    #stop_AVrecording(session['uid'])
    stop_AVrecording(session['uid'])
    return ('/')

@app.route("/stop_posture",methods = ['GET'])
def stop_posture():
    sit.stopPost()
    return ('/')

@app.route("/stop_eye",methods = ['GET'])
def stop_eye():
    eye.stop()
    return ('/')

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
    qs_dict = json.loads(output) #this converts the json output to a python dictionary
    #5leena hena n compute kol so2al q eih text
    session['q0'] = QS_TEXT[qs_dict['0']]
    print(session['q0'])
    session['q1'] = QS_TEXT[qs_dict['1']]
    print(session['q1'])
    session['q2'] = QS_TEXT[qs_dict['2']]
    print(session['q2'])
    session['q3'] = QS_TEXT[qs_dict['3']]
    print(session['q3'])
    session['q4'] = QS_TEXT[qs_dict['4']]
    print(session['q4'])
    return qs_dict

@app.route("/speech", methods=['POST'])   
def speech():
    global p1
    p1 = SER(path='SER_model.h5')
    q = request.get_json()
    p1.analyse_speech(q,session['uid'])
    return ('/')    
 
@app.route("/stop_speech",methods = ['GET']) 
def stop_speech():
    global p1
    p1.stop()
    return ('/')

@app.route("/start_fer", methods=['POST'])
def start_fer():
    global f1
    f1=FER(cap)
    f1.load_model()
    q = request.get_json()
    f1.analyse_face(q,session['uid'])
    return ('/')

@app.route("/stop_fer",methods = ['GET'])
def stop_fer():
    global qs
    f1.stop_facial()
    return ('/')

@app.route("/report")
def get_res():
    print("inreport")
    #I think el sa7 aktr tb2a goa kol fnc stop/qs
    session['contact']=res['eye contact']
    session['mins'] = res['session time']/60
    session['blinks'] = res['blinks']
    session['slouch'] = count
    q2r ={'q0':session['q0'],'q1':session['q1'],'q2':session['q2'],'q3':session['q3'],'q4':session['q4']}
    write_results(qs_dict,session['uid'],session['contact'],session['mins'],session['blinks'] ,session['slouch'])
    cap.release()
    return ('/')

@app.route("/content",methods=['POST'])
def s2t():
    global qa
    qa = request.get_json()
    print("speechis"+qa)
    return ('/')

if __name__ == '__main__':
    app.run(debug=True)

