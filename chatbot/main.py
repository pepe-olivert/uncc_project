# %% READING THE DATA

print('Importing the modules and reading the evidence data...')
import pandas as pd
import pickle
from  preprocessing.evidenceselection import *
import pandas as pd
import numpy as np
evidence_sentences = pd.read_csv('./datasets/Evidences_db.csv').drop(['Unnamed: 0'], axis = 1)
evidence_sentences = evidence_sentences['Evidence'].values
embedding_evidences = pd.read_csv('./datasets/Evidences_db_embeddings.csv').drop(['Unnamed: 0'], axis = 1)
embedding_evidences = np.array(embedding_evidences)
import torch.nn as nn
from transformers import RobertaModel
import torch.nn.functional as F

# Define the custom model
class CustomModel(nn.Module):
    def __init__(self, pretrained_model_name, num_extra_features, num_classes):
        super(CustomModel, self).__init__()
        self.roberta = RobertaModel.from_pretrained(pretrained_model_name, output_attentions=True)
        self.dropout = nn.Dropout(p=0.3)
        self.conv_layers = nn.Sequential(
            nn.Conv1d(in_channels=200, out_channels=64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Conv1d(in_channels=64, out_channels=32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Conv1d(in_channels=32, out_channels=16, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3)
        )
        self.extra_features_layer = nn.Linear(num_extra_features, 64)
        self.concat_layer = nn.Linear(432 + 64, 128)
        self.output_layer = nn.Linear(128, num_classes)
        self.loss_fn = nn.BCEWithLogitsLoss()

    def forward(self, input_ids, attention_mask, extra_features, labels=None):
        roberta_output = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = roberta_output.last_hidden_state
        attention_weights = roberta_output[-1]
        
        conv_output = self.conv_layers(last_hidden_state)
        conv_output = nn.Flatten()(conv_output)
        conv_output = self.dropout(conv_output)
        
        extra_features_output = self.extra_features_layer(extra_features)
        
        concat_output = torch.cat((conv_output, extra_features_output), dim=1)
        concat_output = self.concat_layer(concat_output)
        concat_output = nn.ReLU()(concat_output)
        concat_output = self.dropout(concat_output)
        
        logits = self.output_layer(concat_output)
        probabilities = torch.sigmoid(logits)
        
        outputs = {"logits": logits, "probabilities": probabilities, "last_attention_weights": attention_weights}
        
        if labels is not None:
            loss = self.loss_fn(logits, labels.float())
            outputs["loss"] = loss
        
        return outputs
import matplotlib.pyplot as plt
import pickle
from preprocessing.inference_fake_def3 import inference_claims

#This code will be for the chatbot2.0 using the inference_fake.py script with a model more accurate than the one we are using right now.




#%%


#We will try to build a "chatbot". We will create an interface where you can ask questions and you will 
#recieve an answer.

#As we are working on the Nigeria Elections our "bot" will recieve only questions about that specific topic
#and will answer if that sentence or claim given by the user is false, true or unproven.

#Further more we will try to give a summary given the label and the claim. Why is it labeled like this?


# FIRST STEP WE LOAD THE MODEL

print('\nLoading the models...\n')

with open('./models_used/vectorizer.pkl', 'rb') as archivo:
     vectorizer = pickle.load(archivo)
with open('./models_used/final_model.pkl', 'rb') as archivo:
    final_model = pickle.load(archivo)

from sentence_transformers import SentenceTransformer
modelSBERT = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open('./models_used/toxicmodel.sav', 'rb') as archivo:
    toxicity = pickle.load(archivo)

with open('./models_used/emotionmodel.sav', 'rb') as archivo:
    emotion = pickle.load(archivo)

with open('./models_used/zeroshot.sav', 'rb') as archivo:
    classifier_cats = pickle.load(archivo)







print('\nModels loaded.\n')

#%% 
import streamlit as st
from streamlit_chat import message

def generate_answer():
    user_msg = st.session_state.input_text
    st.session_state.input_text = ""
    st.session_state.history.append(
        {"message": user_msg, "is_user":True,
        "avatar_style": "fun-emoji",
        "seed": 4}
    )
    st.session_state.history.append(
        {"message": inference_claims(user_msg,modelSBERT,final_model,emotion,toxicity, graphs), "is_user":False,
        "avatar_style": "bottts-neutral",
        "seed": 36}
    )




#Example of claim: 
#    - Trump is the president of Zambia
#    - Hakainde Hichilema is the president of Zambia
#    - Edgar Chagwa Lungu is the president of Zambia
#    - Trump is not the president of Zambia


#IMPORT THE CLASS THAT LET US FIND EVIDENCES ABOUT OUR CLAIM.


FIRST_OUTPUT="""Hello! It is NigeriaFactCheck Bot at your service, nice to meet you. My duty is to provide a label to the claim you tell me. Hope i am accurate :D!

What is your question/claim?:

"""
#print(FIRST_OUTPUT)
    
st.title("NigeriaFactCheck Bot")
st.text("""Give the NigeriaFactCheck Bot a statement and it will tell you whether it is correct 
or not according to the elections of Nigeria!
An example of a claim would be: 'Trump is the president of Nigeria'""")
initial_history = [
    {
        "message": "Hello bot!",
        "is_user": True,
        "avatar_style": "fun-emoji",
        "seed": 4
    },
    {
        "message": FIRST_OUTPUT,
        "is_user": False,
        "avatar_style": "bottts-neutral",
        "seed": 36
    }
]

if "history" not in st.session_state:
    st.session_state.history = initial_history
c = st.expander("Open to see the previous messages!")
graphs = st.expander("Open to see the charts of the last claim!")
for i, chat in enumerate(st.session_state.history):
    if i < len(st.session_state.history)-6:
        with c:
            message(**chat, key=str(i)) #unpacking
    else:
        message(**chat, key=str(i)) #unpacking
st.text_input("You: ", "", key="input_text", on_change = generate_answer)


#if claim=='bye': print('Hope i was useful, see you in a bit!')