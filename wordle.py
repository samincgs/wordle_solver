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
    global answered_correct, num_guess, initial_guess, filtered_list

    def submit():
        global answered_correct, num_guess, initial_guess, filtered_list
        allowed = set(CORRECT_ANSWER + WRONG_ANSWER + SEMI_CORRECT_ANSWER)
        left_textbox.configure(state='normal')
        right_textbox.configure(state='normal')
        
        left_textbox.delete('0.0', 'end')
        
        if not ai:
            guess = guess_str.get()
        else:
            guess_str.set('stare' if initial_guess else pick_word(filtered_list))
            guess = guess_str.get()
            
        if not ai:
            feedback = feedback_str.get()
        else:
            feedback_str.set(get_feedback(guess))
            feedback = feedback_str.get()
        
        if (len(guess) != MAX_GUESS_LENGTH) or (not guess.isalpha()):
            left_textbox.insert('0.0', 'Guess is invalid. Must be correct length, only letters, and allowed characters.')
            return
        
        if (len(feedback) != MAX_GUESS_LENGTH) or (not feedback.isalpha()) or (not set(feedback).issubset(allowed)):
            left_textbox.insert('0.0', 'Feedback is invalid. Must be correct length, only letters, and allowed characters.')
            return
        
        num_guess += 1
        
        if initial_guess:
            filtered_list = apply_filter(answers_list, guess, feedback)
            initial_guess = False
        else: 
            filtered_list = apply_filter(filtered_list, guess, feedback)
        
        right_textbox.insert('end', f'{num_guess}. {guess}\n')
        
        if (guess == wordle_word) or (feedback == 'ggggg'):
            answered_correct = True
            left_textbox.insert('0.0', f'You got the wordle! The word is {guess}\nIt took you ' + str(num_guess) + ' guesses')
            return
        
        
        left_textbox.insert('0.0', f'Possible Options:\n\n{'\n'.join(filtered_list)}')
        left_textbox.configure(state='disabled')
        right_textbox.configure(state='disabled')
        
        if ai:
            submit_button.invoke()


    app = ctk.CTk()
    app.title("Wordle Helper")
    app.geometry("500x500")

    app.columnconfigure(0, weight=1)
    
    guess_str = ctk.StringVar()
    feedback_str = ctk.StringVar()

    guess_label = ctk.CTkLabel(app, text="What is your guess?")
    guess_entry = ctk.CTkEntry(app, placeholder_text="Guess", textvariable=guess_str)

    feedback_label = ctk.CTkLabel(app, text="Enter feedback:")
    feedback_entry = ctk.CTkEntry(app, placeholder_text="Feedback", textvariable=feedback_str)

    submit_button = ctk.CTkButton(app, text="Submit", command=submit)

    split_frame = ctk.CTkFrame(app)
    split_frame.columnconfigure(0, weight=7)
    split_frame.columnconfigure(1, weight=3)
    split_frame.rowconfigure(0, weight=1)
    
    left_textbox = ctk.CTkTextbox(split_frame, wrap="word", state='normal')
    right_textbox = ctk.CTkTextbox(split_frame, wrap="word", width=20, state='normal')
    right_textbox.insert('end', f'All Guesses:\n\n')
    
    
    split_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
    
    guess_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(30,0), sticky="w")
    guess_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,20), sticky="ew")

    feedback_label.grid(row=2, column=0, columnspan=2, padx=20, sticky="w")
    feedback_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=(0,20), sticky="ew")

    submit_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(10,20), sticky="ew")
    
    left_textbox.grid(row=0, column=0, sticky="nsew")

    right_textbox.grid(row=0, column=1, sticky="nsew")
    
    if ai:
        submit_button.invoke()
    
    app.mainloop()

def play(ai=False, ui=False):
    if not ui:
        play_in_terminal(ai)
    else:
        play_gui(ai)
        
        
guessable_words_list, answers_list = get_words_lists(path=PATH)
wordle_word = 'theft'
answered_correct = False
initial_guess = True
filtered_list = answers_list.copy()
num_guess = 0

try:
    play(ui=True, ai=False)
except KeyboardInterrupt:
    sys.exit()