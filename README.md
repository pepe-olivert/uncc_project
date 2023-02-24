This simple text file will be used to document every aspect and goal we are going to try to achieve in this subject.

The team members are Hugo Albert, Kexin Jiang, Diana Yaser, David Borregón, Iván Arcos and José Fco. Olivert. We will be cooperating with UNICC in a misinformation detection project. 

The objective of the project is to build a Pipeline composed of two things, an Fact-Checking algorithm and a Machine Learning model. The Fact-Checking algorithm will be in charge of updating the data of the model. A big problem of using a simple machine or deep learning model for this task is that the information in social media gets outdated easily. That's why we need that algorithm. Also, it will download all the information and build the database in the first step of the project. The database will be composed of sentences that will be categorized as "evidence" and "claims",that could be "true" or "false".

For the ML model we will use a pretrained model such as BERT and retrained it with our data obtained by our algorithm for our specific topic. It will return the probability of the sentence of being "true", "contradictory" or "neutral"
