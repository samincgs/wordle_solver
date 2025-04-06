import os
import random

PATH = 'data/'

def get_words_lists(path):
    
    guessable_words_list = []
    answers_list = []
    
    for file in os.listdir(path):
        file_path = path + file
        if file.endswith('.txt'):
            f = open(file_path)
            data = f.read().split('\n')
            f.close()
            if 'guess' in file_path:
                guessable_words_list.extend(data)
            if 'answer' in file_path:
                answers_list.extend(data)
                
    return guessable_words_list, answers_list
        

def pick_word(word_list):
    return word_list[0]
   

def get_feedback(word):
    feedback = ''
    
    for i in range(len(word)):
        if word[i] == wordle_word[i]:
            feedback += 'g'
        elif word[i] != wordle_word[i] and word[i] in wordle_word:
            feedback += 'y'
        elif word[i] != wordle_word[i]:
            feedback += 'x'
    return feedback

def apply_filter(word_list, current_word, feedback):
    kept_words = []
    
    for word in word_list:
        keep = True
        
        for i in range(len(word)):
            if feedback[i] == 'x':
                if current_word[i] in word:
                    keep = False
                    break
                    
            if feedback[i] == 'g':
                if current_word[i] != word[i]:
                    keep = False
                    break
                
            if feedback[i] == 'y':
                if current_word[i] != word[i] and current_word[i] not in word:
                    keep = False
                    break
                
        if keep:
            kept_words.append(word)
    
    return kept_words
    

def play(ai):
    pass

guessable_words_list, answers_list = get_words_lists(path=PATH)
wordle_word = random.choice(answers_list)

guessed_word = 'crane'

feedback = get_feedback(guessed_word)

print(f'Current Wordle Word: {wordle_word}')
print(f'Guessed Word {guessed_word}')

print(feedback)

xd = apply_filter(answers_list, guessed_word, feedback)

print(xd)