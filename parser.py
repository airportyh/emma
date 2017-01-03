import sys
from lexer import Tokenizer

def assert_next_token(tokens, name):
    token_name, _ = tokens.next()
    assert token_name == name, 'Expected next token to be %r' % name

def prog(tokens, indent):
    return ('prog', stms(tokens, indent))

def stms(tokens, indent):
    stms = []
    while True:
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
    print 'stm'
    token_name, value = tokens.peek()
    print "token_name %r" % token_name
    if token_name == 'indent':
        tokens.next()
        if len(value) != indent:
            raise Exception('Indentation mismatch')
    return fn_stm(tokens, indent) or line_stm(tokens, indent)

def line_stm(tokens, indent):
    ret_expr = expr(tokens, indent)
    print 'got expr %r' % (ret_expr,)
    token_name, _ = tokens.next()
    if token_name != 'newline':
        raise Exception('Expected newline')
    return ret_expr

def expr(tokens, indent):
    ret_expr = assn_expr(tokens, indent) or return_expr(tokens, indent) or atom_expr(tokens, indent)
    if ret_expr is None:
        raise Exception('Expected an expression')
    return ret_expr

def fn_stm(tokens, indent):
    print 'fn_expr'
    token_name, _ = tokens.peek()
    if token_name != 'function':
        return None
    else:
        tokens.next()
    token_name, identifier = tokens.next()
    plist = param_list(tokens, indent)
    assert_next_token(tokens, 'colon')
    assert_next_token(tokens, 'newline')
    indent_token = tokens.peek()
    assert indent_token[0] == 'indent', 'Expected indentation'
    indent_amount = len(indent_token[1])
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
        if token[0] == 'closeparan':
            break
        assert token[0] == 'comma', 'Expected comma'
    print 'Params %r' % params
    return params

def return_expr(tokens, indent):
    print 'return_expr'
    token_name, _ = tokens.peek()
    if token_name != 'return':
        return None
    else:
        tokens.next()
    ret_expr = expr(tokens, indent)
    print 'Returning a return'
    return ('return', ret_expr)

def assn_expr(tokens, indent):
    print 'assn_expr'
    token_name, identifier = tokens.peek()
    if token_name != 'identifier':
		return None
    else:
		tokens.next()
    token_name, _ = tokens.next()
    if token_name != 'assignment':
        raise Exception('Expected assignment operator')
    # TODO: not just atoms can be on rhs
    rhs = atom_expr(tokens, indent)
    return ('assignment', identifier, rhs)

def atom_expr(tokens, indent):
    token_name, value = tokens.next()
    if token_name != 'number':
        raise Exception('Expected number')
    return ('number', float(value))

if __name__ == '__main__':
    filename = sys.argv[1]
    print "Reading", filename
    f = open(filename, 'r')
    print prog(Tokenizer(f.read()), 0)
