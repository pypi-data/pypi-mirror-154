import nltk as __nltk
from nltk.stem import LancasterStemmer as __ls
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory as __indo_stemmer
from langdetect import detect as __ld
from googletrans import Translator as __tr

from . import lang

import picklepie as __pp

# dont forget to download nltk_data : nltk.download()
# downloaded to C:\Users\ahadi\AppData\Roaming\nltk_data -> massive file size

# Indonesian
# https://medium.com/@ksnugroho/dasar-text-preprocessing-dengan-python-a4fa52608ffe

# stemming English
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python

# twint
# https://stackoverflow.com/questions/66513554/python-twitter-scraper-without-using-api
# https://github.com/twintproject/twint
# install twint : pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# https://medium.com/@erika.dauria/scraping-tweets-off-twitter-with-twint-a7e9d78415bf

class __translated :
    text = None
    src = None
    dest = None
    pronounciation = None

def find (a_all_text='',a_text_to_find='') :
    loc_words = __nltk.tokenize.word_tokenize(a_all_text)
    loc_text = __nltk.Text(loc_words)
    loc_match = loc_text.concordance(a_text_to_find)
    return loc_match

def freq (a_word='') :
    loc_word = __pp.data.df_to_array(a_word,b_type='list',b_column='word')
    loc_freq = __nltk.probability.FreqDist(loc_word)
    return __pp.data.array_to_df(loc_freq.most_common(),['word','freq'])

def clean (a_text) :
    loc_text = a_text
    loc_text = loc_text.replace('\n',' ')
    loc_text = loc_text.replace('.','')
    loc_text = loc_text.replace(',','')
    # define punctuation
    loc_punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    # remove punctuation from the string
    loc_no_punct = ""
    for loc_char in loc_text:
        if loc_char not in loc_punctuations :
            loc_no_punct = loc_no_punct + loc_char
        else :
            loc_no_punct = loc_no_punct + ' '
    return loc_no_punct

def stem (a_sentence='',a_lang='English') :
    if (a_lang == 'Indonesian') :
        loc_factory = __indo_stemmer()        
        loc_stemmer = loc_factory.create_stemmer()
    elif (a_lang == 'English') :
        loc_factory = __ls()        
        loc_stemmer = loc_factory
    loc_return = loc_stemmer.stem(a_sentence)
    return loc_return

def stop_words (a_lang='English') :
    return set(__nltk.corpus.stopwords.words(a_lang))
    
def translate (a_text='',b_src='',b_dest='en') :
    loc_translator = __tr()
    if (b_dest != '') :
        loc_to = b_dest
    else :
        loc_to = 'en'
    if (b_src != '') :
        loc_lang = b_src
        loc_translated_ori = loc_translator.translate(a_text,src=loc_lang,dest=loc_to)
    else :
        loc_lang = __pp.ai.nlp.lang.detect(a_text)
        loc_translated_ori = loc_translator.translate(a_text,src=loc_lang.lang,dest=loc_to)
    loc_translated = __translated()
    loc_translated.text = loc_translated_ori.text
    loc_translated.src = loc_translated_ori.src
    loc_translated.dest = loc_translated_ori.dest
    loc_translated.pronounciation = loc_translated_ori.pronunciation
    return loc_translated
    
def word (a_text='',a_excl_stop_words=False,a_stop_words_lang='English') :
    loc_words = __nltk.tokenize.word_tokenize(a_text)
    if (a_excl_stop_words == False) :
        loc_return = loc_words
    else :
        loc_return = []
        for loc_word in loc_words :
            if loc_word not in __pp.ai.nlp.stop_words(a_stop_words_lang) :
                loc_return.append(loc_word)
    return __pp.data.array_to_df(loc_return,b_as_column=['word'])
    
    