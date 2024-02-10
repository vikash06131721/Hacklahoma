# -*- coding: UTF-8 -*-
import time
# import env_load
from flask import request, jsonify, Response
# from transformers import pipeline
# from transformers import AutoTokenizer,AutoModelForCausalLM

# copy_models_from_nfs()
from flask import Flask
import json
# import torch

app = Flask(__name__, static_folder='static', template_folder='templates')  # type: Flask # Initialize the Flask application
# device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
# model_str = "defog/sqlcoder-7b-2" #chat-hf (hugging face wrapper version)
# tokenizer = AutoTokenizer.from_pretrained(model_str)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# model = AutoModelForCausalLM.from_pretrained("defog/sqlcoder-7b-2", torch_dtype=torch.float16, device_map="cuda:0")


# pipeline = pipeline(
#     "text-generation",
#     model=model,
#     torch_dtype=torch.float16,
#     device_map=device # if you have GPU
# )

# def return_prediction(text,length,k):
#     sequences = pipeline(
#     text,
#     do_sample=True,
#     top_k=k,
#     top_p = 0.9,
#     temperature = 0.2,
#     num_return_sequences=2,
#     eos_token_id=tokenizer.eos_token_id,
#     max_length=length, # can increase the length of sequence
#     )

#     return sequences
# tokenizer = BertTokenizerFast.from_pretrained("models")
#language model load
# model =  BertForMaskedLM.from_pretrained("models/checkpoint-72000",output_hidden_states = True)
# model.to(device)

# #income qa model
# model_checkpoint = "models/bert-finetuned-income/checkpoint-21000/"
# question_answerer = pipeline("question-answering", model=model_checkpoint)

from prompter import Prompter
prompter = Prompter("alpaca")

@app.route('/return_pred', methods=['POST'])
def income_qa():
    response ={}
    status = 200
    # response = jsonify(response)
    

    response["output"] =["""The paper reports on the BioLaySumm shared task from the ACL 2023 BioNLP Workshop, aimed at creating abstractive summarisation models to produce easily understandable summaries of biomedical research for the general public. The task was divided into Lay Summarisation and Readability-controlled Summarisation, attracting 20 teams to develop models that simplify scientific articles for non-experts, highlighting the challenge of technical jargon and the need for making research accessible.""",
    """At ACL 2023's BioNLP Workshop, a shared task named BioLaySumm was introduced to foster the development of summarisation models that can generate non-technical, or "lay," summaries of biomedical articles. The initiative, which saw participation from 20 teams, included challenges in lay summarisation and readability-controlled summarisation, emphasizing the importance of making scientific findings understandable to wider audiences."""]
    response = jsonify(response)
    response.status_code = status

    return response

# @app.route('/return_pred', methods=['POST'])
# def income_qa():
#     content = json.loads(request.data)
#     instruction = content['instruction']
#     input_ = content['input']
#     try:
#         max_length = content["tokens"]
#     except KeyError:
#         max_length=1000
#     try:
#         top_p = content["top_p"]
#     except KeyError:
#         top_p=0.5
#     try:
#         temp = content["temperature"]
#     except KeyError:
#         temp=0.8
#     prompt_ = prompter.generate_prompt(
#             instruction,
#             input_
#         )

#     inputs = tokenizer(prompt_, return_tensors="pt", truncation=False,padding=True).input_ids.cuda(0)

#     output = model.generate(inputs, max_length=max_length, top_p=top_p,temperature=temp)
#     decoded_texts = tokenizer.batch_decode(output, skip_special_tokens=True)
#     response ={}
#     response["generated"] = decoded_texts
#     # import pdb;pdb.set_trace()
    
#     status = 200
#     response = jsonify(response)
#     response.status_code = status
#     # logger.info(f"time taken : {time.time() - t}")
#     return response

@app.route('/healthcheck', methods=['GET'])
def health_check():
    resp = Response()
    resp.data = json.dumps({"status":"All Good!"})
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True,debug=False)
