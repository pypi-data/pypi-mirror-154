from langdetect import detect as __ld

import picklepie as __pp

class __detect_lang :
    lang = None
    desc = None

def desc (a_lang='') :
    loc_dict = __pp.ai.nlp.lang.dict_()
    loc_data = __pp.data.row.value(loc_dict,'code',a_lang)
    if (len(loc_data) >= 1) :
        loc_desc = __pp.data.cell_value(loc_data,0,'desc')
    else :
        loc_desc = ''
    return loc_desc

def detect (a_text='') :
    loc_lang = __ld(a_text)
    loc_dict = __pp.ai.nlp.lang.dict_()
    loc_df = __pp.data.array_to_df(loc_dict,['code','desc'])
    loc_data = __pp.data.row.value(loc_df,'code',loc_lang)
    if (len(loc_data) >= 1) :
        loc_desc = __pp.data.cell_value(loc_data,0,'desc')
    else :
        loc_desc = ''
    loc_detect_lang = __detect_lang()
    loc_detect_lang.lang = loc_lang
    loc_detect_lang.desc = loc_desc
    return loc_detect_lang

def dict_ () :
    loc_dict = [('af','Afrikaans'),('ar','Arabic'),('bg','Bulgarian'),('bn','Bengali'),('ca','Catalan, Valencian'),('cs','Czech'),('cy','Welsh'),('da','Danish'),('de','German'),('el','Greek, Modern'),('en','English'),('es','Spanish, Castilian'),('et','Estonian'),('fa','Persian'),('fi','Finnish'),('fr','French'),('gu','Gujarati'),('he','Hebrew'),('hi','Hindi'),('hr','Croatian'),('hu','Hungarian'),('id','Indonesian'),('it','Italian'),('ja','Japanese'),('kn','Kannada'),('ko','Korean'),('lt','Lithuanian'),('lv','Latvian'),('mk','Macedonian'),('ml','Malayalam'),('mr','Marathi'),('ne','Nepali'),('nl','Dutch, Flemish'),('no','Norwegian'),('pa','Punjabi, Panjabi'),('pl','Polish'),('pt','Portuguese'),('ro','Romanian, Moldavian, Moldovan'),('ru','Russian'),('sk','Slovak'),('sl','Slovenian'),('so','Somali'),('sq','Albanian'),('sv','Swedish'),('sw','Swahili'),('ta','Tamil'),('te','Telugu'),('th','Thai'),('tl','Tagalog'),('tr','Turkish'),('uk','Ukrainian'),('ur','Urdu'),('vi','Vietnamese'),('zh-cn','Chinese'),('zh-tw','Chinese')]
    return __pp.data.array_to_df(loc_dict,b_as_column=['code','desc'])

def lang (a_desc='') :
    loc_dict = __pp.ai.nlp.lang.dict_()
    loc_data = __pp.data.row.value(loc_dict,'desc',a_desc)
    if (len(loc_data) >= 1) :
        loc_code = __pp.data.cell_value(loc_data,0,'code')
    else :
        loc_code = ''
    return loc_code



