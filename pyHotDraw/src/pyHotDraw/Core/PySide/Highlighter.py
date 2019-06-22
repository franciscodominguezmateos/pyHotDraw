#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22/11/2013

@author: paco
'''
from PySide import QtCore, QtGui

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        #keywordFormat.setFontWeight(QtGui.QFont.Bold)
        keywordFormat.setForeground(QtGui.QColor(0,170,0))

        keywordPatterns = ["\\bG00\\b", "\\bG01\\b","\\bG0\\b", "\\bG1\\b", "\\bM02\\b",
                "\\bM05\\b", "\\bG21\\b", "\\bG22\\b", "\\bG02\\b", "\\bG2\\b",
                "\\bG03\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]
        
        axisFormat=QtGui.QTextCharFormat()
        axisFormat.setForeground(QtGui.QColor(255,85,0))
        self.highlightingRules.append((QtCore.QRegExp("[xyzijXYZIJ]"),axisFormat))
        feedFormat=QtGui.QTextCharFormat()
        feedFormat.setForeground(QtGui.QColor(128,64,0))
        self.highlightingRules.append((QtCore.QRegExp("[fF]"),feedFormat))

        parameterFormat = QtGui.QTextCharFormat()
        #parameterFormat.setFontWeight(QtGui.QFont.Bold)
        parameterFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("[#]\\d+"),
                parameterFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtGui.QColor(170,170,127))

        self.commentStartExpression = QtCore.QRegExp("\\(")
        self.commentEndExpression = QtCore.QRegExp("\\)")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);

