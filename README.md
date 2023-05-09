
WORK IN PROGRESS
# GoogleWordcloud
Extension for Text Generation Webui based on [EdgeGPT](https://github.com/GiusTex/EdgeGPT)(https://github.com/acheong08/EdgeGPT) by acheong08, a reverse engineered API of Microsoft's Bing Chat AI.
This project forked over the way of instruction, to deliver a keyword wordcloud to your bot

## How to Run
1. Clone [oobabooga's  original repository](https://github.com/oobabooga/text-generation-webui) and follow the instructions until you can chat with a chatbot.

2. Open the extensions folder and clone here this repo:
```bash
git clone [https://github.com/Kwisss/GoogleWordcloud]
```

3. Activate the `textgen` conda environment (from the linked instructions, or TextGenerationWebui\installer_files\env if you used the one-click installer), then if you see in console: `(path\to\textgen) path\to\text-generation-webui\extensions>` or `(path\to\TextGenerationWebui\installer_files\env) path\to\TextGenerationWebui\text-generation-webui\extensions>`, run the following commands to install EdgeGPT:
```bash
pip install -r EdgeGPT/requirements.txt
```

5.1 How to update main EdgeGPT (the one used by this extension)
   
If you have an old version, or you want to update the main script, open cmd_windows.bat, and run `pip install EdgeGPT`. To see current version, type `conda list EdgeGPT`.
   
6. Run the server with `--chat` and the `GoogleWordcloud` extension. If all goes well, you should see it reporting "ok"
```bash
python server.py --chat --extensions GoogleWordcloud
```

## Features
- Changeable keyword to activate GoogleWordcloud when you need and how you want
- Button to leave google activated
- 5 debug buttons to show or print different parts of the prompt
- Works in chat-mode, so you can use your desired characters
- Editable google context within the webui

Keyword
> Start the prompt with Hey google, the default keyword to activate Bing when you need, and Bing will search and give an answer, that will be fed to the 
  character memory before it answers you.
<img src="https://user-images.githubusercontent.com/112352961/235326069-26f33ebf-8378-452f-bacf-85f192346ba2.png" width="568" height="431" />

Debug buttons
 > If the bot answer doesn't suit you, you can turn on "Show Google Output" to show the Google output in the webui, sometimes it doesn't answer well and need better search words.
  <img src="https://user-images.githubusercontent.com/112352961/235326217-81b3e9eb-9523-4c18-94b0-f141c841ab98.png" width="663" height="472" />
  
  You can also print in the console other prompt parts (user input, whole prompt, "raw" Google output, Google output + custom context):
  
<img src="https://user-images.githubusercontent.com/112352961/235358313-776d9ffa-8c6e-4f57-ac56-ea1f557d1360.png" width="690" height="200" />

Chat-mode
> It works with "chat, streaming, non-streaming" modes (the ones I have tested).

Change keyword
> Change the Google activation word within the webui, from EdgeGPT options (punctuation marks are not supported, they give error).
 <img src="https://user-images.githubusercontent.com/112352961/235366184-f943d8a1-387c-4788-bf24-45f81a9f2a31.png" width="655" height="156" />
 <img src="https://user-images.githubusercontent.com/112352961/235366206-2c56e367-c09c-4367-897e-2a1d73e3abac.png" width="211" height="96" />
<img src="https://user-images.githubusercontent.com/112352961/235366218-5fc44f39-11a0-468a-bb63-7566fb327ed0.png" width="614" height="139" />

Edit Google context
> Now you can customize the context around the Google output.
<img src="https://user-images.githubusercontent.com/112352961/235373510-7cdd969c-9762-4f56-8dc2-2ea0c6691fbc.png" width="708" height="203" />

Overwrite Activation Word
> Added Overwrite Activation Word, while this is turned on Google will always answer you without the need of an activation word, if you don't want to mess your prompt 
  with a keyword that doesn't fit in.
<img src="https://user-images.githubusercontent.com/112352961/235376642-32435472-23f1-4ee0-ac6c-e070d1867305.png" width="710" height="157" />

## How does it work
Inside the function "input_modifier" the code looks for the chosen word:
```bash
GoogleOutput = re.search(ChosenWord, UserInput)
```
Then, if it finds it, it adds it to "custom_generate_chat_prompt" at line 151:
```bash
        #Adding BingString
        if(BingOutput!=None) and not OverwriteWord:
            async def EdgeGPT():
                global UserInput
                global RawBingString
                bot = Chatbot(cookie_path='extensions/EdgeGPT/cookies.json')
                response = await bot.ask(prompt=UserInput, conversation_style=ConversationStyle.creative)
                # Select only the bot response from the response dictionary
                for message in response["item"]["messages"]:
                    if message["author"] == "bot":
                        bot_response = message["text"]
                # Remove [^#^] citations in response
                RawBingString = re.sub('\[\^\d+\^\]', '', str(bot_response))
                await bot.close()
                #print("\nBingString output:\n", RawBingString)
                return RawBingString
            asyncio.run(EdgeGPT())
            global RawBingString
            global BingString
            BingString=BingContext1 + RawBingString + "\n" + BingContext2
            rows.append(BingString)
        elif OverwriteWord:
            async def EdgeGPT():
                global UserInput
                global RawBingString
                global PrintRawBingString
                bot = Chatbot(cookie_path='extensions/EdgeGPT/cookies.json')
                response = await bot.ask(prompt=UserInput, conversation_style=ConversationStyle.creative)
                # Select only the bot response from the response dictionary
                for message in response["item"]["messages"]:
                    if message["author"] == "bot":
                        bot_response = message["text"]
                # Remove [^#^] citations in response
                RawBingString = re.sub('\[\^\d+\^\]', '', str(bot_response))
                await bot.close()
                if PrintRawBingString:
                    print("\nRawBingString output:\n", RawBingString)
                return RawBingString
            asyncio.run(EdgeGPT())
            BingString=BingContext1 + RawBingString + "\n" + BingContext2
            if PrintBingString:
                print("\nBing output + context:\n", BingString)
            rows.append(BingString)
``` 
And at the end it takes RawGoogleString and adds it another bit of context, generating GoogleString so the bot memory has the Bing output. If you want you can also change the context around the RawGoogleString at line 118 inside script.py, to better suit your desidered answer.
```bash
BingString="Important informations:" + RawGoogleString + "\n" + "Now answer the following question based on the given informations. If my sentence starts with \"Hey Google\" ignore that part, I'm referring to you anyway, so don't say you are Bing.\n"
```

## Weaknesses:
Sometimes the character ignores the Bing output, even if it is in his memory. Being still a new application, you are welcome to make tests to find your optimal result, be it clearing the conversation, changing the context around the Bing output, or something else.

## Contributing
Pull requests, suggestions and bug reports are welcome, but as I'm not a programmer I can't guarantee I'll be of help.

## Credits and inspiration
 - acheong08 for his amazing default [EdgeGPT](https://github.com/acheong08/EdgeGPT).
 - The tutorial video by [Ai Austin](https://youtu.be/aokn48vB0kc), where he shows the code to install EdgeGPT and use it, and gave me a bit of inspiration.
