import sys
from lexer import Tokenizer
import pprint
pp = pprint.PrettyPrinter(indent=4)

def assert_next_token(tokens, name):
    token = tokens.next()
    assert token.name == name, 'Expected next token to be %r' % name

def prog(tokens, indent):
    return ('prog', stms(tokens, indent))

def stms(tokens, indent):
    stms = []
    while True:
        if tokens.peek().name == 'newline':
            tokens.next()
        s = stm(tokens, indent)
        if s:
            stms.append(s)
        else:
            break
        try:
            tokens.peek()
        except:
            break
    return stms

def stm(tokens, indent):
    print 'stm', indent
    token = tokens.peek()
    print "token_name %r" % token.name
    if token.name == 'indent':
        print 'len(token.value)', len(token.value)
        tokens.next()
        if len(token.value) < indent:
            return None
        elif len(token.value) != indent:
            raise Exception('Indentation mismatch')
    else:
        if indent > 0:
            # in a block but no indent means stopping
            # indent block
            return None
    return fn_stm(tokens, indent) or line_stm(tokens, indent)

def line_stm(tokens, indent):
    ret_expr = expr(tokens, indent)
    print 'got expr %r' % (ret_expr,)
    token = tokens.next()
    if token.name != 'newline':
        raise Exception('Expected newline')
    return ret_expr

def expr(tokens, indent):
    ret_expr = assn_expr(tokens, indent) or return_expr(tokens, indent) or atom_expr(tokens, indent)
    if ret_expr is None:
        raise Exception('Expected an expression')
    return ret_expr

def fn_stm(tokens, indent):
    print 'fn_expr'
    token = tokens.peek()
    if token.name != 'function':
        return None
    else:
        tokens.next()
    token = tokens.next()
    identifier = token.value
    plist = param_list(tokens, indent)
    assert_next_token(tokens, 'colon')
    assert_next_token(tokens, 'newline')
    indent_token = tokens.peek()
    assert indent_token.name == 'indent', 'Expected indentation'
    indent_amount = len(indent_token.value)
    print 'indent_amount %r' % indent_amount
    block_stms = stms(tokens, indent_amount)
    return ('function', identifier, plist, block_stms)

def param_list(tokens, indent):
    print 'param_list'
    params = []
    assert_next_token(tokens, 'openparan')
    while True:
        token = tokens.next()
        params.append(token)
        token = tokens.next()
        if token.name == 'closeparan':
            break
        assert token.name == 'comma', 'Expected comma'
    print 'Params %r' % params
    return params

def return_expr(tokens, indent):
    print 'return_expr'
    token = tokens.peek()
    if token.name != 'return':
        return None
    else:
        tokens.next()
    ret_expr = expr(tokens, indent)
    print 'Returning a return'
    return ('return', ret_expr)

def assn_expr(tokens, indent):
    print 'assn_expr'
    token = tokens.peek()
    if token.name != 'identifier':
		return None
    else:
		tokens.next()
    token = tokens.next()
    if token.name != 'assignment':
        raise Exception('Expected assignment operator - Line %d' % token.line_no)
    # TODO: not just atoms can be on rhs
    rhs = atom_expr(tokens, indent)
    return ('assignment', token.name, rhs)

def atom_expr(tokens, indent):
    token = tokens.next()
    if token.name != 'number':
        raise Exception('Expected number')
    return ('number', float(token.value))

if __name__ == '__main__':
    filename = sys.argv[1]
    print "Reading", filename
    f = open(filename, 'r')
    pp.pprint(prog(Tokenizer(f.read()), 0))
