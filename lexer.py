import sys
import re
# print contents

patterns = [
    ('function', re.compile(r'function')),
    ('return', re.compile(r'return')),
    ('identifier', re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*')),
    ('number', re.compile(r'[0-9]+(?:\.[0-9]+)?')),
    ('assignment', re.compile(r'=')),
    ('indent', re.compile(r'\t+')),
    ('newline', re.compile(r'\n')),
    ('openparan', re.compile(r'\(')),
    ('closeparan', re.compile(r'\)')),
    ('whitespace', re.compile(r' +')),
    ('colon', re.compile(r':')),
    ('comma', re.compile(r','))
]

def tokenize(contents):
    last_token_name = None
    while contents:
        m = None
        for token_name, pattern in patterns:
            m = pattern.match(contents)
            if m:
                # print "matched %s %s" % (pattern.pattern, m.group(0))
                if token_name == 'whitespace':
                    if last_token_name == 'newline':
                        yield (token_name, m.group(0))
                else:
                    yield (token_name, m.group(0))
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
