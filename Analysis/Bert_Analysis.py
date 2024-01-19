
import numpy as np
import pandas as pd

from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.utils.data import Dataset, DataLoader
import joblib


#모델 가져오기 분류헤드가 아직 훈련되지 않았으니 오류는 정상
def Bert_Analysis(text):    
    num_label = 2
    model_ckpt="JKKANG/bert-fakenews"
    model = (AutoModelForSequenceClassification.from_pretrained(model_ckpt, num_labels= num_label))
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)

    text = text
    inputs = tokenizer(text, return_tensors="pt")
    inputs = dict(inputs)
    
    with torch.no_grad():
        logits = outputs = model(**inputs).logits
    results = torch.softmax(logits, dim=1).tolist()[0]
    prediction = results[0]*100

    if(prediction > 75):
        return 1, f"BERT가 예측한 피싱 메일의 본문은 피싱일 확률이 {prediction}%입니다."
    else:
        return 0