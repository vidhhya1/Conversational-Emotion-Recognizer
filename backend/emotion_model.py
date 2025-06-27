import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import MultiLabelBinarizer 
import numpy as np


LABEL_MAP = {
    "admiration": "happy",
    "amusement": "happy",
    "anger": "angry",
    "annoyance": "angry",
    "approval": "happy",
    "caring": "happy",
    "confusion": "anxious",
    "curiosity": "surprised",
    "desire": "happy",
    "disappointment": "sad",
    "disapproval": "angry",
    "disgust": "angry",
    "embarrassment": "sad",
    "excitement": "happy",
    "fear": "anxious",
    "gratitude": "happy",
    "grief": "sad",
    "joy": "happy",
    "love": "happy",
    "nervousness": "anxious",
    "optimism": "happy",
    "pride": "happy",
    "realization": "surprised",
    "relief": "happy",
    "remorse": "sad",
    "sadness": "sad",
    "surprise": "surprised",
    "neutral": "neutral"
}


temp_mlb = MultiLabelBinarizer()

temp_mlb.fit([list(LABEL_MAP.keys())])
GOEMOTIONS_LABELS = list(temp_mlb.classes_)


model_path = "./fine_tuned_emotion_model"
loaded_tokenizer = AutoTokenizer.from_pretrained(model_path)
loaded_model = AutoModelForSequenceClassification.from_pretrained(
    model_path,
    use_safetensors=True 
)


loaded_model.eval()


OPTIMAL_THRESHOLD = 0.57  

def get_emotion(text, threshold=OPTIMAL_THRESHOLD):

    inputs = loaded_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)

    
    if next(loaded_model.parameters()).is_cuda: 
        inputs = {name: tensor.cuda() for name, tensor in inputs.items()}

    
    with torch.no_grad(): 
        outputs = loaded_model(**inputs)

 
    probs = torch.sigmoid(outputs.logits).cpu().numpy().flatten()

  
    predicted_label_indices = np.where(probs >= threshold)[0]

    detailed_emotions = []
    general_emotions = []
    emotion_scores = {}

    if len(predicted_label_indices) == 0:

        if "neutral" in GOEMOTIONS_LABELS:
            neutral_index = GOEMOTIONS_LABELS.index("neutral")
            if probs[neutral_index] >= threshold:
                detailed_emotions.append("neutral")
                general_emotions.append("neutral")
                emotion_scores["neutral"] = probs[neutral_index]
            else:
                
                return [], [], {}
        else:
            
            return [], [], {}
    else:
        for idx in predicted_label_indices:
            detailed_emotion = GOEMOTIONS_LABELS[idx]
            general_emotion = LABEL_MAP.get(detailed_emotion, "unknown") 
            
            detailed_emotions.append(detailed_emotion)
            general_emotions.append(general_emotion)
            emotion_scores[detailed_emotion] = probs[idx]

    return detailed_emotions, list(set(general_emotions)), emotion_scores

