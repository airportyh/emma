import sys
import re
# print contents

def token(name):
    return (name, re.compile(name))

patterns = [
    token('function'),
    token('return'),
    token('class'),
    token('super'),
    token('method'),
    token('constructor'),
    token('true'),
    token('false'),
    ('identifier', re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*')),
    ('number', re.compile(r'[0-9]+(?:\.[0-9]+)?')),
    ('assignment', re.compile(r'=')),
    ('indent', re.compile(r'\t+')),
    ('newline', re.compile(r'\n')),
    ('openparan', re.compile(r'\(')),
    ('closeparan', re.compile(r'\)')),
    ('whitespace', re.compile(r' +')),
    ('colon', re.compile(r':')),
    ('comma', re.compile(r',')),
    ('plus', re.compile(r'\+')),
    ('minus', re.compile(r'\-')),
    ('multiply', re.compile(r'\*')),
    ('string_literal', re.compile(r"'[^']+'")),
    ('dot', re.compile(r'\.')),
    ('left_bracket', re.compile(r'\[')),
    ('right_bracket', re.compile(r'\]')),
    ('left_curly', re.compile(r'\{')),
    ('right_curly', re.compile(r'\}'))
]

class Token(object):
    def __init__(self, name, value, line_no):
        self.name = name
        self.value = value
        self.line_no = line_no

    def __repr__(self):
        if self.name == 'newline':
            return '\\n'
        else:
            return '%s(%s)' % (self.name, self.value)

def tokenize(contents):
    last_token_name = None
    line_no = 1
    while contents:
        m = None
        for token_name, pattern in patterns:
            m = pattern.match(contents)
            if m:
                # print "matched %s %s" % (pattern.pattern, m.group(0))
                if token_name == 'whitespace':
                    if last_token_name == 'newline':
                        yield Token(token_name, m.group(0), line_no)
                else:
                    yield Token(token_name, m.group(0), line_no)
                if token_name == 'newline':
                    line_no += 1
                contents = contents[m.end():]
                # print "Rest[%s]" % contents
                last_token_name = token_name
                break
            else:
                # print "didnt match %s" % pattern.pattern
                pass
        if m is None:
			raise Exception('Houston, we have a problem.')

class Tokenizer(object):
	def __init__(self, contents):
		self.gen = tokenize(contents)
		self.buffer = []

	def __iter__(self):
		return self

	def next(self):
		if len(self.buffer) > 0:
			return self.buffer.pop(0)
		else:
			return self.gen.next()

	def peek(self):
		if self.buffer == []:
			self.buffer.append(self.gen.next())
		return self.buffer[0]

if __name__ == '__main__':
    filename = sys.argv[1]

    print "Reading", filename

    f = open(filename, 'r')
    for token in Tokenizer(f.read()):
        print token
