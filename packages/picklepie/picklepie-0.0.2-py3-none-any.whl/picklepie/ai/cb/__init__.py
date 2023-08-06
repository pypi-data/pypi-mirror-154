from chatterbot import ChatBot as __cb
from chatterbot.trainers import ListTrainer as __lt
from chatterbot.trainers import ChatterBotCorpusTrainer as __cp
import picklepie as __pp

# https://chatterbot.readthedocs.io/en/stable/examples.html
# https://github.com/gunthercox/ChatterBot/tree/master/examples
# https://chatterbot.readthedocs.io/en/stable/training.html
# https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data

# IF ERROR : AttributeError: module 'time' has no attribute 'clock'
# Open : C:\Users\ahadi\AppData\Local\Programs\Python\Python39\Lib\site-packages\sqlalchemy\util\compat.py
# line 264
'''
if win32 or jython:
    try :
        time_func = time.perf_counter() # change to this
    except AttributeError :
        time_func = time.clock # this causes error in python 3
else:
    time_func = time.time
'''

# train with YAML file : https://programmersought.com/article/23532685360/
# https://github.com/gunthercox/chatterbot-corpus/blob/master/chatterbot_corpus/data/english/conversations.yml
# https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data

def chat (a_ask='') :
    # create a new chatbot
    loc_chatbot = __cb(
        'Pickleku'
        , read_only = True
        , storage_adapter='chatterbot.storage.SQLStorageAdapter'
        , database_uri='sqlite:///pickleku.sqlite3'
        , logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation'
            ,
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am sorry, but I do not understand.',
                    'maximum_similarity_threshold': 0.90
                }
            , 'chatterbot.logic.TimeLogicAdapter'
        ]
    )
    # train
    loc_trainer = __cp(loc_chatbot)
    loc_trainer.train = ("./pickleku.yml")
    # get a response
    loc_response = loc_chatbot.get_response(a_ask)
    return loc_response
    # use : print(loc_response) : to show the response
