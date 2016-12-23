
import os
#import tkinter as tk    #todo gui later
import numpy as np
import pandas as pd
import heapq

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         tk.Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")
#
#         self.QUIT = tk.Button(self, text="QUIT", fg="red",
#                                             command=root.destroy)
#         self.QUIT.pack(side="bottom")
#
#     def say_hi(self):
#         print("hi there, everyone!")
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()

def main():
    dictionary = select_dictionary("dictionaries")    #TODO also get the name of dictionary to create name of a save file

    priority_dictionary = pd.DataFrame(np.zeros(dictionary.shape[0])).astype(int)    #TODO get_priorities() from save file

    priority_dictionary_dataframe = pd.concat([priority_dictionary, dictionary], axis=1)
    priority_dictionary_priority_queue = [tuple(x) for x in priority_dictionary_dataframe.values]
    heapq.heapify(priority_dictionary_priority_queue)

    while True:     #TODO termination and set_priorities() to save file
        select_definition(priority_dictionary_priority_queue)

def select_dictionary(dictionaries_path):
    dictionary_options = os.listdir(dictionaries_path)

    def select_dictionary_prompt(dictionary_options):
        print("Enter a number between 1 and " + str(len(dictionary_options)) + " to select a dictionary to memorize. ")
        for df in range(0, len(dictionary_options)):
            print("[" + str(df+1) + "] " + dictionary_options[df])
    input_int = get_input_int(select_dictionary_prompt, dictionary_options)

    df = input_int - 1
    print("You have selected " + "[" + str(df+1) + "] " + dictionary_options[df] + ". ")
    dictionary_path = "dictionaries" + os.sep + os.listdir("dictionaries")[df]
    dictionary = pd.read_csv(dictionary_path, sep='\t', header=None)
    return dictionary

def select_definition(priority_dictionary_priority_queue):
    num_terms = len(priority_dictionary_priority_queue)
    pref_num_options = 10
    num_options = min(pref_num_options, num_terms)
    definition_options_list = []
    for o in range(0, num_options):
        definition_options_list.append(heapq.heappop(priority_dictionary_priority_queue))
    definition_options = pd.DataFrame(definition_options_list)

    random_sample = np.random.choice(10, size=10, replace=False)
    definition_options = definition_options.ix[random_sample]
    target_o = np.random.choice(10)

    def select_definition_prompt(definition_options):
        print("Enter a number between 1 and " + str(num_options) + " to select the definition of " + definition_options.ix[target_o, 1] + ". ")
        for o in range(0, num_options):
            print("[" + str(o+1) + "] " + definition_options.ix[o, 2])
    input_int = get_input_int(select_definition_prompt, definition_options)

    o = input_int - 1
    print("You have selected " + "[" + str(o+1) + "] " + definition_options.ix[o, 2] + ". ")
    if o == target_o:
        print("Correct! ")
        definition_options.ix[o,0] += 1 + int(np.ceil(0.01 * num_terms))
    else:
        print("Incorrect. The correct option was " + definition_options[target_o, 2] + ". ")
        definition_options.ix[o,0] += 1

    for o in range(0, num_options):
        definition_option = (definition_options.ix[o,0], definition_options.ix[o,1], definition_options.ix[o,2])
        heapq.heappush(priority_dictionary_priority_queue, definition_option)

def get_input_int(prompt, options):
    num_options = len(options)
    while True:
        prompt(options)
        try:
            input_str = input()
            input_int = int(input_str)
            if input_int < 1 or input_int > num_options:
                int("one")  #go to except
            return input_int
        except:
            print("Your input string \"" + input_str + "\" is not a number between 1 and " + str(num_options) + ". ")

if __name__ == "__main__":
    main()