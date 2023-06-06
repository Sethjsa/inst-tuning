import spacy
import json
import sys
from tqdm import tqdm
import random
import nltk
from nltk.corpus import stopwords




nlp = spacy.load("en_core_web_lg")
# nlp.add_pipe('sentencizer')

texts = "Without quoting directly from the text go home. give me a summary of the history of the Key Lime Pie."

# docs = nlp(texts)


def remove_s(text):

    docs = nlp(text)

    s = [token.text for token in docs]

    sent = [word for word in s if not word in stopwords.words("english")]

    sentence = " ".join(sent)

    return sentence


def remove_pc(text, pc):

    docs = nlp(text)

    s = [token.text for token in docs]

    num_items_to_remove = int(len(s) * (pc / 100))

    indices_to_remove = random.sample(list(range(len(s))), num_items_to_remove)

    sent = [item for c, item in enumerate(s) if c not in indices_to_remove]

    sentence = " ".join(sent)

    return sentence

print(remove_s(texts))
sys.exit()

def reorder(text):

    docs = nlp(text)

    string = ""

    for sent in docs.sents:
        # print(sent)
        # [str(sent).strip() for sent in doc.sents]
        s = []
        docs = nlp(str(sent))
        for c, token in enumerate(docs):

            s.append({
            "token": token.text,
            "index":c,
            "tag":token.tag_,
            "dep":token.dep_,
            "head":token.head.text,
            "ancestors":[str(t) for t in token.ancestors],
            "children":[str(t) for t in token.children],
            "left_childs":[str(t) for t in token.lefts],
            "right_childs":[str(t) for t in token.rights],
            })
        
        sentence = swap_children(s)

        output = sorted(sentence, key=lambda x: x['index'])
        output_string = " ".join([d['token'] for d in output])
        string = string + " " + output_string

    return string


def swap_children(sentence):

    multi_child_words = []

    for word in sentence:
        if len(word["children"]) >= 2:
            child_indices = [w["index"] for w in sentence if w["token"] in word["children"]]
            multi_child_words.append([word["token"], word["dep"], child_indices, word["index"]])
    
    total = len(multi_child_words)

    root_children=[]
    for count, word in enumerate(multi_child_words):
        # reorder root children first
        if word[1] == "ROOT":
            new_indices = [len(sentence)-i for i in word[2]]
            for c, index in enumerate(word[2]):
                for w in sentence:
                    if w["index"] == index:
                        w["index"] = new_indices[c]
            children = word[2]
            root_children = children
            multi_child_words.pop(count)
        
    
    # print(children)
    second_children = []
    third_children = []
    fourth_children = []
    fifth_children = []
    
    while multi_child_words:
        
        for count, word in enumerate(multi_child_words):
            # iterate through root's children
            # breadth first - children of root, then 2nd order, then 3rd, etc.
            if word[3] in root_children:
                new_indices = [len(sentence)-i for i in word[2]]
                for c, index in enumerate(word[2]):
                    for w in sentence:
                        if w["index"] == index:
                            w["index"] = new_indices[c]
                second_children.extend(word[2])
                root_children.pop(root_children.index(word[3]))
                multi_child_words.pop(count)
            
            if word[3] in second_children:
                new_indices = [len(sentence)-i for i in word[2]]
                for c, index in enumerate(word[2]):
                    for w in sentence:
                        if w["index"] == index:
                            w["index"] = new_indices[c]
                third_children.extend(word[2])
                second_children.pop(second_children.index(word[3]))
                try:
                    if multi_child_words:
                        multi_child_words.pop(count)
                except:
                    if multi_child_words:
                        multi_child_words.pop(count-1)

            if word[3] in third_children:
                new_indices = [len(sentence)-i for i in word[2]]
                for c, index in enumerate(word[2]):
                    for w in sentence:
                        if w["index"] == index:
                            w["index"] = new_indices[c]
                fourth_children.extend(word[2])
                third_children.pop(third_children.index(word[3]))
                try:
                    if multi_child_words:
                        multi_child_words.pop(count)
                except:
                    try:
                        if multi_child_words:
                            multi_child_words.pop(count-1)
                    except: 
                        if multi_child_words:
                            multi_child_words.pop(count-2)
            
            else:
                new_indices = [len(sentence)-i for i in word[2]]
                for c, index in enumerate(word[2]):
                    for w in sentence:
                        if w["index"] == index:
                            w["index"] = new_indices[c]
                fifth_children.extend(word[2])
                # third_children.pop(third_children.index(word[3]))
                try:
                    if multi_child_words:
                        multi_child_words.pop(count)
                except:
                    try:
                        if multi_child_words:
                            multi_child_words.pop(count-1)
                    except: 
                        if multi_child_words:
                            multi_child_words.pop(count-2)
    # print(multi_child_words)
    # for count, word in enumerate(multi_child_words):
    #     print(word[3])
    #     if len(multi_child_words) < total and word[3] in children: 
    #         print("here")
    #         new_indices = [len(sentence)-i for i in child_indices]
    #         for c, index in enumerate(word[2]):
    #             for w in sentence:
    #                 if w["index"] == index:
    #                     w["index"] = new_indices[c]
    #         root_children.extend(word[2])
    #         children.pop(children.index(word[3]))
    #         multi_child_words.pop(count)
    
    # for count, word in enumerate(multi_child_words):
    #     if len(multi_child_words) < total and word[3] in children: 

    #         new_indices = [len(sentence)-i for i in indices]
    #         for c, index in enumerate(word[2]):
    #             for w in sentence:
    #                 if w["index"] == index:
    #                     w["index"] = new_indices[c]
    #         root_children.append(word[2])
    #         children.pop(children.index(word[3]))
    #         multi_child_words.pop(count)

    return sentence

# print(reorder(texts))


def shuffle_1(sentence):
    s = []
    docs = nlp(str(sentence))
    for c, token in enumerate(docs):
        s.append(token.text)
    random.shuffle(s)
    sentence = " ".join(s)
    return sentence

def shuffle_2(sentence):
    s = []
    docs = nlp(str(sentence))
    for c, token in enumerate(docs):
        s.append(token.text)

    sentence = [s[x:x+2] for x in range(0, len(s), 2)]
    random.shuffle(sentence)
    sentence = [" ".join(pair) for pair in sentence]
    sentence = " ".join(sentence)
    return sentence

def shuffle_3(sentence):
    s = []
    docs = nlp(str(sentence))
    for c, token in enumerate(docs):
        s.append(token.text)

    sentence = [s[x:x+3] for x in range(0, len(s), 3)]
    random.shuffle(sentence)
    sentence = [" ".join(pair) for pair in sentence]
    sentence = " ".join(sentence)
    return sentence
    

with open("/users/xbkx052/archive/dolly-db/data/dolly_data.json", "r") as f, open("/users/xbkx052/archive/dolly-db/data/dolly_data_shuf1_inst.json", "w") as g:
    dictionaries = json.load(f)
    rewrite = []
    for prompt in tqdm(dictionaries):
        prompt["instruction"] = shuffle_1(prompt["instruction"])
        # prompt["output"] = shuffle_1(prompt["output"])
        rewrite.append(prompt)
    json.dump(rewrite, g)

