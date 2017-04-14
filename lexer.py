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
    def __init__(self, name, value, line_no, col_no):
        self.name = name
        self.value = value
        self.line_no = line_no
        self.col_no = col_no

    def __repr__(self):
        value = self.value
        if value == '\n':
            value = '\\n'
        return '%s(%s) - %d, %d' % (self.name, value, self.line_no, self.col_no)

def tokenize(contents):
    lines = contents.split('\n')
    last_token_name = None
    line_no = 1
    col_no = 1
    while contents:
        m = None
        for token_name, pattern in patterns:
            m = pattern.match(contents)
            if m:
                # print "matched %s %s" % (pattern.pattern, m.group(0))
                if token_name == 'whitespace':
                    if last_token_name == 'newline':
                        yield Token(token_name, m.group(0), line_no, col_no)
                    col_no += m.end()
                else:
                    yield Token(token_name, m.group(0), line_no, col_no)
                    if token_name == 'newline':
                        line_no += 1
                        col_no = 1
                    else:
                        col_no += m.end()

                contents = contents[m.end():]
                # print "Rest[%s]" % contents
                last_token_name = token_name
                break
            else:
                # print "didnt match %s" % pattern.pattern
                pass
        if m is None:
            print
            line = lines[line_no - 1]
            print line
            line_indent = get_indent(line)
            print line_indent + ' ' * (col_no - len(line_indent) - 1) + '^'
            raise Exception('Houston, we have  a problem on line %d column %d.' % (line_no, col_no))

INDENT_RE = re.compile(r'\t*')
def get_indent(line):
    return INDENT_RE.match(line).group(0)

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
