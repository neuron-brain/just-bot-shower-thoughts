# bot that makes showerthoughts
import random

import pytumblr

from grammar_checks import *
from sentences import sentence_structure

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    # insert keys here
)

# Make the request
client.info()

trigger_words = {
    "gun": "gun tw",
    "death": "death tw",
    "kill": "death tw",
    "food": "food tw",
    "life": "unreality tw",
    "dream": "unreality tw"
}

generate = int(input('how many posts boss?'))
# Creating a text post
for i in range(generate):
    post = random.choice(sentence_structure).generate()
    # Tags
    taglist = ['bot thoughts', 'shower thoughts',
               'bot generated post', 'thoughts from the shower']
    for word in post.split(' '):
        if word in trigger_words:
            taglist.append(trigger_words[word])
    # Send
    client.create_text('just-bot-shower-thoughts',
                       state='queue', body=post, tags=taglist)
