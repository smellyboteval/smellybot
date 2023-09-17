#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 00:47:35 2022

@author: amal
"""

#imports
import pandas as pd
from antlr4 import  FileStream, CommonTokenStream
from Parse.Java8Lexer import Java8Lexer
from Parse.Java8Parser import Java8Parser
from Parse.Java8Visitor import Java8Visitor

method = pd.DataFrame  (columns = [  'mName','Method'])
classes = pd.DataFrame  (columns = ['cName', 'Class'])

def getFullText (tokens, start, stop):
    text = [tokens[i].text for i in range(start, stop+1)]
    return ' '.join(text)
    
   
def Extract(fileName):
    global method, classes
    method = method[0:0]
    classes = classes[0:0]
    method = method.append({'mName':'', 'Method' : ""}, ignore_index = True)

    try:
        data = FileStream(fileName, encoding = 'utf-8')
    
        # lexer
        lexer = Java8Lexer(data)
        stream = CommonTokenStream(lexer)
        
        # tokens
        stream.fill()
        tokens = stream.getTokens(0, len(stream.tokens)-1)
        
        # parser
        parser = Java8Parser(stream)
        tree = parser.compilationUnit()
        
        # evaluator
        visitor1 = MyVisitorM(tokens)
        visitor2 = MyVisitorC(tokens)
        output = visitor1.visit(tree)
        output = visitor2.visit(tree)

        #print('Data successfully extracted: ', fileName)
    except:
        print('Unable to extract from file: ', fileName)
        
    return method['mName'][:-1].values.tolist(), method['Method'][:-1].values.tolist(), classes['cName'].values.tolist(), classes['Class'].values.tolist()
    
class MyVisitorM(Java8Visitor):
    
    __slots__ = 'tokens'

    def __init__(self, tokens):
        self.tokens = tokens

        #this code is ude to remove the @ at the start of amethod
    def visitMethodModifier(self, ctx):
        start = ctx.start.tokenIndex       
        stop = ctx.stop.tokenIndex
        
        global method 
        text = getFullText(self.tokens, start, stop)
        if text.startswith('@'):
            return
        #method = method.append({'Method' : text}, ignore_index = True)
        method.iloc[-1, 1] = method.iloc[-1]['Method'] + " " + text
               
        
    def visitMethodHeader(self, ctx):
        start = ctx.start.tokenIndex       
        stop = ctx.stop.tokenIndex
        
        method_name = ctx.children[1].children[0].getText()
        #print('method name ========== ', method_name)
        
        global method 
        text = getFullText(self.tokens, start, stop)
        #method = method.append({'Method' : text}, ignore_index = True)
        method.iloc[-1, 1] = method.iloc[-1]['Method'] + " " + text
        method.iloc[-1, 0] =  method_name

    def visitMethodBody(self, ctx):
        start = ctx.start.tokenIndex       
        stop = ctx.stop.tokenIndex
        
        global method 
        text = getFullText(self.tokens, start, stop)
        method.iloc[-1, 1] = method.iloc[-1]['Method'] + " " + text
        method = method.append({'Method' : ""}, ignore_index = True)
#'''        
    
class MyVisitorC(Java8Visitor):
    
    __slots__ = 'tokens'

    def __init__(self, tokens):
        self.tokens = tokens
    def visitClassDeclaration(self, ctx):
        start = ctx.start.tokenIndex       
        stop = ctx.stop.tokenIndex
        
        class_name = ctx.children[0].children[2].getText()
        #print('class name ========== ', class_name)
        
        global classes 
        text = getFullText(self.tokens, start, stop)
        classes = classes.append({'cName': class_name,'Class' : text}, ignore_index = True)
        
        #print('This is the class: ', text)


if __name__ == "__main__":
    a = ""
    #mn, m, cn, c = Extract("Projects/Test-1.2.2/Java9BaseListener.java")
    #print (mn)
    #print (m)
    #print (cn)
    #print (c)