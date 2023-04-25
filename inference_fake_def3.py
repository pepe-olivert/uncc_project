#!/usr/bin/env python
# coding: utf-8

# In[36]:


### Carga de las evidencias y embbedings + componentes indicando frecuencia de nombres propios
import pandas as pd
import numpy as np
evidence_sentences = pd.read_csv('/home/vant/Documentos/mySpace/fun/chatbot/datasets/evidence_sentences.csv').drop(['Unnamed: 0'], axis = 1)
evidence_sentences = evidence_sentences['evidence_sentences'].values
#evidence_sentences


# In[37]:


embedding_evidences = pd.read_csv('/home/vant/Documentos/mySpace/fun/chatbot/datasets/embedding_evidences.csv').drop(['Unnamed: 0'], axis = 1)
embedding_evidences = np.array(embedding_evidences)
#embedding_evidences 


# In[48]:


from operator import itemgetter
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")






# In[49]:


candidate_labels = [
    "Voter registration",
    "Election administration",
    "Campaign strategies",
    "Voter turnout",
    "Women in politics"
]



def inference_claims(claim,modelSBERT,vectorizer,final_model,emotion,toxicity,classifier_cats):
    
    evidencias_check = []
    print(f"\nChecking: {claim}\n")
    claim_emb = modelSBERT.encode(claim)
    vec1 = list(vectorizer.transform([claim]).toarray()[0])
    emb_claim_sbert = np.array(list(modelSBERT.encode(claim)) + vec1).reshape(1, -1)
    indexes = np.argsort(cosine_similarity(emb_claim_sbert, embedding_evidences))[0][-5:]
    text = np.array(evidence_sentences)[indexes]
    evidences5 = '.'.join(list(text))
    print(f"The evidences used to classfication are:\n")
    for ev in list(text):
        ev_ = ev.replace('\n', '')
        print(f"\t- {ev_}")
    vec2 = list(vectorizer.transform([evidences5]).toarray()[0])
    pred = classifier_cats(f"If I have these evidences: {evidences5} then this {claim} is True or False", ['True', 'False'])
    sorted_pred = sorted(zip(pred['labels'], pred['scores']))
    probFalseZS, probTrueZS = sorted_pred[0][1], sorted_pred[1][1]
    emotion_labels = emotion(claim)
    all_scores_emotion = []
    print(f"\nAnalyzing emotions: ")
    for dic_em in emotion_labels[0]:
        all_scores_emotion.append((dic_em['label'], dic_em['score']))
    sorted_emotions = sorted(all_scores_emotion)
    sorted_emotions_max = sorted(all_scores_emotion,key=itemgetter(1), reverse = True)[0][0]
    plt.figure(figsize=(12,5))
    sns.barplot(y=[x[0] for x in sorted_emotions], x = [x[1] for x in sorted_emotions])
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    all_scores_emotion_numbers = []
    for n_e in sorted_emotions:
        all_scores_emotion_numbers.append(n_e[1])
    toxicity_labels = toxicity(claim)
    all_scores_toxicity = []
    print(f"Analyzing toxicity: ")
    for dic_em in toxicity_labels[0]:
        all_scores_toxicity.append((dic_em['label'], dic_em['score']))
    sorted_toxicity = sorted(all_scores_toxicity)
    all_scores_toxicity_numbers = []
    for n_e in sorted_toxicity:
        all_scores_toxicity_numbers.append(n_e[1])
    plt.figure(figsize=(12,5))
    sns.barplot(y=[x[0] for x in sorted_toxicity], x = [x[1] for x in sorted_toxicity])
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    pred2 = classifier_cats(claim, candidate_labels)
    sorted_pred2 = sorted(zip(pred2['labels'], pred2['scores']))
    sorted_pred2_max = sorted(zip(pred2['scores'], pred2['labels']), reverse = True)[0][1]
    all_scores_cat = []
    for cat in sorted_pred2:
        all_scores_cat.append(cat[1])
    ev_emb = modelSBERT.encode(evidences5)
    evidencias_check.append(evidences5)
    r = [probFalseZS,probTrueZS]  + all_scores_emotion_numbers+all_scores_toxicity_numbers + all_scores_cat + list(claim_emb) + list(ev_emb) + vec1 + vec2
    
    probs = final_model.predict_proba(np.array(r).reshape(1,-1))
    categories = {0: 'FALSE', 1: 'TRUE'}
    argmax = np.argmax(probs[0])
    print(f"\n<A>: This text is {categories[argmax]} with a probability of {str(round(probs[0][argmax], 4))} by a XGBOOST model")
    return np.array(r).reshape(1,-1)


