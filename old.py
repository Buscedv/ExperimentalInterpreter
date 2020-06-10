import sys, re
#
# class Tokens:
# 	def __init__(self, tokens):
# 		self.tokens = []
#
# 		for token in tokens:
# 			self.tokens.append(token)
#
# 		self.index = -1
#
# 	def __repr__(self):
# 		return self.tokens
#
# 	def next(self):
# 		if self.index + 1 < len(self.tokens):
# 			return self.tokens[self.index + 1]
# 		return None
#
# 	def move_next(self):
# 		if self.next() is not None:
# 			self.index += 1
#
# 	def current(self):
# 		return self.tokens[self.index]
#
#
# class Token:
# 	def __init__(self, type, value):
# 		self.type = type
# 		self.value = value
#
# 	def __repr__(self):
# 		return 'type: ' + self.type + ',\nvalue: ' + self.value + '\n'
#
#
# class SourceLine:
# 	def __init__(self, line):
# 		self.line = line
# 		self.index = -1
#
# 	def next(self):
# 		if self.index + 1 < len(self.line):
# 			return self.line[self.index + 1]
# 		return None
#
# 	def move_next(self):
# 		if self.next() is not None:
# 			self.index += 1
#
# 	def current(self):
# 		return self.line[self.index]
#
#
# def scan_until(to_scan, until, ignore_until):
# 	res = to_scan.current()
#
# 	if ignore_until:
# 		res = ''
#
# 	while to_scan.next() is not None and to_scan.next() not in until:
# 		to_scan.move_next()
# 		res += to_scan.current()
#
# 	if ignore_until:
# 		to_scan.move_next()
#
# 	return res
#
#
# def scan_while(to_scan, allowed):
# 	res = to_scan.current()
#
# 	while to_scan.next() is not None and to_scan.next() in allowed:
# 		to_scan.move_next()
# 		res += to_scan.current()
#
# 	return res
#
#
# def scan_while_re(to_scan, allowed_regex):
# 	res = to_scan.current()
#
# 	while to_scan.next() is not None and re.match(allowed_regex, to_scan.next()):
# 		to_scan.move_next()
# 		res += to_scan.current()
#
# 	return res
#
#
# def lex(line):
# 	line = SourceLine(line)
#
# 	ignored = ' \t'
# 	string_repr = '"\''
# 	numbers = '0123456789.'
# 	literals = '+-*/%'
# 	word_regex = r'[_a-zA-Z]'
#
# 	while line.next() is not None:
# 		line.move_next()
#
# 		char = line.current()
#
# 		if char in string_repr:
# 			yield Token('string', scan_until(line, string_repr, True))
# 		elif char in numbers:
# 			yield Token('number', scan_while(line, numbers))
# 		elif char in literals:
# 			yield Token('literal', scan_while(line, literals))
# 		elif re.match(word_regex, char):
# 			yield Token('word', scan_while_re(line, word_regex))
# 		elif char == '\n':
# 			yield Token('line', '')
# 		elif char == '=':
# 			yield Token('equals', '')
# 		elif char == '(':
# 			yield Token('lparen', '')
# 		elif char == ')':
# 			yield Token('rparen', '')
#
#
# def next_expr(tokens, prev):
# 	tokens.move_next()
#
# 	token = tokens.current()
# 	token_type = token.type
# 	token_val = token.value
#
# 	if token_type == 'line':
# 		return prev
# 	elif token_type in ['word', 'string', 'number']:
# 		if prev is None:
# 			return next_expr(tokens, (token_type, token_val))
# 	elif token_type == 'literal':
# 		nxt = next_expr(tokens, None)
# 		return next_expr(tokens, ("operation", token_val, prev, nxt))
# 	elif token_type == 'equals':
# 		if prev is not None:
# 			if prev[0] == 'word':
# 				nxt = next_expr(tokens, None)
# 				return next_expr(tokens, ("assignment", prev, nxt))
#
#
# def parse(tokens):
# 	tokens = Tokens(tokens)
#
# 	while tokens.next() is not None:
# 		tokens.move_next()
#
# 		expr = next_expr(tokens, None)
#
# 		if expr is not None:
# 			yield expr
#
# file_name = sys.argv[1]
# with open(file_name) as f:
# 	source = f.read()
#
# tokens = lex(source)
#
# parsed = parse(tokens)
# # for thing in parsed:
# # 	print(thing)


class Operation:
	def __init__(self, typ, left, right):
		self.typ = typ
		self.left = left
		self.right = right

	def __repr__(self):
		return self.left + self.typ + self.right


class Source:
	def __init__(self, source):
		self.source = source
		self.index = -1

	def next_char(self):
		if self.index + 1 < len(self.source):
			return self.source[self.index + 1]
		return None

	def move_to_next_char(self):
		self.index += 1

	def current_char(self):
		return self.source[self.index]


class Token:
	def __init__(self, typ, val):
		self.typ = typ
		self.val = val


class Tokens:
	def __init__(self, tokens_iterator):
		self.tokens = list(tokens_iterator)

		self.index = -1

	def next_token(self):
		if self.index + 1 < len(self.tokens):
			return self.tokens[self.index + 1]
		return None

	def move_to_next_token(self):
		self.index += 1

	def current_token(self):
		return self.tokens[self.index]


def scan_while(source, allowed):
	res = source.current_char()

	while source.next_char() in allowed:
		source.move_to_next_char()
		res += source.current_char()

	return res


def lex(source):
	numbers = '0123456789.'
	literals = '+-*/%'
	ignored = ' \t'

	while source.next_char() is not None:
		source.move_to_next_char()
		char = source.current_char()

		if char in ignored:
			continue
		elif char == '\n':
			yield Token('line', '')
		elif char in numbers:
			yield Token('number', scan_while(source, numbers))
		elif char in literals:
			yield Token('literal', scan_while(source, literals))


file_name = sys.argv[1]

with open(file_name) as f:
	source_code = f.read()

source_code = Source(source_code)
tokens = lex(source_code)
tokens = Tokens(tokens)
ast = parse(tokens)
