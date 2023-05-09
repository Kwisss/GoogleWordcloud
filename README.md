# ⚠ 🕱 🕱 WORK IN PROGRESS 🕱 🕱 ⚠

| Feature | From | Status | Function |
| --- | --- | --- | --- |
| Inject Google Wordcloud | - | ✅ | Get it working |
| Lose nltk or multidict | - | ❌ | Reduce libarys |
| Clean up script| - | ❌ | Improve readability |
| Integrate scrub.py | - | ❌ | Improve readability |
| Keyword frequency selector | - | ❌ | Usability improvement |
| Keyword exclusion input box | - | ❌ | Usability improvement |
| Better context templates  | - | ❌ | Usability improvement |
| Prompt -> Search manipulation | - | ❌ | Result improvement |

### Example without GoogleWordcloud on the left, and with GoogleWordcloud turned on on the right:
##
![googlecloud](https://github.com/Kwisss/GoogleWordcloud/assets/68794249/1adbc11e-00cf-42c1-8f88-8c712dca38b4)



## GoogleWordcloud
Extension for Text Generation Webui forked from [EdgeGPT](https://github.com/GiusTex/EdgeGPT) by GiusTex which in turn forked (https://github.com/acheong08/EdgeGPT) by acheong08, a reverse engineered API of Microsoft's Bing Chat AI.

This project copys the prompt to search Google, which will scrape the results and deliver a keyword wordcloud to your bot.

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
> Start the prompt with Hey google, the default keyword to activate Google when you need, and Google will search and give an answer, that will be fed to the 
  character memory before it answers you.


Debug buttons
 > If the bot answer does not seem to change turn "Show Google Output" on to show the Google output in the webui, sometimes it doesn't answer well and it needs better search words.
  
  You can also print in the console other prompt parts (user input, whole prompt, "raw" Google output, Google output + custom context):
  
![googlecloud3](https://github.com/Kwisss/GoogleWordcloud/assets/68794249/7079eaf9-fc0d-46e7-812a-487c758cdcae)

Chat-mode
> It works with "chat, streaming, non-streaming" modes (the ones I have tested).

Change keyword
> Change the Google activation word within the webui, from EdgeGPT options (punctuation marks are not supported, they give error).

Edit Google context
> Now you can customize the context around the Google output.

Overwrite Activation Word
> Added Overwrite Activation Word, while this is turned on Google will always answer you without the need of an activation word, if you don't want to mess your prompt 
  with a keyword that doesn't fit in.


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
