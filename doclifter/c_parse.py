#!/usr/bin/env python

class LineTokenizer:
    "Make a collection of lines available either as lines or tokens."
    def __init__(self, lines):
        self.lines = lines
        self.pretokenizer = None
        self.token_index = 0
        self.tokens = []
        self.tokenize()
    def popline(self):
        "Grab the next line and make it the token buffer."
        if not self.lines:
            #sys.stderr.write("Popline returns None\n")
            return None
        else:
            #sys.stderr.write("Popline starts with: %s\n" % self)
            res = self.lines[0]
            self.lines.pop(0)
            self.tokens = []
            if self.lines:
                self.tokenize(self.pretokenizer)
            #sys.stderr.write("In popline, I return %s: %s\n" % (`res`, self))
            return res
    def pushline(self, line):
        "Replace the token buffer with the current line."
        self.lines = [self.line] + self.lines
        self.tokenize(self.pretokenizer)
        #sys.stderr.write("Pushline leaves: %s\n" % self)
    def peekline(self):
        "Return the token buffer"
        if not self.lines:
            return None
        else:
            return self.lines[0]
    def tokenize(self, new_pretokenizer=None):
        "Split a line on tabs and whitespaces, but not linefeeds."
        self.pretokenizer = new_pretokenizer
        if self.lines:
            if self.pretokenizer:
                line = self.pretokenizer(self.lines[0])
            else:
                line = self.lines[0]
            self.tokens = line.split()
            #sys.stderr.write("In tokenize, I split: " + `self` + '\n')
    def restore_newlines(self):
        self.tokens.append("\n")
        for i in range(len(self.lines)):
            self.lines[i] += "\n"
    def token_pop(self, count=1):
        "Get a token."
        if not self.lines:
            return None
        #sys.stderr.write("In token_pop, I see: " + `self` + '\n')
        res = self.tokens[0]
        self.tokens = self.tokens[count:]
        if not self.tokens:
            if not self.lines:
                #sys.stderr.write("In token_pop, I return None: " + `self` + '\n')
                return None
            self.popline()
        self.token_index += 1
        #sys.stderr.write("In token_pop, I return: " + `self` + '\n')
        return res
    def token_peek(self):
        "Peek at the next token."
        if self.tokens:
            return self.tokens[0]
        else:
            return None		# list empty means we're out of data

    def token_push(self, tok):
        "Push back a token."
        self.tokens = [tok] + self.tokens
        # We do *not* alter the source line!
        self.token_index -= 1
    def __str__(self):
        "Display the state of the object."
        return "<tokens=%s, lines=%s>" % (self.tokens, self.lines)
    __repr__ = __str__

import exceptions

class CDeclarationError(exceptions.Exception):
    def __init__(self, message, retval=1):
        self.message = message
        self.retval = retval

class CDeclarationParser:
    "Parse a C declaration,"
    def __init__(self, io, handler, notifier=lambda x: None):
        self.io = io
        self.handler = handler
        self.notifier = notifier
        self.tokencount = 0
        self.state_stack = []
        self.construct_stack = []
        self.typedefs = {}
        self.declaration()
    def token_peek(self):
        return self.io.token_peek()	# FIXME: skip C comments
    def token_pop(self):
        self.tokencount += 1
        return self.io.token_pop()	# FIXME: skip C comments
    def checkin(self, label, opt):
        print " " * len(self.construct_stack) + "->" + label + " " + ("required", "optional")[opt]
        self.state_stack.append(self.tokencount)
        self.construct_stack.append(label)
    def checkout(self, label, opt):
        nonempty = self.state_stack[-1] < self.tokencount
        self.state_stack.pop()
        self.construct_stack.pop()
        if not opt and not nonempty:
            raise CDeclarationError("missing required element in " + label)
        else:
            print " " * len(self.construct_stack) + "<-" + label + " " + ("not found", "found")[nonempty]
            return nonempty
    def expect(self, *args):
        yes = self.token_peek() in args
        print " " * len(self.construct_stack) + "expect" + `args` + " = " + "ny"[yes] + " (" + self.token_peek() + ")"
        if yes:
            # One of only two places we pop the token stack
            print "Popped terminal:", self.token_pop()
        return yes
    def identifier(self, opt):
        self.checkin("identifier", opt)
        id = self.token_peek()
        if not id or (not id[0].isalpha and isalpha[0] != "_"):
            raise CDeclarationError("saw %s where identifier expected " % id)
        else:
            # And here is the other.
            self.handler(id, self.construct_stack)
            self.token_pop()
        self.checkout("identifier", opt)
    # Rest is hand-compiled from "A.13 of the C Programming Language", 2nd ed.
    # It covers the entire declaration syntax, except for initializers.
    # It does not cover function definitions.  There are two things we
    # don't do quite right because they can't be done LL(1), see below.
    def declaration(self):
        self.declaration_specifiers(opt=0)
        self.init_declarator_list(opt=0)	# Technically, is opt
        self.expect(";")
    def declaration_list(self, opt):
        self.checkin("declaration_list", opt)
        self.declaration_specifiers(opt=0)
        while self.declaration_specifiers(opt=1):
            continue
        return self.checkout("declaration_list", opt)
    def declaration_specifiers(self, opt):
        self.checkin("declaration_specifiers", opt)
        if \
        self.storage_class_specifier(opt=1) or \
        self.type_specifier(opt=1) or \
        self.type_qualifier(opt=1):
            self.declaration_specifiers(opt=1)
        return self.checkout("declaration_specifiers", opt)
    def storage_class_specifier(self, opt):
        self.checkin("storage_class_specifier", opt)
        self.expect("static", "extern", "typedef")	# auto, register
        return self.checkout("storage_class_specifier", opt)
    def type_specifier(self, opt):
        self.checkin("type_specifier", opt)
        self.expect("void", "char", "short", "int", "long", "float", "double", "signed", "unsigned") \
        or \
        self.struct_or_union_specifier(opt) \
        or \
        self.identifier(opt)
        # We've left out one legal alternative, an enum, because we
        # never expect to encounter it on a man page.
        # We accept any identifier here because we can't know all typedefs
        # in advance -- that would require parsing include files and a
        # semi-infinite amount of hair.
        return self.checkout("type_specifier", opt)
    def type_qualifier(self, opt):
        self.checkin("type_qualifier", opt)
        self.expect("const", "volatile")
        return self.checkout("type_qualifier", opt)
    def struct_or_union_specifier(self, opt):
        self.checkin("struct_or_union_specifier", opt)
        if not (self.expect("struct","union") and self.identifier(opt=0)):
            self.expect("{") and \
            self.struct_declaration_list(opt=0) and \
            self.expect("}")
        return self.checkout("struct_or_union_specifier", opt)
    def struct_declaration_list(self, opt):
        self.checkin("struct_declaration_list", opt)
        self.struct_declaration(opt=0)
        while self.struct_declaration(opt=1):
            continue
        return self.checkout("struct_declaration_list", opt)
    def init_declarator_list(self, opt):
        self.checkin("init_declarator_list", opt)
        # This is where we lop off the initializer branch.
        self.declarator(opt=0)
        while self.expect(","):
            self.init_declaration(opt=1)
        return self.checkout("init_declarator_list", opt)
    def struct_declaration(self, opt):
        self.checkin("struct_declaration", opt)
        self.specifier_qualifier_list(opt=0)
        self.struct_declarator_list(opt=0)
        return self.checkout("struct_declaration", opt)
    def specifier_qualifier_list(self, opt):
        self.checkin("specifier_qualifier_list", opt)
        self.type_specifier(opt=0) or self.type_qualifier(opt=0)
        while self.type_specifier(opt=1) or self.type_qualifier(opt=1):
            continue
        self.specifier_qualifier_list(opt=1)
        return self.checkout("specifier_qualifier_list", opt)
    def struct_declarator_list(self, opt):
        self.checkin("struct_declarator_list", opt)
        self.struct_declarator(opt=0)
        while self.struct_declaration(opt=1):
            continue
        return self.checkout("struct_declarator_list", opt)
    def struct_declarator(self, opt):
        self.checkin("struct_declarator", opt)
        self.declarator(opt=1)
        if self.expect(":"):
            self_constant_expression(opt=0)
        return self.checkout("struct_declarator", opt)
    def declarator(self, opt):
        self.checkin("declarator", opt)
        self.pointer(opt=1)
        self.direct_declarator(opt=0)
        return self.checkout("declarator", opt)
    def direct_declarator(self, opt):
        self.checkin("direct_declarator", opt)
        # This is not quite the A.13 production, which is
        # direct-declarator:
        #     identifer
        #     ( declarator)
        #     direct-declarator [ constant-expression? ]...
        #     direct-declarator ( parameter-type-list )
        #     direct-declarator ( identifier-list )
        # This be parsed LL(1) the way we're doing.  We implement this:
        # direct-declarator-prefix:
        #     identifier
        #     ( declarator )
        # direct-declarator:
        #     direct-declarator-prefix [ constant-expression? ]...
        #     direct-declarator-prefix ( parameter-type-list )
        #     direct-declarator-prefix ( identifier-list )
        # This won't catch weird shit like foo(bar)[MUMBLE].
        # Let's hope it doesn't miss any real-world cases.
        if self.expect("("):
            self.declarator(opt=0)
            self.expect(")")
        else:
            self.identifier(opt=0)
        if self.expect("("):
            self.parameter_type_list(opt=0) or self.identifier_list(1)
            self.expect(")")
        else:
            while self.expect("["):
                self.constant_expression(opt=1)
                self.expect("]")
        return self.checkout("direct_declarator", opt)
    def pointer(self, opt):
        self.checkin("pointer", opt)
        self.expect("*")
        if self.type_qualifier_list(opt=1):
            self.pointer(opt=1)
        return self.checkout("pointer", opt)
    def type_qualifier_list(self, opt):
        self.checkin("type_qualifier_list", opt)
        while self.type_qualifier(opt=1):
            continue
        return self.checkout("type_qualifier_list", opt)
    def parameter_type_list(self, opt):
        self.checkin("parameter_type_list", opt)
        self.parameter_list(opt=0)
        if self.expect(","):
            self.expect("...")
        return self.checkout("parameter_type_list", opt)
    def parameter_list(self, opt):
        self.checkin("parameter_list", opt)
        self.parameter_declaration(opt=0)
        while self.expect(","):
            self.parameter_declaration(opt=0)
        return self.checkout("parameter_list", opt)
    def parameter_declaration(self, opt):
        self.checkin("parameter_declaration", opt)
        self.declaration_specifiers(opt=0)
        self.declarator(opt=0) \
        or \
        self.abstract_declarator(opt=1)
        return self.checkout("parameter_declaration", opt)
    def identifier_list(self, opt):
        self.checkin("identifier_list", opt)
        self.identifier(opt=0)
        while self.expect(","):
            self.identifier(opt=0)
        return self.checkout("identifier_list", opt)
    def type_name(self, opt):
        self.checkin("type_name", opt)
        self.specifier_qualifier_list(opt=0)
        self.abstract_declarator(opt=1)
        return self.checkout("type_name", opt)
    def abstract_declarator(self, opt):
        self.checkin("abstract_declarator", opt)
        if self.pointer(opt=1):
            self.direct_abstract_declarator(opt=1)
        else:
            self.direct_abstract_declarator(opt=0)
        return self.checkout("abstract_declarator", opt)
    def direct_abstract_declarator(self, opt):
        self.checkin("direct_abstract_declarator", opt)
        # The actual production is
        # direct_abstract_declarator:
        #    ( abstract-declarator )
        #    direct_abstract_declarator? [ constant-expression? ]
        #    direct_abstract_declarator? ( parameter-type-list? )
        # This too cannot be parsed LL(1)  So we do this:
        # direct_abstract_declarator-prefix:
        #    ( abstract_declarator ) [ constant-expression? ]...
        #    ( abstract_declarator ) ( parameter-type-list? )
        # and hope it's good enough to catch the real-world cases.
        if self.expect("("):
            self.abstract_declarator(opt=0)
            self.expect(")")        
        if self.expect("("):
            self.parameter_type_list(opt=0)
            self.expect(")")
        else:
            while self.expect("["):
                self.constant_expression(opt=1)
                self.expect("]")
        return self.checkout("direct_abstract_declarator", opt)
    def typedef_name(self, opt):
        self.checkin("typedef_name", opt)
        self.identifier(opt=0)
        return self.checkout("typedef_name", opt)
    def constant_expression(self, opt):
        self.checkin("constant_expression", opt)
        # Full grammar has expressions here.
        # All we're ever going to see is constants, thank goodness.
        self.identifier(opt=1)
        return self.checkout("constant_expression", opt)

if __name__ == "__main__":
    import sys
    def post(token, stack):
        print "I see %s with %s" % (token, stack)
    def notify(msg):
        print msg
    io = LineTokenizer(sys.stdin.readlines())
    print io
    try:
        CDeclarationParser(io, post, notify)
    except CDeclarationError, e:
        print e.message

