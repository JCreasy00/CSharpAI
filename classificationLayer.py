# Jacob Creasy

# what is Keras?
# https://www.tensorflow.org/guide/keras#:~:text=Keras%20is%20the%20high%2Dlevel,focus%20on%20modern%20deep%20learning.

# NOTE: this is a recurrent neural network (RNN) with Long Short-Term Memory units (LSTM)
# includes an embedding layer and a dense layer. These layers are transformation layers, our input goes and and we get back a number between 0 and 1

# NOTE: Tensor Flow/Keras has a save method that allows us to save the model and deploy it later
# this does not include that because I wanted to know what was happening behind the scenes with Epochs


# import modules
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, LSTM
import numpy as np

# Sample data (sentences) and labels (0: not code-related, 1: code-related)
# this is used to teach the neural network what a code or not code realted sentence is
sentences = [
    "How do you sort an array in Python?",
    "I love watching movies on the weekend.",
    "How can you concatenate strings in JavaScript?",
    "My dog loves to go for walks.",
    "What's the syntax for a for-loop in Java?",
    "I enjoy hiking and being outdoors.",
    "How do you declare variables in C++?",
    "Cooking is one of my favorite hobbies.",
    "Is python a programming language",
]

labels = [1, 0, 1, 0, 1, 0, 1, 0, 1]  # 1 for code-related and 0 for not code-related (correlates with the sentences)
labels = np.array(labels) # convert labels to numpy array

# Tokenizing the sentences
# turn the sentences into numerical form so they can be fed to the NE
tokenizer = Tokenizer(num_words = 100, oov_token = '<OOV>')
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(sentences)

# Padding sequences
# just makes all of the sequences the same size
padded_sequences = pad_sequences(sequences, padding = 'post')

# Building the model
# 'model' from here on out is referring to the RNN
# here we create our layers 
model = Sequential([
    Embedding(100, 16, input_length = padded_sequences.shape[1]), # takes tokenized sentence and converts to vector of 16 dimensions
    LSTM(32), # Long Short Term Memory is a type of RNN layer, in this case we have 32 units which are used to capture the sequence information in the sentences
    Dense(1, activation = 'sigmoid') # also known as the 'fully connected layer'. Takes output form LTSM layer and produces a single output using the sigmoid function ( this is out number betwenn 0 and 1 )
])

# I think this line just configures the model for training. I am not exactly sure what that means
# optimizer is the optimiation algorithm we are using, adam in this case (I asked GPT for a suggestion)
#    the optimizer algorithm dictates how the model updates its paramters (weights and biases) during 
#       goal is to minimize the loss function
#       loss function quantifies how well a machine learning models predictions match the true data.
#    this is an area where we need to find the best algorithm for our scenarion. 
# loss has to do with binary classification. again not exactly sure what that means
# the metrics are what is monitored during training
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Training the model
# after we train the model is when we could then use the save function to save our model
model.fit(padded_sequences, labels, epochs = 10)

# Making predictions
# predictions with not result in code related unless the input sentence is asking a question about code or how to do something
test_sentences = [
    "How do you initialize an array in C?",
    "I like to read books.",
    "Can a dinasour write code about arrays in C?",
    "C is great programming language",
    "Is C a programming language"
]

test_sequences = tokenizer.texts_to_sequences(test_sentences) # tokenzie out test sentences like we did with out training data
padded_test_sequences = pad_sequences(test_sequences, padding ='post', maxlen = padded_sequences.shape[1]) # pad them all to the same size

predictions = model.predict(padded_test_sequences) # our decimal value between 0 and 1

# Decoding the predictions
for i, pred in enumerate(predictions):
    if pred > 0.5:
        print(f"The sentence '{test_sentences[i]}' is code-related.")
    else:
        print(f"The sentence '{test_sentences[i]}' is not code-related.")