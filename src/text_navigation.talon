
#column navigation    
#Consider renaming before and after to till and past
#[go] [right] before <user.symbol_key> [<number>]: user.move_right_before(symbol_key, number or 1)
#[go] [right] after <user.symbol_key> [<number>]: user.move_right_after(symbol_key, number or 1)
#[go] left [before] <user.symbol_key> [<number>]: user.move_left_before(symbol_key, number or 1)
#[go] left after <user.symbol_key> [<number>]: user.move_left_after(symbol_key, number or 1)
#extend [right] before <user.symbol_key> [<number>]: user.extend_right_before(symbol_key, number or 1)
#extend [right] [after] <user.symbol_key> [<number>]: user.extend_right_after(symbol_key, number or 1)
#extend left [before] <user.symbol_key> [<number>]: user.extend_left_before(symbol_key, number or 1)
#extend left after <user.symbol_key> [<number>]: user.extend_left_after(symbol_key, number or 1)

# text navigation
[<user.navigation_option>] [<user.direction>] <user.cursor_location> <user.text> [<number>]:
	user.navigation(navigation_option or "go", direction or "right", cursor_location, text, number or  1)
<user.navigation_option> [<user.direction>] <user.text> [<number>]:
	user.navigation(navigation_option, direction or "right", "after", text, number or  1)
	
# symbol navigation
[<user.navigation_option>] [<user.direction>] <user.cursor_location> <user.symbol_key> [<number>]:
	user.navigation(navigation_option or "go", direction or "right", cursor_location, symbol_key, number or  1)
<user.navigation_option> [<user.direction>] <user.symbol_key> [<number>]:
	user.navigation(navigation_option, direction or "right", "after", symbol_key, number or  1)

# alphabet navigation
[<user.navigation_option>] [<user.direction>] <user.cursor_location> <user.letter> [<number>]:
	user.navigation(navigation_option or "go", direction or "right", cursor_location, letter, number or  1)
<user.navigation_option> [<user.direction>] <user.letter> [<number>]:
	user.navigation(navigation_option, direction or "right", "after", letter, number or  1)	

# number navigation
[<user.navigation_option>] [<user.direction>] <user.cursor_location> <number>:
	user.navigation(navigation_option or "go", direction or "right", cursor_location, "{number}", 1)
<user.navigation_option> [<user.direction>] <number>:
	user.navigation(navigation_option, direction or "right", "after", "{number}", 1)
	