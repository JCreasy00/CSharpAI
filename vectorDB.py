from transformers import LongformerTokenizer, LongformerModel
import torch

# Initialize the Longformer model and tokenizer
tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
model = LongformerModel.from_pretrained('allenai/longformer-base-4096')

def vectorize_text(text):
    # Tokenize the text and convert to tensors
    inputs = tokenizer(text, return_tensors='pt')

    # Get the embeddings
    outputs = model(**inputs)

    # Use the embeddings of the [CLS] token (the first token)
    embeddings = outputs[0][0][0]

    return embeddings.detach().numpy()

# Example usage
article_text = "This is an example article that is longer than a single sentence."
vector = vectorize_text(article_text)

print(vector)