# from flask import Flask, render_template
from flask import Flask, redirect, url_for, request ,render_template
import Conversation_starter as cs
import logging
import json
logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__) 

@app.route('/base',methods = ['POST', 'GET'])
def talk():
    u_unit=int(request.form['u_unit'])
    u_topic=int(request.form['u_topic'])
    u_paragraph=int(request.form['u_paragraph'])
    u_progress=[u_unit,u_topic,u_paragraph]
    times=int(request.form['times'])
    u_input = request.form['user_input']
    logging.info("entering system turn")
    output,times,u_progress,emotracker,emotracker2=cs.system_turn(u_input,u_progress,times) 
    if cs.isFinish(u_input):
        output="Thanks"
    return render_template('result.html',message=output,unit=u_progress[0],topic=u_progress[1],paragraph=u_progress[2],times=times)
    
  
@app.route('/api',methods = ['POST', 'GET'])
def talk_info():
    u_unit=int(request.form['u_unit'])
    u_topic=int(request.form['u_topic'])
    u_paragraph=int(request.form['u_paragraph'])
    u_progress=[u_unit,u_topic,u_paragraph]
    times=int(request.form['times'])
    val_but=int(request.form['val_but'])
    u_input = request.form['user_input']
    output,times,u_progress,emotracker,emotracker2=cs.system_turn(u_input,u_progress,times) 
    if cs.isFinish(u_input):
        output="Thanks"
    return render_template('example.html',message={"output":output,"u_progress":u_progress,"times":times,"val_but":val_but,"emotracker":emotracker,"u_input":u_input,"emotracker2":emotracker2})
  


if __name__ == '__main__': 
    app.run(debug = True) 

