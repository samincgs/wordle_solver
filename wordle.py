import os
import sys
import random

import customtkinter as ctk

PATH = 'data/'
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
MAX_GUESS_LENGTH = 5
MAX_GUESSES = 6

CORRECT_ANSWER = 'g'
SEMI_CORRECT_ANSWER = 'y'
WRONG_ANSWER = 'x'

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
    frequency = {w: 0 for w in ALL_LETTERS}
    best_word = None
    best_score = -1
    
    for word in word_list:
        for letter in set(word):
            if letter in frequency:
                frequency[letter] += 1

    for word in word_list:
        unique_letters = set(word)
        score = 0
        for letter in unique_letters:
            score += frequency[letter]
            
        if score > best_score:
            best_score = score
            best_word = word
            
    return best_word
   

def get_feedback(word):
    feedback = ''
    
    for i in range(len(word)):
        if word[i] == wordle_word[i]:
            feedback += CORRECT_ANSWER
        elif word[i] != wordle_word[i] and word[i] in wordle_word:
            feedback += SEMI_CORRECT_ANSWER
        elif word[i] != wordle_word[i]:
            feedback += WRONG_ANSWER
    return feedback

def apply_filter(word_list, current_word, feedback):
    kept_words = []
 
    for word in word_list:
        keep = True
        
        for i in range(len(word)):
            if feedback[i] == WRONG_ANSWER:
                if current_word[i] in word:
                    keep = False
                    break
                    
            if feedback[i] == CORRECT_ANSWER:
                if current_word[i] != word[i]:
                    keep = False
                    break
                
            if feedback[i] == SEMI_CORRECT_ANSWER:
                if current_word[i] == word[i] or current_word[i] not in word:
                    keep = False
                    break
                
        if keep:
            kept_words.append(word)
            
    return kept_words
    
def validate_input(input_type, question):
    allowed = set(CORRECT_ANSWER + WRONG_ANSWER + SEMI_CORRECT_ANSWER)
    
    while True:
        response = input(str(question)).strip().lower()
        if (len(response) != MAX_GUESS_LENGTH) or (not response.isalpha()):
            print(f'That is not correct. Please enter another ' + input_type)
            continue
        if input_type == 'feedback':
            if not set(response).issubset(allowed): 
                print('Your feedback has incorrect inputs.')
                continue
        break
    return response

def play_in_terminal(ai):
    global answered_correct, num_guess, initial_guess, filtered_list
            
    while (not answered_correct) and (num_guess < MAX_GUESSES):      
        if not ai:
            guess = validate_input(input_type='guess', question='What is your guess? ')
        else:
            guess = 'crane' if initial_guess else pick_word(filtered_list)
            
        num_guess += 1
        print(num_guess)
        if not ai:
            feedback = validate_input(input_type='feedback', question='What is your feedback? ')
        else:
            feedback = get_feedback(guess)  

        if initial_guess:
            filtered_list = apply_filter(answers_list, guess, feedback)
            initial_guess = False
        else: 
            filtered_list = apply_filter(filtered_list, guess, feedback)
            
        if (guess == wordle_word) or (feedback == 'ggggg'):
            answered_correct = True
            print(f'You got the wordle! The word is {guess}')
            print('It took you ' + str(num_guess) + ' guesses')
            break
        
        print(f'You guessed {guess}')
        print(f'The feedback is: {feedback}')
        print(f'Possible Answers:\n{filtered_list}')
    
    if num_guess >= MAX_GUESSES:
        print('You lost....')
    

def play_gui(ai):
    app = ctk.CTk()
    app.title("Wordle Helper")
    app.geometry("500x500")
    
    app.mainloop()

def play(ai=False, ui=False):
    if not ui:
        play_in_terminal(ai)
    else:
        play_gui(ai)
        
        
guessable_words_list, answers_list = get_words_lists(path=PATH)
wordle_word = random.choice(answers_list)
answered_correct = False
initial_guess = True
filtered_list = answers_list.copy()
num_guess = 0

try:
    play(ui=False)
except KeyboardInterrupt:
    sys.exit()