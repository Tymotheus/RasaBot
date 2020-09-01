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


# This is a simple example for a custom action which utters "Hello World!"


from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

import logging
import json

# We use the medicare.gov database to find information about 3 different
# healthcare facility types, given a city name, zip code or facility ID
# the identifiers for each facility type is given by the medicare database
# xubh-q36u is for hospitals
# b27b-2uc7 is for nursing homes
# 9wzi-peqs is for home health agencies

logger = logging.getLogger(__name__)

class Give_Trivia(Action):
    """Action class allows to hear some random trivias"""

    def name(self):
        """Defining the name for the custom function to be used in stories"""
        return "give_trivia"

    def run(self, dispatcher, tracker, domain):
        print(tracker.get_slot("trivia_types"))
        #converting json format reply into python dictionary object
        request = json.loads(requests.get('https://opentdb.com/api.php?amount=1').text)
        print(request)
        trivia = request['results'][0]['question']
        answer = request['results'][0]['correct_answer']
        #dispatcher.utter_message(trivia + '\n \n' + answer)
        dispatcher.utter_message(trivia)
        dispatcher.utter_message(answer)
        return []
