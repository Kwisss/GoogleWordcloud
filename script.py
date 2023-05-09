import re
import asyncio
import modules.shared as shared
import gradio as gr
import subprocess
import sys

from EdgeGPT import Chatbot, ConversationStyle
from modules.chat import replace_all
from modules.text_generation import (encode, get_max_prompt_length)
from modules.extensions import apply_extensions


GoogleOutput=None
RawGoogleString=None
GoogleString=None
ShowGoogleString=False
OverwriteWord=False
PrintUserInput=False
PrintWholePrompt=False
PrintRawGoogleString=False
PrintGoogleString=False

ChosenWord="Hey Google"
GoogleContext1="Interesting keywords to use: "
GoogleContext2="use these keywords to make an extremely long winded answer!"

print("\nThanks for using the GoogleGPT extension! If you encounter any bug, Youre on your own! Good luck!")

params = {
    'ShowGoogleString': False,
    'OverwriteWord': False,
    'PrintUserInput': False,
    'PrintWholePrompt': False,
    'PrintRawGoogleString': False,
    'PrintGoogleString': False
}

def input_modifier(string):
    global UserInput
    global GoogleOutput
    global RawGoogleString
    global ChosenWord
    # Reset Google output shown in the webui
    RawGoogleString=None

    UserInput=string
    # Find out if the chosen word appears in the sentence.
    # If you want to change the chosen word, change "Hey Google"
    GoogleOutput = re.search(ChosenWord, UserInput)

    if params['ShowGoogleString']:
        global ShowGoogleString
        ShowGoogleString=True
    else:
        ShowGoogleString=False

    if params['OverwriteWord']:
        global OverwriteWord
        OverwriteWord=True
    else:
        OverwriteWord=False

    if params['PrintUserInput']:
        global PrintUserInput
        PrintUserInput=True
        print("User input:\n", UserInput)
    else:
        PrintUserInput=False
    
    if params['PrintWholePrompt']:
        global PrintWholePrompt
        PrintWholePrompt=True
    else:
        PrintWholePrompt=False
    
    if params['PrintRawGoogleString']:
        global PrintRawGoogleString
        PrintRawGoogleString=True
    else:
        PrintRawGoogleString=False

    if params['PrintGoogleString']:
        global PrintGoogleString
        PrintGoogleString=True
    else:
        PrintGoogleString=False

    if(GoogleOutput!=None) and not OverwriteWord:
        shared.processing_message = "*Is searching...*"
    elif OverwriteWord:
        shared.processing_message = "*Is searching...*"
    else:
        shared.processing_message = "*Is typing...*"
    return string
    

    # Default prompt + GoogleString (if requested)
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
        if(GoogleOutput!=None) and not OverwriteWord:
            async def EdgeGPT():
                global UserInput
                global RawGoogleString
                global PrintRawGoogleString
                response = subprocess.Popen(["python", ".\extensions\Google\scrape.py", UserInput], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = response.communicate(input=b'kwissbeats')
                response.wait()  # Wait for the process to complete
                if err:
                    sys.stderr.write(err.decode())
                response = out.decode()
                # Select only the bot response from the response dictionary
                bot_response = response
                # Remove [^#^] citations in response
                RawGoogleString = str(bot_response)
                if PrintRawGoogleString:
                    print("\nRawGoogleString output:\n", RawGoogleString)
                return RawGoogleString
            asyncio.run(EdgeGPT())
            global RawGoogleString
            global GoogleString
            global PrintGoogleString
           # global GoogleContext1
           # global GoogleContext2
            GoogleString=GoogleContext1 + RawGoogleString + "\n" + GoogleContext2
            if PrintGoogleString:
                print("\nGoogle output + context:\n", GoogleString)
            rows.append(GoogleString)
        elif OverwriteWord:
            async def EdgeGPT():
                global UserInput
                global RawGoogleString
                global PrintRawGoogleString
                response = subprocess.Popen(["python", ".\extensions\Google\scrape.py", UserInput], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = response.communicate(input=b'kwissbeats')
                response.wait()  # Wait for the process to complete
                if err:
                    sys.stderr.write(err.decode())
                response = out.decode()
                # Select only the bot response from the response dictionary
                bot_response = response
                # Remove [^#^] citations in response
                RawGoogleString = str(bot_response)
                if PrintRawGoogleString:
                    print("\nRawGoogleString output:\n", RawGoogleString)
                return RawGoogleString
            asyncio.run(EdgeGPT())
            GoogleString = (GoogleContext1 or "") + (RawGoogleString or "") + "\n" + (GoogleContext2 or "")
            if PrintGoogleString:
                print("\nGoogle output + context:\n", GoogleString)
            rows.append(GoogleString)

        # Adding the user message
        if len(user_input) > 0:
            rows.append(replace_all(user_turn, {'<|user-message|>': user_input.strip(), '<|round|>': str(len(shared.history["internal"]))}))

        # Adding the Character prefix
        rows.append(apply_extensions("bot_prefix", bot_turn_stripped.rstrip(' ')))

    while len(rows) > min_rows and len(encode(''.join(rows))[0]) >= max_length:
        rows.pop(1)

    prompt = ''.join(rows)
    if also_return_rows:
        if PrintWholePrompt:
            print("Prompt:\n", prompt)
        return prompt, rows
    else:
        if PrintWholePrompt:
            print("Prompt:\n", prompt)
        return prompt
    

def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    global GoogleOutput
    global RawGoogleString
    global ShowGoogleString
    if ShowGoogleString:
        string = "Google:" + str(RawGoogleString) + "\n\n\n" + string
        return string
    else:
        return string


def bot_prefix_modifier(string):
    """
    This function is only applied in chat mode. It modifies
    the prefix text for the Bot and can be used to bias its
    behavior.
    """
    
    return string


def FunChooseWord(CustomWordRaw):
    global ChosenWord
    ChosenWord = CustomWordRaw
    return CustomWordRaw

def Context1Func(Context1Raw):
    global GoogleContext1
    GoogleContext1 = Context1Raw
    return Context1Raw

def Context2Func(Context2Raw):
    global GoogleContext2
    GoogleContext2 = Context2Raw
    return Context2Raw


def ui():
    with gr.Accordion("Instructions", open=False):
        with gr.Box():
            gr.Markdown(
                """
                To use it, just start the prompt with Hey Google; it doesn't start if you don't use uppercase and lowercase as in the example. You can change the activation word from EdgeGPT options. If the output is strange turn on Show Google Output to see the result of Google, maybe you need to correct your question.
                
                """)
            
    with gr.Accordion("EdgeGPT options", open=False):
        with gr.Row():
            ShowGoogleString = gr.Checkbox(value=params['ShowGoogleString'], label='Show Google Output')
        with gr.Row():
            WordOption = gr.Textbox(label='Choose and use a word to activate Google', placeholder="Choose your word. Empty = Hey Google")
            OverwriteWord = gr.Checkbox(value=params['OverwriteWord'], label='Overwrite Activation Word. Google will always search, ignoring the activation word.')
        with gr.Accordion("EdgeGPT context", open=False):
            with gr.Row():
                Context1Option = gr.Textbox(label='Choose Google context-1', placeholder="First context, is injected before the Google output. Empty = default context-1")
            with gr.Row():
                Context2Option = gr.Textbox(label='Choose Google context-2', placeholder="Second context, is injected after the Google output. Empty = default context-2")
            with gr.Row():
                gr.Markdown(
                    """
                    You can see the default context (with Google output in the middle) by turning on the fourth option in "Print in console options": "Print Google string in command console".
                    """)
            
    with gr.Accordion("Print in console options", open=False):
        with gr.Row():
            PrintUserInput = gr.Checkbox(value=params['PrintUserInput'], label='Print User input in command console. The user input will be fed first to Google, and then to the default bot.')
        with gr.Row():
            PrintWholePrompt = gr.Checkbox(value=params['PrintWholePrompt'], label='Print whole prompt in command console. Prompt has: context, Google search output, and user input.')
        with gr.Row():
            PrintRawGoogleString = gr.Checkbox(value=params['PrintRawGoogleString'], label='Print raw Google string in command console. The raw Google string is the clean Google output.')
        with gr.Row():
            PrintGoogleString = gr.Checkbox(value=params['PrintGoogleString'], label='Print Google string in command console. It is the Google output + a bit of context, to let the default bot understand what to do with it.')
    

    ShowGoogleString.change(lambda x: params.update({"ShowGoogleString": x}), ShowGoogleString, None)
    WordOption.change(fn=FunChooseWord, inputs=WordOption)
    OverwriteWord.change(lambda x: params.update({"OverwriteWord": x}), OverwriteWord, None)
    
    Context1Option.change(fn=Context1Func, inputs=Context1Option)
    Context2Option.change(fn=Context2Func, inputs=Context2Option)

    PrintUserInput.change(lambda x: params.update({"PrintUserInput": x}), PrintUserInput, None)
    PrintWholePrompt.change(lambda x: params.update({"PrintWholePrompt": x}), PrintWholePrompt, None)
    PrintRawGoogleString.change(lambda x: params.update({"PrintRawGoogleString": x}), PrintRawGoogleString, None)
    PrintGoogleString.change(lambda x: params.update({"PrintGoogleString": x}), PrintGoogleString, None)
