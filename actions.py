# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

import logging
import json
import random


logger = logging.getLogger(__name__)

class Give_Trivia(Action):
    """Action class allows to hear some random trivias"""

    def name(self):
        """Defining the name for the custom function to be used in stories"""
        return "give_trivia"

    def run(self, dispatcher, tracker, domain):
    
        #converting json format reply into python dictionary object
        request = json.loads(requests.get('https://opentdb.com/api.php?amount=1').text)
        print(request)
        trivia = request['results'][0]['question']
        #converting unconverted apostrophes, ampersands, quotation marks
        trivia = (((trivia.replace("&quot;", '"')).replace("&amp", "&")).replace("&#039;","'")).replace("&eacute;", "é")
        correct_answer = request['results'][0]['correct_answer']
        correct_answer = (((correct_answer.replace("&quot;", '"')).replace("&amp", "&")).replace("&#039;","'")).replace("&eacute;", "é")
        #getting a list of all possible answers and randomizing it
        all_answers = request['results'][0]['incorrect_answers']
        for answ in all_answers:
            answ = (((answ.replace("&quot;", '"')).replace("&amp", "&")).replace("&#039;","'")).replace("&eacute;", "é")
        all_answers.append(correct_answer)
        random.shuffle(all_answers)

        buttons = []
        for answ in all_answers:
            #2 potential solutions: 1) intent \correct_asnwer and \incorrect_answer
            # and reactions to them 2) answer with setting slots of user answer and then comparing it to correct one

            if answ == correct_answer:
                intent = '/answer_correct'
            else :
                intent = '/answer_incorrect'

            #intent = '/answer{"user_answer":"' + answ + '"}'

            buttons.append(

                {"title": "{}".format(answ),
                "payload": "{}".format(intent)
                }
            )

        #dispatcher.utter_button_template(trivia, buttons, tracker)
        dispatcher.utter_message(trivia)
        dispatcher.utter_message(buttons = buttons)
        print(all_answers)
        return [SlotSet("correct_answer","{}".format(correct_answer))]
        #return []

class Correct_Answer:

    def name(self):
        return "answer_correct_react"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("You answered correctly, great!")
        return []


class Incorrect_Answer:

    def name(self):
        return "answer_incorrect_react"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("You answered incorrectly, sorry.")
        return []

class Give_Type(Action):

    def name(self):
        return "give_type"

    def run(self, dispatcher, tracker, domain):
        print(tracker.get_slot("trivia_type"))
        return []

class Verify_Answer(Action):
    """Function verifying user's answer, comparing it to the correct one and
    adding one point to score if it is the correct one """
    def name(self):
        return "verify_answer"

    def run(self, dispatcher, tracker, domain):
        print("Users last message was: {}".format(tracker.latest_message.get("text") ) )
        print("Correct answer is: {}".format(tracker.get_slot("correct_answer")))
        if ( tracker.get_slot("correct_answer") == tracker.get_slot("user_answer") ):
            print("Answer Correct! :)")
        else:
            print("Answer Incorrect :(")
        return[]

class Button_Test(Action):

    def name(self):
        return "button_test"

    def run(self, dispatcher, tracker, domain):
        buttons = []
        buttons.append(
            {"title": "{}".format("Bye Button"),
             "payload": "/goodbye"})
        buttons.append(
            {"title": "{}".format("Thanks Button"),
             "payload": "/thanks"}
        )

        dispatcher.utter_button_template("utter_greet", buttons, tracker)
        return []

