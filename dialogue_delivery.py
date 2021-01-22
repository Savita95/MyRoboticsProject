import json
import random
import sentiment_analyser as sa
import logging
logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def fn_get_validation_data (keyName,message_content):
    for keys, values in message_content.items():
        if keys==keyName:
            return values


def is_not_blank(string,myStrings):
    while string=="":
        string=random.choice(myStrings)
    return string



def fn_load_json_file(filename=str):
    with open(filename, "r",encoding="utf8") as f:
        content = json.load(f)
    return content
test_content=fn_load_json_file("bc_content_version2.json")
message_content=fn_load_json_file("message.json")

#
REPs=3
Track_Dict={}
Track_Dict_list=[]




def fn_get_content(test_content):
    current_unit_id = 0
    current_topic_id = 0
    current_paragraph_id = 0
    track_Dict_list=[]
    # KEYWORD=[]

    for no_of_units in test_content:
        current_unit_id=no_of_units.get("unit_id")
        topics=no_of_units.get("topics")
        logging.info("%d current_unit_id ", current_unit_id)
        for topics_elements in topics:
            current_topic_id=topics_elements.get("topic_id")
            contents=topics_elements.get("contents")
            for contents_elements in  contents:
                KEYWORD=contents_elements.get("keywords")
                current_paragraph_id=contents_elements.get("paragraph_id")
                text=str(contents_elements.get("text"))
                print(text,"text")
                i=0
                while i < REPs:
                    response = input(is_not_blank(random.choice(fn_get_validation_data("ask_understanding", message_content)),fn_get_validation_data("validation_3", message_content)).format(is_not_blank(random.choice(KEYWORD),KEYWORD)))
                    if sa.is_negative_response(response):
                        i += 1
                        if len(contents_elements["text_alt"]) != 0:
                            rand = str(is_not_blank(random.choice(contents_elements["text_alt"]),contents_elements["text_alt"]))
                            print(rand)
                        else:
                            logging.info("inside else")
                            print(text)

                        if i == REPs:
                            rand = str(is_not_blank(random.choice(fn_get_validation_data("not_understood_move_on", message_content)),fn_get_validation_data("validation_1", message_content)))
                            print(rand)
                            
                            Track_Dict = {"unit_id": current_unit_id, "topic_id": current_topic_id,
                                          "paragraph_id": current_paragraph_id}
                            track_Dict_list.append(Track_Dict)
                            logging.info("integrating track_dict_list")



                    else:
                        rand = is_not_blank(random.choice(fn_get_validation_data("understood_move_on", message_content)),fn_get_validation_data("validation_2", message_content))
                        print(rand)
                        i = REPs
        logging.info("Track_Dict_list %s", track_Dict_list)
        return track_Dict_list


# def fn_start_conversation


# fn_get_content(test_content)
