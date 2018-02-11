import en_core_web_sm
import spacy
nlp = en_core_web_sm.load()
for i in range(100):
    doc = nlp(u'print the words i am a human')
