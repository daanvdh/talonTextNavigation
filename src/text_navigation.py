import time
import re
from talon import ctrl, ui, Module, Context, actions, clip
import itertools
from _ast import Try

ctx = Context()
mod = Module()

mod.list("cursor_location", desc="words to start dictating prose, and the formatter they apply")
mod.list("direction", desc="words to start dictating prose, and the formatter they apply")
mod.list("navigation_option", desc="words to start dictating prose, and the formatter they apply")
ctx.lists["self.cursor_location"] = {"before", "after"}
ctx.lists["self.direction"] = {"left", "right"}
ctx.lists["self.navigation_option"] = {"go", "extend", "select", "delete", "cut"}

@mod.capture(rule="{self.cursor_location}")
def cursor_location(m) -> str:
    "One directional arrow key"
    return m.cursor_location
@mod.capture(rule="{self.direction}")
def direction(m) -> str:
    "One directional arrow key"
    return m.direction
@mod.capture(rule="{self.navigation_option}")
def navigation_option(m) -> str:
    "One directional arrow key"
    return m.navigation_option

@mod.action_class
class Actions:
    def navigation(navigation_option: str, direction: str, cursor_location: str, text: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and put the cursor before it"""
        option = navigation_option+" "+cursor_location if navigation_option=="go" else navigation_option
        navigation(option, direction, re.escape(text), int(occurrence_number))

    def move_right_before(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and put the cursor before it"""
#        before(re.escape(symbol), int(occurrence_number))
        
    def move_right_after(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and put the cursor after it"""
#        after(ascii(symbol), int(occurrence_number))

    def move_left_before(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and put the cursor before it"""
#        backwards_before(re.escape(symbol), occurrence_number)
        
    def move_left_after(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and put the cursor after it"""
#        backwards_after(ascii(symbol), int(occurrence_number))        
                        
    def extend_right_before(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and extent the current selection until before it"""
#        extend_right_before(ascii(symbol), int(occurrence_number))
                        
    def extend_right_after(symbol: str, occurrence_number: int):
        """go right until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
#        extend_right_after(ascii(symbol), int(occurrence_number))

    def extend_left_before(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until before it"""
#        extend_left_before(ascii(symbol), int(occurrence_number))

    def extend_left_after(symbol: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
#        extend_left_after(ascii(symbol), int(occurrence_number))

    def select_right(text: str, occurrence_number: int):
        """go left until you find the given symbol for the occurrence_number-th time and extent the current selection until after it"""
#        select_right(re.escape(text), occurrence_number)
                                
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

def go_right(i):
    for j in range(0, i):
        actions.edit.right()

def go_left(i):
    for j in range(0, i):
        actions.edit.left()

def extend_left(i):
    for j in range(0, i):
        actions.edit.extend_left()

def extend_right(i):
    for j in range(0, i):
        actions.edit.extend_right()

def navigation(navigation_option, direction, regex, occurrence_number):
    if direction == "left":
        navigate_left(navigation_option, regex, occurrence_number)
    else:
        navigate_right(navigation_option, regex, occurrence_number)

def navigate_left(navigation_option, regex, occurrence_number):
    current_selection_length = get_current_selection_size()
    if current_selection_length > 0: 
        actions.edit.right()
    try:
        text = get_text_left()
        subtext = text if current_selection_length <= 0 else text[:-current_selection_length] 
        match = list(re.finditer(regex, subtext, re.IGNORECASE))[-occurrence_number]
        start = match.start() 
        end = match.end()
        if navigation_option == "go before":
            go_left(len(text)- start)                
        elif navigation_option == "go after":
            go_left(len(text)- end)
        elif navigation_option == "select":
            go_left(len(text)- end)                
            extend_left(end-start)
        elif navigation_option == "delete":
            go_left(len(text)- end)                
            extend_left(end-start)
            actions.edit.delete()
        elif navigation_option == "cut":
            go_left(len(text)- end)                
            extend_left(end-start)
            actions.edit.cut()
        elif navigation_option == "extend":
            extend_left(len(text) - match.start())
    except IndexError:
        extend_left(current_selection_length)
        return 
    return

def navigate_right(navigation_option, regex, occurrence_number):
    current_selection_length = get_current_selection_size()                
    if current_selection_length > 0: 
        actions.edit.left()
    try:
        text = get_text_right()
        sub_text = text[current_selection_length:]
        # pick the next interrater, Skip n number of occurrences, get an iterator given the Regex
        match = next(itertools.islice(re.finditer(regex, sub_text, re.IGNORECASE), occurrence_number-1, None))
        start = current_selection_length + match.start() 
        end = current_selection_length + match.end() 
        if navigation_option == "go before":
            go_right(start)
        elif navigation_option == "go after":
            go_right(end)
        elif navigation_option == "select":
            go_right(start)
            extend_right(end-start)
        elif navigation_option == "delete":
            go_right(start)
            extend_right(end-start)
            actions.edit.delete()
        elif navigation_option == "cut":
            go_right(start)
            extend_right(end-start)
            actions.edit.cut()
        elif navigation_option == "extend":
            extend_right(end)
    except StopIteration:
        extend_right(current_selection_length)
        return
    return 

    