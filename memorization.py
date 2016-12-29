
import os
#import tkinter as tk    #todo gui later
import numpy as np
import pandas as pd
import heapq

# class Application(tk.Frame):      #https://docs.python.org/3/library/tkinter.html
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
    dictionary, dictionary_option = select_dictionary()
    priority_dictionary_option = "Priorities For " + dictionary_option      #keeps the same file extension as that of the dictionary

    priority_dictionary_dataframe = load_priority_dictionary_dataframe(priority_dictionary_option)
    if priority_dictionary_dataframe is None:       #http://stackoverflow.com/questions/36217969/how-to-compare-pandas-dataframe-against-none-in-python
        priority_dictionary_dataframe = new_priority_dictionary_dataframe(dictionary)

    priority_dictionary_priority_queue = [tuple(x) for x in priority_dictionary_dataframe.values]   #http://stackoverflow.com/questions/9758450/pandas-convert-dataframe-to-array-of-tuples
    heapq.heapify(priority_dictionary_priority_queue)

    pref_num_options = 10
    while True:     #I have chosen to use an infinite while loop as opposed to infinite recursion, even though tail recursion should not stack overflow and even though recursion would be more parallel in style with the other select_() functions
        input_int = select_action()
        if input_int == 1:
            select_definition(priority_dictionary_priority_queue, pref_num_options)
        elif input_int == 2:
            priority_dictionary_dataframe = pd.DataFrame(priority_dictionary_priority_queue)
            print("You have knowledge score of " + str(sum(priority_dictionary_dataframe.ix[:,0])) + ". ")
        elif input_int == 3:
            priority_dictionary_dataframe = pd.DataFrame(priority_dictionary_priority_queue)
            save_priority_dictionary_dataframe(priority_dictionary_dataframe, priority_dictionary_option)
        elif input_int == 4:
            priority_dictionary_dataframe = pd.DataFrame(priority_dictionary_priority_queue)
            save_priority_dictionary_dataframe(priority_dictionary_dataframe, priority_dictionary_option)
            break

def new_priority_dictionary_dataframe(dictionary):
    num_terms = len(dictionary)
    #priorities = pd.DataFrame(np.zeros(num_terms)).astype(int)
    priorities = pd.DataFrame(np.random.choice(1 + int(np.ceil(0.01 * num_terms)), num_terms))
    priority_dictionary_dataframe = pd.concat([priorities, dictionary], axis=1)
    return priority_dictionary_dataframe

def save_priority_dictionary_dataframe(priority_dictionary_dataframe, priority_dictionary_option, priority_dictionaries_path = "priority_dictionaries"):
    priority_dictionary_option_path = priority_dictionaries_path + os.sep + priority_dictionary_option
    priority_dictionary_dataframe.to_csv(priority_dictionary_option_path, sep='\t', header=None, index=None)                                    #TODO understand encoding problem

def load_priority_dictionary_dataframe(priority_dictionary_option, priority_dictionaries_path = "priority_dictionaries"):
    priority_dictionary_option_path = priority_dictionaries_path + os.sep + priority_dictionary_option
    priority_dictionary_dataframe = None
    if os.path.isfile(priority_dictionary_option_path):
        priority_dictionary_dataframe = pd.read_csv(priority_dictionary_option_path, sep='\t', header=None, index_col=None, encoding="latin1")  #TODO understand encoding problem   #http://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
    return priority_dictionary_dataframe

def select_dictionary(dictionaries_path="dictionaries"):
    dictionary_options = os.listdir(dictionaries_path)

    def select_dictionary_prompt(dictionary_options):
        print("Enter a number between 1 and " + str(len(dictionary_options)) + " to select a dictionary to memorize. ")
        for df in range(0, len(dictionary_options)):
            print("[" + str(df+1) + "] " + dictionary_options[df])
    input_int = get_input_int(select_dictionary_prompt, dictionary_options)

    df = input_int - 1
    print("You have selected " + "\"[" + str(df+1) + "] " + dictionary_options[df] + "\". ")

    dictionary_option_path = "dictionaries" + os.sep + os.listdir("dictionaries")[df]
    dictionary = pd.read_csv(dictionary_option_path, sep='\t', header=None, index_col=None)
    return dictionary, dictionary_options[df]

def select_action():
    action_options = ["Next Word", "Check Knowledge Score", "Save", "Save & Quit"]

    def select_action_prompt(action_options):       #doesn't really need the get_input_int architecture, but uses it anyways
        print("Enter a number between 1 and " + str(len(action_options)) + " to select which action to do next. ")
        for a in range(0, len(action_options)):
            print("[" + str(a+1) + "] " + action_options[a])
    input_int = get_input_int(select_action_prompt, action_options)

    a = input_int - 1
    print("You have selected " + "\"[" + str(a+1) + "] " + action_options[a] + "\". ")

    return input_int

def select_definition(priority_dictionary_priority_queue, pref_num_options = 10):
    num_terms = len(priority_dictionary_priority_queue)
    num_options = min(pref_num_options, num_terms)

    definition_options_list = []                                                    #gets the options from the priority queue
    for o in range(0, num_options):                                                 #gets the options from the priority queue
        definition_options_list.append(heapq.heappop(priority_dictionary_priority_queue))
    definition_options = pd.DataFrame(definition_options_list)                      #gets the options from the priority queue

    random_sample = np.random.choice(10, size=10, replace=False)                    #randomizes the order of the answer choices
    definition_options = definition_options.ix[random_sample]                       #randomizes the order of the answer choices
    target_o = np.random.choice(10)

    def select_definition_prompt(definition_options):
        print("Enter a number between 1 and " + str(num_options) + " to select the definition of " + definition_options.ix[target_o, 1] + ". ")
        for o in range(0, num_options):
            print("[" + str(o+1) + "] " + definition_options.ix[o, 2])
    input_int = get_input_int(select_definition_prompt, definition_options)

    o = input_int - 1
    print("You have selected " + "\"[" + str(o+1) + "] " + definition_options.ix[o, 2] + "\". ")

    if o == target_o:
        print("Correct! ")
        definition_options.ix[target_o,0] += 1 + int(np.ceil(0.01 * num_terms))     #updates the priority of the target option
    else:
        print("Incorrect. The correct definition of \"" + definition_options.ix[target_o, 1] + "\" was \"" + definition_options.ix[target_o, 2] + "\". ")
        print("You had selected the definition of \"" + definition_options.ix[o, 1] + "\", \"" + definition_options.ix[o, 2] + "\". ")
        definition_options.ix[target_o,0] += 1                                      #updates the priority of the target option

    for o in range(0, num_options):                                                 #pushes the options back onto the queue
        definition_option = (definition_options.ix[o,0], definition_options.ix[o,1], definition_options.ix[o,2])
        heapq.heappush(priority_dictionary_priority_queue, definition_option)       #pushes the options back onto the queue

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