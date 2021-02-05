import time
import re
from talon import ctrl, ui, Module, Context, actions, clip
import itertools
from _ast import Try

mod = Module()
@mod.action_class
class Actions:
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

    def select_right(text: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
        select_right(re.escape(text), occurrence_number)
                                
def get_text_left():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text

def get_text_right():
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text

def get_current_selection_size():
    return len(actions.edit.selected_text())

# to do: remove method
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

# to do: remove method
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

def go_right(i):
    for j in range(0, i):
        actions.edit.right()

def go_left(i):
    for j in range(0, i):
        actions.edit.left()


def extend_right(i):
    for j in range(0, i):
        actions.edit.extend_right()

def extend_right_or_reselect(current_selection_length, i):
    if i > 0:
        extend_right(i)
    else:
        for j in range(0, current_selection_length):
            actions.edit.extend_right()

def extend_left_or_reselect(current_selection_length, i):
    if i > 0:
        for j in range(0, i):
            actions.edit.extend_left()
    else:
        for j in range(0, current_selection_length):
            actions.edit.extend_left()

def before(regex, occurrence_number):
    text = get_text_right()
    try:
        # 2 do: remove comments
        # pick the next interrater, Skip and number of occurrences, get an error iterator given the _WordRegex
        match = next(itertools.islice(re.finditer(regex, text), occurrence_number-1, None))
    except StopIteration:
        return 
    go_right(match.start())

def after(symbol, occurrence_number):
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, 0)
    if i > 0: go_right(i+1)

def backwards_after(symbol, occurrence_number):
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, 0)
    if i > 0: go_left(i)
    
def backwards_before(regex, occurrence_number):
    text = get_text_left()
    try:
        match = list(re.finditer(regex, text))[-occurrence_number]
    except IndexError:
        return 
    go_left(len(text)- match.end())

def extend_right_before(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.left()        
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, current_selection_length)
    extend_right_or_reselect(current_selection_length, i)

def extend_right_after(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.left()
    text = get_text_right()
    i = find_index_right(symbol, occurrence_number, text, current_selection_length)
    extend_right_or_reselect(current_selection_length, i+1)

def extend_left_before(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.right()
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, current_selection_length)
    extend_left_or_reselect(current_selection_length, i+1)

def extend_left_after(symbol, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.right()
    text = get_text_left()
    i = find_index_left(symbol, occurrence_number, text, current_selection_length)    
    extend_left_or_reselect(current_selection_length, i)

def select_right(regex, occurrence_number):
    text = get_text_right()
    try:
        match = next(itertools.islice(re.finditer(regex, text), occurrence_number-1, None))
    except StopIteration:
        return 
    go_right(match.start())
    extend_right(match.end()-match.start())