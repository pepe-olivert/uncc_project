# %% READING THE DATA

print('Importing the modules and reading the evidence data...')
import pandas as pd
import pickle
from  preprocessing.evidenceselection import *
import pandas as pd
import numpy as np
evidence_sentences = pd.read_csv('/home/vant/Documentos/mySpace/fun/chatbot/datasets/evidence_sentences.csv').drop(['Unnamed: 0'], axis = 1)
evidence_sentences = evidence_sentences['evidence_sentences'].values
embedding_evidences = pd.read_csv('/home/vant/Documentos/mySpace/fun/chatbot/datasets/embedding_evidences.csv').drop(['Unnamed: 0'], axis = 1)
embedding_evidences = np.array(embedding_evidences)

import matplotlib.pyplot as plt
import pickle
from preprocessing.inference_fake_def3 import inference_claims
"""

This code will be for the chatbot2.0 using the inference_fake.py script with a model more accurate than the one we are using right now.



"""



#%%

"""
We will try to build a "chatbot". We will create an interface where you can ask questions and you will 
recieve an answer.

As we are working on the Nigeria Elections our "bot" will recieve only questions about that specific topic
and will answer if that sentence or claim given by the user is false, true or unproven.

Further more we will try to give a summary given the label and the claim. Why is it labeled like this?


"""
# FIRST STEP WE LOAD THE MODEL

print('\nLoading the models...\n')

with open('/home/vant/Documentos/mySpace/fun/chatbot/models/vectorizer.pkl', 'rb') as archivo:
     vectorizer = pickle.load(archivo)
with open('/home/vant/Documentos/mySpace/fun/chatbot/models/final_model.pkl', 'rb') as archivo:
    final_model = pickle.load(archivo)

with open('/home/vant/Documentos/mySpace/fun/chatbot/models/sbert.sav', 'rb') as archivo:
    modelSBERT = pickle.load(archivo)

with open('/home/vant/Documentos/mySpace/fun/chatbot/models/toxicmodel.sav', 'rb') as archivo:
    toxicity = pickle.load(archivo)

with open('/home/vant/Documentos/mySpace/fun/chatbot/models/emotionmodel.sav', 'rb') as archivo:
    emotion = pickle.load(archivo)

with open('/home/vant/Documentos/mySpace/fun/chatbot/models/zeroshot.sav', 'rb') as archivo:
    classifier_cats = pickle.load(archivo)







print('\nModels loaded.\n')

#%% 


"""

Example of claim: 
    - Trump is the president of Zambia
    - Hakainde Hichilema is the president of Zambia
    - Edgar Chagwa Lungu is the president of Zambia
    - Trump is not the president of Zambia

"""

#IMPORT THE CLASS THAT LET US FIND EVIDENCES ABOUT OUR CLAIM.


FIRST_OUTPUT="""Hello! I am NigeriaFactCheck Bot (but i am trained with Zambia elections data), nice to meet you. My duty is to provide a label to the claim you tell me. Hope i am accurate :D!

What is your question/claim?:

"""
print(FIRST_OUTPUT)


claim=str(input('<Q>: (write bye to leave) '))

while claim != 'bye':

    label=inference_claims(claim,modelSBERT,vectorizer,final_model,emotion,toxicity,classifier_cats)

    
    claim=str(input('<Q>: '))
    

if claim=='bye': print('Hope i was useful, see you in a bit!')