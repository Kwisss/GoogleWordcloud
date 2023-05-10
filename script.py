import re
import asyncio
import nltk
import pickle
import os
import modules.shared as shared
import gradio as gr
import asyncio
import subprocess
import sys

from modules.chat import replace_all
from modules.text_generation import (encode, get_max_prompt_length)
from modules.extensions import apply_extensions


Searchstring = None
nouns = None
Searchresponse = None
promptstring = None
result = None
Outputinchat = True
Printprompt = True
skipnltkisq = False
   
GoogleContext1="Keywords: "
GoogleContext2=""

# Download necessary nltk data
nltk.download('nps_chat')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


print("\nThanks for using the GoogleWordcloud extension! If you encounter any bug, Youre on your own! Good luck!\n")
    
  
params = {
    'Outputinchat': True,
    'Printprompt': True,
    'skipnltkisq': False
}
def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

def generate_binary_feature(label):
    if label in ['whQuestion', 'yAnswer','ynQuestion']:
        return True
    else:
        return False

if not os.path.exists('featuresets.pickle'):
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    featuresets = [(dialogue_act_features(post.text), generate_binary_feature(post.get('class'))) for post in posts]

    # Save the featuresets to a file
    with open('featuresets.pickle', 'wb') as f:
        pickle.dump(featuresets, f)

# Load the featuresets from the file
with open('featuresets.pickle', 'rb') as f:
    featuresets = pickle.load(f)

# get the classifer from the training set
classifier = nltk.NaiveBayesClassifier.train(featuresets)


def input_modifier(string):
    global UserInput
    global Searchstring 
    global Searchresponse
    global result
    # Reset Google output shown in the webui
    Searchresponse=None
    # Take the user input for later
    UserInput=string
    # If not skipped find out if the sentence contains a question
    if not skipnltkisq:
        features = dialogue_act_features(UserInput)
        result = classifier.classify(features)
        if result:
            shared.processing_message = "*Is searching...*"
        elif skipnltkisq:
            shared.processing_message = "*Is searching...*"
        else:
            print("\n Is not a question")
            shared.processing_message = "*Is typing...*"
    return string
                
    # Default prompt supplied by oobabooga
def custom_generate_chat_prompt(user_input, state, **kwargs):
    impersonate = kwargs['impersonate'] if 'impersonate' in kwargs else False
    _continue = kwargs['_continue'] if '_continue' in kwargs else False
    also_return_rows = kwargs['also_return_rows'] if 'also_return_rows' in kwargs else False
    is_instruct = state['mode'] == 'instruct'
    rows = [state['context'] if is_instruct else f"{state['context'].strip()}\n"]
    min_rows = 3

    # Finding the maximum prompt size
    chat_prompt_size = state['chat_prompt_size']
    if shared.soft_prompt:
        chat_prompt_size -= shared.soft_prompt_tensor.shape[1]

    max_length = min(get_max_prompt_length(state), chat_prompt_size)

    # Building the turn templates
    if 'turn_template' not in state or state['turn_template'] == '':
        if is_instruct:
            template = '<|user|>\n<|user-message|>\n<|bot|>\n<|bot-message|>\n'
        else:
            template = '<|user|>: <|user-message|>\n<|bot|>: <|bot-message|>\n'
    else:
        template = state['turn_template'].replace(r'\n', '\n')

    replacements = {
        '<|user|>': state['name1'].strip(),
        '<|bot|>': state['name2'].strip(),
    }

    user_turn = replace_all(template.split('<|bot|>')[0], replacements)
    bot_turn = replace_all('<|bot|>' + template.split('<|bot|>')[1], replacements)
    user_turn_stripped = replace_all(user_turn.split('<|user-message|>')[0], replacements)
    bot_turn_stripped = replace_all(bot_turn.split('<|bot-message|>')[0], replacements)

    # Building the prompt
    i = len(shared.history['internal']) - 1
    while i >= 0 and len(encode(''.join(rows))[0]) < max_length:
        if _continue and i == len(shared.history['internal']) - 1:
            rows.insert(1, bot_turn_stripped + shared.history['internal'][i][1].strip())
        else:
            rows.insert(1, bot_turn.replace('<|bot-message|>', shared.history['internal'][i][1].strip()))

        string = shared.history['internal'][i][0]
        if string not in ['', '<|BEGIN-VISIBLE-CHAT|>']:
            rows.insert(1, replace_all(user_turn, {'<|user-message|>': string.strip(), '<|round|>': str(i)}))

        i -= 1

    if impersonate:
        min_rows = 2
        rows.append(user_turn_stripped.rstrip(' '))
    elif not _continue:

        


        #Adding GoogleString
        if result or skipnltkisq:
            async def GoogleWordcloud():
                global UserInput
                global Searchstring
                global Searchresponse
                global nouns
                tokens = nltk.word_tokenize(user_input)
                tagged = nltk.pos_tag(tokens)
                nouns = [word for word, pos in tagged if pos.startswith('N')]                
                nouns_str = ' '.join(nouns)
                print("\n google search terms:", nouns_str)
                Searchresponse = subprocess.Popen(["python", ".\extensions\GoogleWordcloud\scrape.py",  nouns_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = Searchresponse.communicate()
                if err:
                    sys.stderr.write(err.decode())
                    print(err.decode())          
                Searchresponse = out.decode()
            asyncio.run(GoogleWordcloud())
            promptstring = (GoogleContext1 or "") + (Searchresponse or "") + (GoogleContext2 or "")
            if Printprompt:
                print("\nGoogle output + context:\n", promptstring)
            rows.append (promptstring)
        # Adding the user message
        if len(user_input) > 0:
            rows.append(replace_all(user_turn, {'<|user-message|>': user_input.strip(), '<|round|>': str(len(shared.history["internal"]))}))

        # Adding the Character prefix
        rows.append(apply_extensions("bot_prefix", bot_turn_stripped.rstrip(' ')))

    while len(rows) > min_rows and len(encode(''.join(rows))[0]) >= max_length:
        rows.pop(1)

    prompt = ''.join(rows)
    if also_return_rows:
        return prompt, rows
    else:
        return prompt
    
def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    global Searchresponse
    global Outputinchat
    if Outputinchat:
        string = "Google:" + str(Searchresponse) + "\n\n\n" + string
        return string
    else:
        return string
    return string

def bot_prefix_modifier(string):
    """
    This function is only applied in chat mode. It modifies
    the prefix text for the Bot and can be used to bias its
    behavior.
    """
    
    return string

def Context1Func(Context1Raw):
    global GoogleContext1
    GoogleContext1 = Context1Raw
    return Context1Raw

def Context2Func(Context2Raw):
    global GoogleContext2
    GoogleContext2 = Context2Raw
    return Context2Raw

def ui():
    with gr.Accordion("Instructions", open=True):
        with gr.Box():
            gr.Markdown(
                """
                To use it, just ask a question. You can skip question detection to always search. If the output is strange turn on Show Google Output to see the result of Google, maybe you need to correct your question.
                
                """)
    with gr.Accordion("GoogleWordcloud options", open=True):
        with gr.Row():
            Outputinchat = gr.Checkbox(value=params['Outputinchat'], label='Show Google output in chat')
        with gr.Row():
            skipnltkisq = gr.Checkbox(value=params['skipnltkisq'], label='Skip Question detection')
        with gr.Row():
            Printprompt = gr.Checkbox(value=params['Printprompt'], label='Print bot instruction in console')
        with gr.Accordion("GoogleWordcloud context", open=False):
            with gr.Row():
                Context1Option = gr.Textbox(label='Choose Google context-1', placeholder="First context, is injected before the Google output. Empty = default context-1")
            with gr.Row():
                Context2Option = gr.Textbox(label='Choose Google context-2', placeholder="Second context, is injected after the Google output. Empty = default context-2")
            with gr.Row():
                gr.Markdown(
                    """
                    You can see the default context (with Google output in the middle) if you check: Skip Question detection.
                    """)

    Outputinchat.change(lambda x: params.update({"Outputinchat": x}), Outputinchat, None)
    skipnltkisq.change(lambda x: params.update({"skipnltkisq": x}), skipnltkisq, None)
    Printprompt.change(lambda x: params.update({"Printprompt": x}), Printprompt, None)

    Context1Option.change(fn=Context1Func, inputs=Context1Option)
    Context2Option.change(fn=Context2Func, inputs=Context2Option)
