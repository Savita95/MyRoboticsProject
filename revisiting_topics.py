import logging
import random

import dialogue_delivery as dd
import sentiment_analyser as sa

logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def fn_revisiting_topics(track_Dict_list,test_content):
    current_unit_id = 0
    current_topic_id = 0
    current_paragraph_id = 0
    track_Dict_list_1 = []
    if len(track_Dict_list) > 0:
        # while len(track_Dict_list_1)>0:
        revisting_message = str(dd.is_not_blank(random.choice(dd.fn_get_validation_data("Revisiting_messages", dd.message_content)),
                                   dd.fn_get_validation_data("Revisiting_messages", dd.message_content)))
        print(revisting_message)
        for dictionary_id in track_Dict_list:
            revisiting_unit_id = dictionary_id.get("unit_id")
            revisiting_topic_id = dictionary_id.get("topic_id")
            revisiting_paragraph_id = dictionary_id.get("paragraph_id")
            #                 print(revisiting_unit_id,revisiting_topic_id,revisiting_paragraph_id)

            for no_of_units in test_content:
                #         print(no_of_units,"la1")
                if no_of_units.get("unit_id") == revisiting_unit_id:
                    Topic_list = no_of_units.get("topics")

                    for topics in Topic_list:
                        if topics.get("topic_id") == revisiting_topic_id:
                            #                     print(topics.get('topic_name'))
                            #                     print("Lets revisit the remaining topics")
                            #                     print(topics.get('contents'))
                            for contents in topics.get('contents'):
                                KEYWORD = contents.get("keywords")
                                if contents.get('paragraph_id') == revisiting_paragraph_id:
                                    print(str(contents.get('text').encode("utf-8")))

                                    i = 0
                                    while i < dd.REPs:
                                        response = input(dd.is_not_blank(random.choice(dd.fn_get_validation_data("ask_understanding", dd.message_content)),dd.fn_get_validation_data("validation_3",dd.message_content)).format(dd.is_not_blank(random.choice(KEYWORD),KEYWORD)))
                                        if sa.is_negative_response(response):
                                            i += 1
                                            if len(contents["text_alt"]) != 0:
                                                rand = str(dd.is_not_blank(random.choice(contents["text_alt"]),contents["text_alt"]))
                                                print(rand)
                                            else:
                                                if isinstance(contents.values(), str):
                                                    print(contents.values())

                                            if i == dd.REPs:
                                                rand = str(dd.is_not_blank(random.choice(dd.fn_get_validation_data("not_understood_move_on",dd.message_content)),dd.fn_get_validation_data("validation_1",dd.message_content)))
                                                print(rand)
                                                #                                               if no_of_units.items()=="Unit_id":
                                                Track_Dict = {"unit_id": current_unit_id, "topic_id": current_topic_id,
                                                              "paragraph_id": current_paragraph_id}
                                                track_Dict_list_1.append(Track_Dict)

                                        else:
                                            rand = str(dd.is_not_blank(random.choice(dd.fn_get_validation_data("understood_move_on", dd.message_content)),dd.fn_get_validation_data("validation_2", dd.message_content)))
                                            print(rand)
                                            i = dd.REPs
        print(len(track_Dict_list_1))

        if len(track_Dict_list_1) == 0:
            success_messages = str(dd.is_not_blank(random.choice(dd.fn_get_validation_data("success_messages", dd.message_content)),
                                dd.fn_get_validation_data("success_messages", dd.message_content)))

            print(success_messages)

    else:
        # success_messages = str(dd.fn_get_validation_data("success_messages", dd.message_content))
        success_messages=str(dd.is_not_blank(random.choice(dd.fn_get_validation_data("success_messages", dd.message_content)),
                            dd.fn_get_validation_data("success_messages", dd.message_content)))
        print(success_messages)


def main(test_content):
    track_Dict_list= dd.fn_get_content(test_content)
    Revisiting_messages = dd.fn_get_validation_data("Revisiting_messages", dd.message_content)
    # print(Revisiting_messages)
    # print(len(track_Dict_list))
    logging.info("Revisiting topics")
    fn_revisiting_topics(track_Dict_list, test_content)
    # print(Track_Dict_list,"Track_Dict_list")


if __name__ == '__main__':
    main(dd.test_content)


