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
    pass
    

def play(ai=False, output=False):
    answered_correct = False
    initial_guess = True
        
    while not answered_correct:      
        if not ai:
            guess = input('What is your guess: ')
        else:
            guess = 'crane'
            
        if not ai:
            feedback = input('What is the colors of the answer: ')
        else: 
            feedback = get_feedback(guess)  
        
        if initial_guess:
            filtered_list = apply_filter(answers_list, guess, feedback)
            initial_guess = False
        else: 
            filtered_list = apply_filter(filtered_list, guess, feedback)
            
        if guess == wordle_word or feedback == 'ggggg':
            answered_correct = True
            print(f'You got the wordle! The word is {guess}')
            break
        
        if output:
            print(feedback)
            print(filtered_list)
            print(len(filtered_list))
        
        
        
        
        
        
        
        
        
        
        
        
    
        
    

guessable_words_list, answers_list = get_words_lists(path=PATH)
wordle_word = random.choice(answers_list)


play(ai=False, output=True)