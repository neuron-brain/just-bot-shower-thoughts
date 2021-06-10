# bot that makes showerthoughts
import pytumblr
import random
import word_lists
from word_lists import lists_noun
from word_lists import lists_verb
from word_lists import lists_adj
from sentences import sentence_structure

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    #insert keys here
)

# Make the request
client.info()
# get lists for nouns, adjectives and verbs

trigger_words = ['gun', 'death', 'kill', 'food', 'life', 'dream']
trigger_warn = ['gun tw', 'death tw', 'death tw', 'food tw', 'unreality tw', 'unreality tw']

generate = int(input('how many posts boss?'))
# Creating a text post
for i in range(0, generate):
    taglist = ['bot thoughts', 'shower thoughts', 'bot generated post', 'thoughts from the shower']
    post = random.choice(sentence_structure).split(' ')
    for i in range(len(post)):
        word = post[i]
        if word in trigger_words:
            x = trigger_words.index(word)
            taglist.append(trigger_warn[x])
    posts = ' '.join(post)
    client.create_text('just-bot-shower-thoughts', state='queue', body=posts,
                       tags=taglist)

