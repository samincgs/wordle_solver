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
        

def pick_word(word_list): # add letter frequency
    frequency = {w: 0 for w in 'abcdefghijklmnopqrstuvwxyz'}
    
    for word in word_list:
        for letter in set(word):
            if letter in frequency:
                frequency[letter] += 1
                
    best_word = None
    best_score = -1
    
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
            guess = input('What is your guess: ').strip().lower()
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
        
        print(f'You guessed {guess}')
        print(f'The feedback is: {feedback}')
        
        if output:
            print(filtered_list)
            print(len(filtered_list))
        
        
guessable_words_list, answers_list = get_words_lists(path=PATH)
wordle_word = random.choice(answers_list)


x = pick_word(answers_list)

print(x)