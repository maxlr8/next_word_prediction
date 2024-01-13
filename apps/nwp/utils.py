# importing packages
import torch
import string
from transformers import BertTokenizer, BertForMaskedLM

def load_model(model_name):
    try:
        if model_name.lower() == 'bert':
            bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            bert_model = BertForMaskedLM.from_pretrained('bert-base-uncased').eval()
            return bert_tokenizer, bert_model
    except Exception as e:
        print('error in load_model',e)

def encode(tokenizer, text_sentence, add_special_tokens=True):
    text_sentence = text_sentence.replace('<mask>',tokenizer.mask_token)
    if tokenizer.mask_token == text_sentence.split()[-1]:
        text_sentence += ' .'
        input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
        mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
    return input_ids, mask_idx

def decode(tokenizer, pred_idx, top_clean):
    ignore_tokens = string.punctuation + '[PAD]'
    tokens = []
    for w in pred_idx:
        token = ''.join(tokenizer.decode(w).split())
        if token not in ignore_tokens:
            tokens.append(token.replace('##', ''))
    return '\n'.join(tokens[:top_clean])

def get_all_predictions(text_sentence, top_clean=5):
    input_ids, mask_idx = encode(bert_tokenizer, text_sentence)
    with torch.no_grad():
        predict = bert_model(input_ids)[0]
    bert = decode(bert_tokenizer, predict[0, mask_idx, :].topk(top_clean).indices.tolist(), top_clean)
    return {'bert': bert}

def get_prediction_eos(input_text,topk):
    try:
        input_text += ' <mask>'
        res = get_all_predictions(input_text, top_clean=topk)
        return res
    except Exception as error:
        print('error in get_prediction_eos', error)

def predict_next_word(input_text, model='BERT', topk=3):
    preds = get_prediction_eos(input_text,topk)
    return preds[model.lower()].split('\n')
bert_tokenizer, bert_model  = load_model('BERT')