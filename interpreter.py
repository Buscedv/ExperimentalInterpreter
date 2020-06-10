import sys, re


class RawCode:
	def __init__(self, code):
		self.code = code
		self.index = -1

	def __repr__(self):
		return self.code

	def next_char(self):
		if self.index + 1 < len(self.code):
			return self.code[self.index + 1]
		return None

	def move_to_next_char(self):
		self.index += 1

	def current_char(self):
		return self.code[self.index]


class Token:
	def __init__(self, typ, val):
		self.typ = typ
		self.val = val

	def __repr__(self):
		return 'Type: ' + self.typ + '\nValue: ' + self.val


class Tokens:
	def __init__(self, tokens):
		self.tokens = tokens
		self.index = -1

	def __repr__(self):
		res = ''

		for token in self.tokens:
			res += repr(token) + '\n\n'

		return res

	def next_token(self):
		if self.index + 1 < len(self.tokens):
			return self.tokens[self.index + 1]
		return None

	def move_to_next_token(self):
		self.index += 1

	def move_back_to_token(self):
		self.index -= 1

	def current_token(self):
		return self.tokens[self.index]


class Ast:
	def __init__(self, iterator):
		self.tree = iterator

	def __repr__(self):
		res = ''
		for thing in self.tree:
			res += repr(thing) + '\n\n'

		return res


def scan_while_re(to_scan, allowed_regex):
	res = to_scan.current_char()

	while to_scan.next_char() is not None and re.match(allowed_regex, to_scan.next_char()):
		to_scan.move_to_next_char()
		res += to_scan.current_char()

	return res


def scan_while(code, allowed):
	res = code.current_char()

	while code.next_char() in allowed:
		code.move_to_next_char()
		res += code.current_char()

	return res


def scan_until(to_scan, until):
	res = ''

	while to_scan.next_char() is not None and to_scan.next_char() not in until:
		to_scan.move_to_next_char()
		res += to_scan.current_char()

	to_scan.move_to_next_char()

	return res


def lex(code):
	numbers = '0123456789.'
	literals = '+-*/%'
	special_literals = '=(),'
	ignored = ' \t'
	string_start_end = '"\''
	word_regex = r'[_a-zA-Z]'

	tokens = []

	while code.next_char() is not None:
		code.move_to_next_char()
		char = code.current_char()

		if char in ignored:
			continue
		if char == '\n':
			tokens.append(Token('line', ''))
		elif char in numbers:
			tokens.append(Token('number', scan_while(code, numbers)))
		elif char in literals:
			tokens.append(Token('literal', scan_while(code, numbers)))
		elif char in special_literals:
			tokens.append(Token('special_literal', char))
		elif char in string_start_end:
			tokens.append(Token('string', scan_until(code, string_start_end)))
		elif re.match(word_regex, char):
			tokens.append(Token('word', scan_while_re(code, word_regex)))

	return tokens


def next_expr(tokens, prev):
	token = tokens.current_token()
	token_typ = token.typ
	token_val = token.val

	if token_typ == 'line':
		return prev

	tokens.move_to_next_token()

	if token_typ in ['number', 'string', 'word']:
		return next_expr(tokens, token)
	elif token_typ == 'literal':
		nxt = next_expr(tokens, None)
		return next_expr(tokens, ['operation', token_val, prev, nxt])
	elif token_typ == 'special_literal':
		if token_val == '=':
			nxt = next_expr(tokens, None)
			return next_expr(tokens, ['assignment', prev, nxt])
		elif token_val == '(':
			args = []
			while tokens.next_token() is not None:
				nxt = next_expr(tokens, None)
				if nxt is not None:
					args.append(nxt)
			return ['call', prev, args]
		elif token_val in '),':
			return prev


def parse(tokens):
	while tokens.next_token() is not None:
		tokens.move_to_next_token()
		expression = next_expr(tokens, None)

		if expression is not None:
			yield expression


file_name = sys.argv[1]

with open(file_name) as f:
	raw_code = f.read()

result = Ast(parse(Tokens(lex(RawCode(raw_code)))))
print(result)
