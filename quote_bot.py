# bot that makes showerthoughts
import pytumblr
import random


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
    sentence_structure = [f"{random.choice(lists_noun)} is just a {random.choice(lists_noun)}",
                          f'a {random.choice(lists_noun)} is like a {random.choice(lists_noun)} but if it was '
                          f'{random.choice(lists_adj)}', f'if {random.choice(lists_noun)} had a '
                                                         f'{random.choice(lists_noun)} then more {random.choice(lists_noun)}'
                                                         f' would {random.choice(lists_verb)} it',
                          f'life is a {random.choice(lists_verb)} {random.choice(lists_noun)}', f"you know when you're "
                          f"{random.choice(lists_verb)}ing your {random.choice(lists_noun)}, "
                         f"you're {random.choice(lists_verb)}ing your {random.choice(lists_noun)}", f'why do we have '
                                    f'{random.choice(lists_adj)} {random.choice(lists_noun)} if we have {random.choice(lists_noun)}?',
                          f'if you become a {random.choice(lists_noun)} then you are legally allowed to {random.choice(lists_verb)} '
                          f'{random.choice(lists_noun)}s', f'{random.choice(lists_noun)} has big {random.choice(lists_noun)} energy']
    post = random.choice(sentence_structure).split(' ')
    for i in range(len(post)):
        word = post[i]
        if word in trigger_words:
            x = trigger_words.index(word)
            taglist.append(trigger_warn[x])
    posts = ' '.join(post)
    client.create_text('just-bot-shower-thoughts', state='queue', body=posts,
                       tags=taglist)

