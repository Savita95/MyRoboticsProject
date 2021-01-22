import dialogue_delivery as dd
import random
import sentiment_analyser as sa
import numpy as np
import logging
logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


bc_content=dd.fn_load_json_file('bc_content_version2.json')
message=dd.fn_load_json_file('message.json')
conversation_progress_tracker={"unit_id":1,"topic_id":1,"paragraph_id":1}
THRESHOLD=3
times=0
ERROR={"error_code":1}
SUCCESS=1
TOPIC_NOT_PRESENT=2
UNIT_NOT_PRESENT=3
END_OF_UNITS=4

def get_next_unit(unit_id,topic_id,paragraph_id):
    topic_id=1
    paragraph_id=1
    return [unit_id+1,topic_id,paragraph_id]

def change_unit_id(u_progress):
    unit_id=u_progress[0]
    topic_id=1
    paragraph_id=1
    if any(unit["unit_id"] == unit_id for unit in bc_content):
        for unit in bc_content:
            if unit["unit_id"]==unit_id:
                for topic in unit["topics"]:
                    if topic["topic_id"]==topic_id:
                        topic_id=topic["topic_id"]
                        for paragraph in topic["contents"]:
                            if paragraph["paragraph_id"]==paragraph_id:
                                return (SUCCESS,paragraph)
    else:
        return (4,{})

def change_topic_id(u_progress):
    unit_id=u_progress[0]
    topic_id=u_progress[1]
    paragraph_id=1
    for unit in bc_content:
        if unit["unit_id"]==unit_id:
            if any(topic["topic_id"] == topic_id for topic in unit["topics"]):
                for topic in unit["topics"]:
                    if topic["topic_id"]==topic_id:
                        for paragraph in topic["contents"]:
                            if paragraph["paragraph_id"]==paragraph_id:
                                return (SUCCESS,paragraph)
            else:
                return (UNIT_NOT_PRESENT,{})

def get_next_topic(unit_id,topic_id,paragraph_id):
    paragraph_id=1
    return [unit_id,topic_id+1,paragraph_id]

def get_paragraph(unit_id,topic_id,paragraph_id):
    for unit in bc_content:  
        if unit["unit_id"]==unit_id:
            for topic in unit["topics"]:
                if topic["topic_id"]==topic_id:
                    if any(paragraph["paragraph_id"] == paragraph_id for paragraph in topic["contents"]):
                        for paragraph in topic["contents"]:
                            if paragraph["paragraph_id"]==paragraph_id:
                                return (SUCCESS,paragraph)
                    else:
                        return (TOPIC_NOT_PRESENT,{})
                        





def listen(u_progress):
    return input(""),u_progress

def say(output,u_progress):
    print(output)

def get_alt_text(paragraph):
    if len(paragraph["text_alt"])!=0:
        return random.choice(paragraph["text_alt"])
    else:
        return paragraph["text"]


def select_text(paragraph,times,user_understood):
    if user_understood:
        if len(paragraph)!=0:
            return paragraph["text"]
        else: return None
    elif (times<THRESHOLD):
        return get_alt_text(paragraph)
    else:
        return "Lets get back to it later"


def get_understand_msg(paragraph):
    keywords=paragraph["keywords"]
    get_understandmsg=random.choice(dd.fn_get_validation_data("ask_understanding",message)).format(random.choice(keywords))
    return get_understandmsg





def get_text(unit_id,topic_id,paragraph_id,times,user_understood):
    error,paragraph=get_paragraph(unit_id,topic_id,paragraph_id)
    errorchange=0
    if error==TOPIC_NOT_PRESENT:
        errorchange,paragraph=change_topic_id(get_next_topic(unit_id,topic_id,paragraph_id))
    if error==UNIT_NOT_PRESENT or errorchange==UNIT_NOT_PRESENT:
        error=errorchange
        u_progress=get_next_unit(unit_id,topic_id,paragraph_id)
        errorchange,paragraph=change_unit_id(u_progress)
    if errorchange==END_OF_UNITS:
        return errorchange,random.choice(dd.fn_get_validation_data("success_messages",message))                        
    text=select_text(paragraph,times,user_understood)
    text+=get_understand_msg(paragraph)
    return error,text

def get_moveOn_msg():
    get_moveOnMsg=random.choice(dd.fn_get_validation_data("not_understood_move_on",message))
    return get_moveOnMsg


def get_next_id_set(unit_id,topic_id,paragraph_id,error):
    next_id_set=[unit_id,topic_id,paragraph_id+1]
    if error==2:
        next_id_set=get_next_topic(unit_id,topic_id,paragraph_id)
    elif error==3:
        next_id_set=get_next_unit(unit_id,topic_id,paragraph_id)
    elif error==4:
        next_id_set=[]
    return next_id_set

def isFinish(u_input):
    return u_input=="Bye"
    

def did_understand(u_input):
#    print(u_input)
    Bool,val=sa.is_negative_response(u_input)
#    print(Bool,val)
    if Bool: 
        return False,val
    else: 
        return True,val 
def system_turn(u_input,u_progress,times=1):
    unit_id=u_progress[0]
    topic_id=u_progress[1]
    paragraph_id=u_progress[2]
    user_understood,val=did_understand(u_input)
    if user_understood:
        next_id_set=get_next_id_set(unit_id,topic_id,paragraph_id,0)
        error,msg=get_text(next_id_set[0],next_id_set[1],next_id_set[2],times,user_understood)
        next_id_set=get_next_id_set(unit_id,topic_id,paragraph_id,error)
        return (msg,times,next_id_set,1,val)
    elif (times<THRESHOLD):
        error,msg=get_text(unit_id,topic_id,paragraph_id,times,user_understood)
        times+=1
        return (msg,times,u_progress,2,val)
    else:
        msg=get_moveOn_msg()
        next_id_set=get_next_id_set(unit_id,topic_id,paragraph_id,0)
        return (msg,0,next_id_set,3,val)
       

def main ():
    u_progress=[1,1,1]
    u_input=""
    finish=False
    times=0
    while(not finish):
        output,times,u_progress,emotracker,emotracker1=system_turn(u_input,u_progress,times)
        print(emotracker,emotracker1,"emotracker,emotracker1")
        say(output,u_progress)
        if len(u_progress)<=0:
            break
        u_input,u_progress=listen(u_progress)
        finish=isFinish(u_input)
            


if __name__=="__main__":
    main()









