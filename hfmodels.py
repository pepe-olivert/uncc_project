from sentence_transformers import SentenceTransformer
import pickle
from transformers import pipeline
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('mitra-mir/setfit-model-Feb11-Misinformation-on-Media-Traditional-Social')

filename = 'sbert.sav'
pickle.dump(model, open(filename, 'wb'))

classifier_cats = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

filename = 'zeroshot.sav'
pickle.dump(classifier_cats, open(filename, 'wb'))

emotion = pipeline('text-classification', 
                    model='SamLowe/roberta-base-go_emotions', return_all_scores=True)

filename = 'emotionmodel.sav'
pickle.dump(emotion, open(filename, 'wb'))

toxicity = pipeline('text-classification', 
                    model='unitary/unbiased-toxic-roberta', 
                   return_all_scores=True)

filename = 'toxicmodel.sav'
pickle.dump(toxicity, open(filename, 'wb'))

