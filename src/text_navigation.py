# This file contains interfaces for navigation actions that can typically be executed within an editor. 
# These interfaces can then be implemented per editor and called directly from .talon files by 
# prefixing the method name with "user.".

import time
import re
from talon import ctrl, ui, Module, Context, actions, clip
import itertools
from _ast import Try

mod = Module()
@mod.action_class
class Actions:
    def jump_back():
        """Move the cursor to its previous location"""

    def jump_forward():
        """Move the cursor to its next location"""        

    def go_inside():
        """Go inside the selected method, variable or class"""

    def go_bracket():
        """Go to the next bracket or the matching bracket if the cursor is already on a bracket"""

    def go_last_error():
        """Go to the last error in the editor"""
        
    def go_next_error():
        """Go to the next error in the editor"""

    def go_next_occurrence():
        """Go to the next occurrence of the selected text"""

    def go_last_occurrence():
        """Go to the last occurrence of the selected text"""

    def go_last_method():
        """Go to the previous method definition"""

    def go_next_method():
        """Go to the next method definition"""
        
    def move_right_before(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and put the cursor before it"""
        before(re.escape(symbol), int(occurrence_number))
        
    def move_right_after(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and put the cursor after it"""
        after(ascii(symbol), int(occurrence_number))

    def move_left_before(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and put the cursor before it"""
        backwards_before(re.escape(symbol), occurrence_number)
        
    def move_left_after(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and put the cursor after it"""
        backwards_after(ascii(symbol), int(occurrence_number))        
                        
    def extend_right_before(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and extent the current selection until before it"""
        extend_right_before(ascii(symbol), int(occurrence_number))
                        
    def extend_right_after(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
        extend_right_after(ascii(symbol), int(occurrence_number))

    def extend_left_before(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until before it"""
        extend_left_before(ascii(symbol), int(occurrence_number))

    def extend_left_after(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
        extend_left_after(ascii(symbol), int(occurrence_number))
                                
def get_text_left():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text

def get_text_right():
    actions.edit.extend_line_end()
    text_right = actions.edit.selected_text()
    actions.edit.left()
    return text_right

def get_current_selection_size():
    with clip.revert():
        actions.edit.copy()
        time.sleep(0.1)
        current_selection_length = len(clip.get())
    return current_selection_length

def find_index_right(symbol, occurrence_number, text, start_index):
    i = start_index
    occurrence_count = 0
    while i < len(text) and occurrence_count != occurrence_number:
        if symbol[1] == text[i]:
            occurrence_count += 1
            if occurrence_count != occurrence_number:
                i += 1
        else:
            i += 1
    return i if occurrence_count == occurrence_number else -1

def find_index_left(symbol, occurrence_number, text, start_index):
    i = start_index
    occurrence_count = 0
    length = len(text) - 1
    while i < length and occurrence_count != occurrence_number:
        if symbol[1] == text[length - i]:
            occurrence_count += 1
            if occurrence_count != occurrence_number:
                i += 1
        else:
            i += 1
    return i if occurrence_count == occurrence_number else -1

def go_right(text, i):
    for j in range(0, i):
        actions.edit.right()

def go_left(text, i):
    if i > 0:
        for j in range(0, i):
            actions.edit.left()

def extend_right_or_reselect(current_selection_length, text, i):
    if i > 0:
        for j in range(0, i):
            actions.edit.extend_right()
    else:
        for j in range(0, current_selection_length):
            actions.edit.extend_right()

def extend_left_or_reselect(current_selection_length, text, i):
    if i > 0:
        for j in range(0, i):
            actions.edit.extend_left()
    else:
        for j in range(0, current_selection_length):
            actions.edit.extend_left()

def before(regex, occurrence_number):
    text = get_text_right()
    try:
        # pick the next interrater, Skip and number of occurrences, get an error iterator given the _WordRegex
        match = next(itertools.islice(re.finditer(regex, text), occurrence_number-1, None))
        #match = list(re.finditer(regex, text))[-occurrence_number]
    except StopIteration:
        return 
    go_right(text, match.start())

def after(symbol, occurrence_number):
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, 0)
    if i > 0:
        go_right(text, i+1)

def backwards_after(symbol, occurrence_number):
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, 0)
    go_left(text, i)
    
def backwards_before(regex, occurrence_number):
    text = get_text_left()
    try:
        # pick the next interrater, Skip and number of occurrences, get an error iterator given the _WordRegex
        #match = next(itertools.islice(re.finditer(regex, text), occurrence_number-1, None))
        match = list(re.finditer(regex, text))[-occurrence_number]
    except IndexError:
        return 
    go_left(text, len(text)- match.end())

#    text = get_text_left()
 #   i = find_index_left(symbol, occurrence_number, text, 0)
  #  go_left(text, i+1)

def extend_right_before(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.left()        
        #time.sleep(0.1)
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, current_selection_length)
    extend_right_or_reselect(current_selection_length, text, i)

def extend_right_after(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.left()
        #time.sleep(0.1)
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, current_selection_length)
    extend_right_or_reselect(current_selection_length, text, i+1)

def extend_left_before(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.right()
        #time.sleep(0.1)
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, current_selection_length)
    extend_left_or_reselect(current_selection_length, text, i+1)

def extend_left_after(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.right()
        #time.sleep(0.1)
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, current_selection_length)    
    extend_left_or_reselect(current_selection_length, text, i)
