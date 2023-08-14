This simple text file will be used to document every aspect and goal we are going to try to achieve in this subject.

The team members are Hugo Albert, Kexin Jiang, Diana Haj, David Borregón, Iván Arcos and José Fco. Olivert. We will be cooperating with UNICC in a misinformation detection project.

The objective of the project is to build a misinformation detection pipeline composed of two elements: a fact-checking algorithm and a machine learning model. The fact-checking algorithm will be in charge of updating the data of the model. A big problem of using a simple machine learning or deep learning model for the task in hand is that the information in social media gets outdated easily, this is when this algorithm comes in handy. The algorithm will also download all the information and build the database for the initial step of the project. This database will consist of sentences that will be categorized as "evidence" and "claims", which can be either "true" or "false".

For the ML model we will use a pretrained model such as BERT and fine-tune it with the data obtained with our algorithm for the specific topic of interest. The model will return the probability of a given sentence being "true", "contradictory" or "neutral".
