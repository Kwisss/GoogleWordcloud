#🕱 WORK IN PROGRESS🕱

| Feature | From | Status | Function |
| --- | --- | --- | --- |
| Inject Google Wordcloud | - | ✅ | Get it working |
| Lose nltk or multidict | - | ❌ | Reduce libarys |
| Clean up script| - | ❌ | improve readability |
| Integrate scrub.py | - | ❌ | improve readability |
| Keyword frequency selector | - | ❌ | usability improvement |
| Keyword exclusion input box | - | ❌ | usability improvement |
| Better context templates  | - | ❌ | usability improvement |
| Prompt -> Search manipulation | - | ❌ | Get it working |



## GoogleWordcloud
Extension for Text Generation Webui forked from [EdgeGPT](https://github.com/GiusTex/EdgeGPT) by GiusTex which in turn forked (https://github.com/acheong08/EdgeGPT) by acheong08, a reverse engineered API of Microsoft's Bing Chat AI.

This project copy the prompt to search Google, which will deliver a keyword wordcloud to your bot.

## How to Run on windows
1. Install [oobabooga's  original repository](https://github.com/oobabooga/text-generation-webui) from oobabooga-windows.zip open start_windows.bat and follow the instructions until you can chat with a chatbot.

2. Now open cmd_windows.bat and clone this repo to extension:

   git clone [https://github.com/Kwisss/GoogleWordcloud]

   And install the requirements
   pip install -r GoogleWordcloud/requirements.txt
   
   ##Importand! You need to be in the right enviorment so opening a terminal with cmd_windows.bat is mandetory!


5.1 How to update main EdgeGPT (the one used by this extension)
   
If you have an old version, or you want to update the main script, open cmd_windows.bat, and run `pip install EdgeGPT`. To see current version, type `conda list EdgeGPT`.
   
6. In webui.py edit Line 164 add --chat --extensions GoogleWordcloud to make it look something like this:

python server.py --chat --extensions GoogleWordcloud

This runs the server with `--chat` and the `GoogleWordcloud` extension. If all goes well, you should see it reporting "ok"



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


## Weaknesses:
1. Most of the the character ignores the output, even if it is in his memory. Being still a new application, you are welcome to make tests to find your optimal result, be it clearing the conversation, changing the context around the output, or something else.
2. This code is dirty fork Written with ai help, it's doubtfull it will work in every enviorment ATM
3. Forking a Ai instructor is a roundabout way of copying a string in a searchbox
4. Google does not like beeing scraped so the scraping script has to be maintained

## Contributing
Pull requests, suggestions and bug reports are welcome, but as I'm not a programmer I can't guarantee I'll be of help.

## Credits and inspiration
 - GiusTex for Inspiring me to do this
 - acheong08 for his amazing default [EdgeGPT](https://github.com/acheong08/EdgeGPT).
 - The tutorial video by [Ai Austin](https://youtu.be/aokn48vB0kc), where he shows the code to install EdgeGPT and use it, and gave me a bit of inspiration.
