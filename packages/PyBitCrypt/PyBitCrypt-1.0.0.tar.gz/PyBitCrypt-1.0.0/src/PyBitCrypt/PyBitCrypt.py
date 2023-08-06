import sys
import getpass
import time

TextList = []
ShiftList = []
OutList = []

def Encode(BitCrypt, Text):

    #Turns BitCrypt Code Into Required Format
    Count = 0
    for u in BitCrypt:
        ShiftList.append(u)
    
    for o in ShiftList:
        if o == 'a':
            ShiftList[Count] = 1
        if o == 'b':
            ShiftList[Count] = 2
        if o == 'c':
            ShiftList[Count] = 3
        if o == 'd':
            ShiftList[Count] = 4
        if o == 'e':
            ShiftList[Count] = 5
        if o == 'f':
            ShiftList[Count] = 6
        if o =='g':
            ShiftList[Count] = 7
        if o =='h':
            ShiftList[Count] = 8
        if o == 'i':
            ShiftList[Count] = 9
        if o == 'j':
            ShiftList[Count] = 10
        if o == 'k':
            ShiftList[Count] = 11
        if o == 'l':
            ShiftList[Count] = 12
        if o == 'm':
            ShiftList[Count] = 13
        if o == 'n':
            ShiftList[Count] = 14
        if o == 'o':
            ShiftList[Count] = 15
        if o == 'p':
            ShiftList[Count] = 16
        if o == 'q':
            ShiftList[Count] = 17
        if o == 'r':
            ShiftList[Count] = 18
        if o == 's':
            ShiftList[Count] = 19
        if o == 't':
            ShiftList[Count] = 20
        if o == 'u':
            ShiftList[Count] = 21
        if o == 'v':
            ShiftList[Count] = 22
        if o == 'w':
            ShiftList[Count] = 23
        if o == 'x':
            ShiftList[Count] = 24
        if o == 'y':
            ShiftList[Count] = 25
        if o == 'z':
            ShiftList[Count] = 26
        if o == ' ':
            ShiftList[Count] = 0
        if o == '`':
            ShiftList[Count] = 27
        if o == '~':
            ShiftList[Count] = 28
        if o == '1':
            ShiftList[Count] = 29
        if o == '!':
            ShiftList[Count] = 30
        if o == '2':
            ShiftList[Count] = 31
        if o == '@':
            ShiftList[Count] = 32
        if o == '3':
            ShiftList[Count] = 33
        if o == '#':
            ShiftList[Count] = 34
        if o == '4':
            ShiftList[Count] = 35
        if o == '$':
            ShiftList[Count] = 36
        if o == '5':
            ShiftList[Count] = 37
        if o == '%':
            ShiftList[Count] = 38
        if o == '6':
            ShiftList[Count] = 39
        if o == '^':
            ShiftList[Count] = 40
        if o == '7':
            ShiftList[Count] = 41
        if o == '&':
            ShiftList[Count] = 42
        if o == '8':
            ShiftList[Count] = 43
        if o == '*':
            ShiftList[Count] = 44
        if o == '9':
            ShiftList[Count] = 45
        if o == '(':
            ShiftList[Count] = 46
        if o == '0':
            ShiftList[Count] = 47
        if o == ')':
            ShiftList[Count] = 48
        if o == '-':
            ShiftList[Count] = 49
        if o == '_':
            ShiftList[Count] = 50
        if o == '=':
            ShiftList[Count] = 51
        if o == '+':
            ShiftList[Count] = 52
        if o == '[':
            ShiftList[Count] = 53
        if o == '{':
            ShiftList[Count] = 54
        if o == ']':
            ShiftList[Count] = 55
        if o == '}':
            ShiftList[Count] = 56
        if o == '\\':
            ShiftList[Count] = 57
        if o == '|':
            ShiftList[Count] = 58
        if o == ';':
            ShiftList[Count] = 59
        if o == ':':
            ShiftList[Count] = 60
        if o == "'":
            ShiftList[Count] = 61
        if o == '"':
            ShiftList[Count] = 62
        if o == ',':
            ShiftList[Count] = 63
        if o == '<':
            ShiftList[Count] = 64
        if o == '.':
            ShiftList[Count] = 65
        if o == '>':
            ShiftList[Count] = 66
        if o == '/':
            ShiftList[Count] = 67
        if o == '?':
            ShiftList[Count] = 68

        Count = Count+1
    
    #Turns Input Text Into Required Format
    Count = 0
    for i in Text:
        TextList.append(i)
    
    for a in TextList:
        if a == 'a':
            TextList[Count] = 1
        if a == 'b':
            TextList[Count] = 2
        if a == 'c':
            TextList[Count] = 3
        if a == 'd':
            TextList[Count] = 4
        if a == 'e':
            TextList[Count] = 5
        if a == 'f':
            TextList[Count] = 6
        if a =='g':
            TextList[Count] = 7
        if a =='h':
            TextList[Count] = 8
        if a == 'i':
            TextList[Count] = 9
        if a == 'j':
            TextList[Count] = 10
        if a == 'k':
            TextList[Count] = 11
        if a == 'l':
            TextList[Count] = 12
        if a == 'm':
            TextList[Count] = 13
        if a == 'n':
            TextList[Count] = 14
        if a == 'o':
            TextList[Count] = 15
        if a == 'p':
            TextList[Count] = 16
        if a == 'q':
            TextList[Count] = 17
        if a == 'r':
            TextList[Count] = 18
        if a == 's':
            TextList[Count] = 19
        if a == 't':
            TextList[Count] = 20
        if a == 'u':
            TextList[Count] = 21
        if a == 'v':
            TextList[Count] = 22
        if a == 'w':
            TextList[Count] = 23
        if a == 'x':
            TextList[Count] = 24
        if a == 'y':
            TextList[Count] = 25
        if a == 'z':
            TextList[Count] = 26
        if a == ' ':
            TextList[Count] = 0
        if a == '`':
            TextList[Count] = 27
        if a == '~':
            TextList[Count] = 28
        if a == '1':
            TextList[Count] = 29
        if a == '!':
            TextList[Count] = 30
        if a == '2':
            TextList[Count] = 31
        if a == '@':
            TextList[Count] = 32
        if a == '3':
            TextList[Count] = 33
        if a == '#':
            TextList[Count] = 34
        if a == '4':
            TextList[Count] = 35
        if a == '$':
            TextList[Count] = 36
        if a == '5':
            TextList[Count] = 37
        if a == '%':
            TextList[Count] = 38
        if a == '6':
            TextList[Count] = 39
        if a == '^':
            TextList[Count] = 40
        if a == '7':
            TextList[Count] = 41
        if a == '&':
            TextList[Count] = 42
        if a == '8':
            TextList[Count] = 43
        if a == '*':
            TextList[Count] = 44
        if a == '9':
            TextList[Count] = 45
        if a == '(':
            TextList[Count] = 46
        if a == '0':
            TextList[Count] = 47
        if a == ')':
            TextList[Count] = 48
        if a == '-':
            TextList[Count] = 49
        if a == '_':
            TextList[Count] = 50
        if a == '=':
            TextList[Count] = 51
        if a == '+':
            TextList[Count] = 52
        if a == '[':
            TextList[Count] = 53
        if a == '{':
            TextList[Count] = 54
        if a == ']':
            TextList[Count] = 55
        if a == '}':
            TextList[Count] = 56
        if a == '\\':
            TextList[Count] = 57
        if a == '|':
            TextList[Count] = 58
        if a == ';':
            TextList[Count] = 59
        if a == ':':
            TextList[Count] = 60
        if a == "'":
            TextList[Count] = 61
        if a == '"':
            TextList[Count] = 62
        if a == ',':
            TextList[Count] = 63
        if a == '<':
            TextList[Count] = 64
        if a == '.':
            TextList[Count] = 65
        if a == '>':
            TextList[Count] = 66
        if a == '/':
            TextList[Count] = 67
        if a == '?':
            TextList[Count] = 68

        Count = Count+1
        
    #TextList[2213%len(TextList)]
    #Encodes Text
    Count = 0
    for q in TextList:
        p = int(q)
        z = int(ShiftList[Count%len(ShiftList)])
        OutList.append(p+z)
        Count = Count+1
        
    #Reverts To Text Format
    Output = ''
    for w in OutList:
        r = w%69
        Count = 0
        if r == 1:
            Output = Output + 'A'
        if r == 2:
            Output = Output + 'B'
        if r == 3:
            Output = Output + 'C'
        if r == 4:
            Output = Output + 'D'
        if r == 5:
            Output = Output + 'E'
        if r == 6:
            Output = Output + 'F'
        if r == 7:
            Output = Output + 'G'
        if r == 8:
            Output = Output + 'H'
        if r == 9:
            Output = Output + 'I'
        if r == 10:
            Output = Output + 'J'
        if r == 11:
            Output = Output + 'K'
        if r == 12:
            Output = Output + 'L'
        if r == 13:
            Output = Output + 'M'
        if r == 14:
            Output = Output + 'N'
        if r == 15:
            Output = Output + 'O'
        if r == 16:
            Output = Output + 'P'
        if r == 17:
            Output = Output + 'Q'
        if r == 18:
            Output = Output + 'R'
        if r == 19:
            Output = Output + 'S'
        if r == 20:
            Output = Output + 'T'
        if r == 21:
            Output = Output + 'U'
        if r == 22:
            Output = Output + 'V'
        if r == 23:
            Output = Output + 'W'
        if r == 24:
            Output = Output + 'X'
        if r == 25:
            Output = Output + 'Y'
        if r == 26:
            Output = Output + 'Z'
        if r == 0:
            Output = Output + ' '
        if r == 27:
            Output = Output + '`'
        if r == 28:
            Output = Output + '~'
        if r == 29:
            Output = Output + '1'
        if r == 30:
            Output = Output + '!'
        if r == 31:
            Output = Output + '2'
        if r == 32:
            Output = Output + '@'
        if r == 33:
            Output = Output + '3'
        if r == 34:
            Output = Output + '#'
        if r == 35:
            Output = Output + '4'
        if r == 36:
            Output = Output + '$'
        if r == 37:
            Output = Output + '5'
        if r == 38:
            Output = Output + '%'
        if r == 39:
            Output = Output + '6'
        if r == 40:
            Output = Output + '^'
        if r == 41:
            Output = Output + '7'
        if r == 42:
            Output = Output + '&'
        if r == 43:
            Output = Output + '8'
        if r == 44:
            Output = Output + '*'
        if r == 45:
            Output = Output + '9'
        if r == 46:
            Output = Output + '('
        if r == 47:
            Output = Output + '0'
        if r == 48:
            Output = Output + ')'
        if r == 49:
            Output = Output + '-'
        if r == 50:
            Output = Output + '_'
        if r == 51:
            Output = Output + '='
        if r == 52:
            Output = Output + '+'
        if r == 53:
            Output = Output + '['
        if r == 54:
            Output = Output + '{'
        if r == 55:
            Output = Output + ']'
        if r == 56:
            Output = Output + '}'
        if r == 57:
            Output = Output + '\\'
        if r == 58:
            Output = Output + '|'
        if r == 59:
            Output = Output + ';'
        if r == 60:
            Output = Output + ':'
        if r == 61:
            Output = Output + "'"
        if r == 62:
            Output = Output + '"'
        if r == 63:
            Output = Output + ','
        if r == 64:
            Output = Output + '<'
        if r == 65:
            Output = Output + '.'
        if r == 66:
            Output = Output + '>'
        if r == 67:
            Output = Output + '/'
        if r == 68:
            Output = Output + '?'

        Count = Count+1

    return(Output)
        
    
def Decode(BitCrypt, Text):
    
    #Turns BitCrypt Code Into Required Format
    Count = 0
    for u in BitCrypt:
        ShiftList.append(u)
    
    for o in ShiftList:
        if o == 'a':
            ShiftList[Count] = 1
        if o == 'b':
            ShiftList[Count] = 2
        if o == 'c':
            ShiftList[Count] = 3
        if o == 'd':
            ShiftList[Count] = 4
        if o == 'e':
            ShiftList[Count] = 5
        if o == 'f':
            ShiftList[Count] = 6
        if o =='g':
            ShiftList[Count] = 7
        if o =='h':
            ShiftList[Count] = 8
        if o == 'i':
            ShiftList[Count] = 9
        if o == 'j':
            ShiftList[Count] = 10
        if o == 'k':
            ShiftList[Count] = 11
        if o == 'l':
            ShiftList[Count] = 12
        if o == 'm':
            ShiftList[Count] = 13
        if o == 'n':
            ShiftList[Count] = 14
        if o == 'o':
            ShiftList[Count] = 15
        if o == 'p':
            ShiftList[Count] = 16
        if o == 'q':
            ShiftList[Count] = 17
        if o == 'r':
            ShiftList[Count] = 18
        if o == 's':
            ShiftList[Count] = 19
        if o == 't':
            ShiftList[Count] = 20
        if o == 'u':
            ShiftList[Count] = 21
        if o == 'v':
            ShiftList[Count] = 22
        if o == 'w':
            ShiftList[Count] = 23
        if o == 'x':
            ShiftList[Count] = 24
        if o == 'y':
            ShiftList[Count] = 25
        if o == 'z':
            ShiftList[Count] = 26
        if o == ' ':
            ShiftList[Count] = 0
        if o == '`':
            ShiftList[Count] = 27
        if o == '~':
            ShiftList[Count] = 28
        if o == '1':
            ShiftList[Count] = 29
        if o == '!':
            ShiftList[Count] = 30
        if o == '2':
            ShiftList[Count] = 31
        if o == '@':
            ShiftList[Count] = 32
        if o == '3':
            ShiftList[Count] = 33
        if o == '#':
            ShiftList[Count] = 34
        if o == '4':
            ShiftList[Count] = 35
        if o == '$':
            ShiftList[Count] = 36
        if o == '5':
            ShiftList[Count] = 37
        if o == '%':
            ShiftList[Count] = 38
        if o == '6':
            ShiftList[Count] = 39
        if o == '^':
            ShiftList[Count] = 40
        if o == '7':
            ShiftList[Count] = 41
        if o == '&':
            ShiftList[Count] = 42
        if o == '8':
            ShiftList[Count] = 43
        if o == '*':
            ShiftList[Count] = 44
        if o == '9':
            ShiftList[Count] = 45
        if o == '(':
            ShiftList[Count] = 46
        if o == '0':
            ShiftList[Count] = 47
        if o == ')':
            ShiftList[Count] = 48
        if o == '-':
            ShiftList[Count] = 49
        if o == '_':
            ShiftList[Count] = 50
        if o == '=':
            ShiftList[Count] = 51
        if o == '+':
            ShiftList[Count] = 52
        if o == '[':
            ShiftList[Count] = 53
        if o == '{':
            ShiftList[Count] = 54
        if o == ']':
            ShiftList[Count] = 55
        if o == '}':
            ShiftList[Count] = 56
        if o == '\\':
            ShiftList[Count] = 57
        if o == '|':
            ShiftList[Count] = 58
        if o == ';':
            ShiftList[Count] = 59
        if o == ':':
            ShiftList[Count] = 60
        if o == "'":
            ShiftList[Count] = 61
        if o == '"':
            ShiftList[Count] = 62
        if o == ',':
            ShiftList[Count] = 63
        if o == '<':
            ShiftList[Count] = 64
        if o == '.':
            ShiftList[Count] = 65
        if o == '>':
            ShiftList[Count] = 66
        if o == '/':
            ShiftList[Count] = 67
        if o == '?':
            ShiftList[Count] = 68

        Count = Count+1
    
    #Turns Input Text Into Required Format
    Count = 0
    for i in Text:
        TextList.append(i)
    
    for a in TextList:
        if a == 'a':
            TextList[Count] = 1
        if a == 'b':
            TextList[Count] = 2
        if a == 'c':
            TextList[Count] = 3
        if a == 'd':
            TextList[Count] = 4
        if a == 'e':
            TextList[Count] = 5
        if a == 'f':
            TextList[Count] = 6
        if a =='g':
            TextList[Count] = 7
        if a =='h':
            TextList[Count] = 8
        if a == 'i':
            TextList[Count] = 9
        if a == 'j':
            TextList[Count] = 10
        if a == 'k':
            TextList[Count] = 11
        if a == 'l':
            TextList[Count] = 12
        if a == 'm':
            TextList[Count] = 13
        if a == 'n':
            TextList[Count] = 14
        if a == 'o':
            TextList[Count] = 15
        if a == 'p':
            TextList[Count] = 16
        if a == 'q':
            TextList[Count] = 17
        if a == 'r':
            TextList[Count] = 18
        if a == 's':
            TextList[Count] = 19
        if a == 't':
            TextList[Count] = 20
        if a == 'u':
            TextList[Count] = 21
        if a == 'v':
            TextList[Count] = 22
        if a == 'w':
            TextList[Count] = 23
        if a == 'x':
            TextList[Count] = 24
        if a == 'y':
            TextList[Count] = 25
        if a == 'z':
            TextList[Count] = 26
        if a == ' ':
            TextList[Count] = 0
        if a == '`':
            TextList[Count] = 27
        if a == '~':
            TextList[Count] = 28
        if a == '1':
            TextList[Count] = 29
        if a == '!':
            TextList[Count] = 30
        if a == '2':
            TextList[Count] = 31
        if a == '@':
            TextList[Count] = 32
        if a == '3':
            TextList[Count] = 33
        if a == '#':
            TextList[Count] = 34
        if a == '4':
            TextList[Count] = 35
        if a == '$':
            TextList[Count] = 36
        if a == '5':
            TextList[Count] = 37
        if a == '%':
            TextList[Count] = 38
        if a == '6':
            TextList[Count] = 39
        if a == '^':
            TextList[Count] = 40
        if a == '7':
            TextList[Count] = 41
        if a == '&':
            TextList[Count] = 42
        if a == '8':
            TextList[Count] = 43
        if a == '*':
            TextList[Count] = 44
        if a == '9':
            TextList[Count] = 45
        if a == '(':
            TextList[Count] = 46
        if a == '0':
            TextList[Count] = 47
        if a == ')':
            TextList[Count] = 48
        if a == '-':
            TextList[Count] = 49
        if a == '_':
            TextList[Count] = 50
        if a == '=':
            TextList[Count] = 51
        if a == '+':
            TextList[Count] = 52
        if a == '[':
            TextList[Count] = 53
        if a == '{':
            TextList[Count] = 54
        if a == ']':
            TextList[Count] = 55
        if a == '}':
            TextList[Count] = 56
        if a == '\\':
            TextList[Count] = 57
        if a == '|':
            TextList[Count] = 58
        if a == ';':
            TextList[Count] = 59
        if a == ':':
            TextList[Count] = 60
        if a == "'":
            TextList[Count] = 61
        if a == '"':
            TextList[Count] = 62
        if a == ',':
            TextList[Count] = 63
        if a == '<':
            TextList[Count] = 64
        if a == '.':
            TextList[Count] = 65
        if a == '>':
            TextList[Count] = 66
        if a == '/':
            TextList[Count] = 67
        if a == '?':
            TextList[Count] = 68

        Count = Count+1
        
    #TextList[2213%len(TextList)]
    #Decodes Text
    Count = 0
    for q in TextList:
        p = int(q)
        OutList.append(p-ShiftList[Count%len(ShiftList)])
        Count = Count+1
    
    #Reverts To Text Format
    Output = ''
    for w in OutList:
        r = w%69
        Count = 0
        if r == 1:
            Output = Output + 'A'
        if r == 2:
            Output = Output + 'B'
        if r == 3:
            Output = Output + 'C'
        if r == 4:
            Output = Output + 'D'
        if r == 5:
            Output = Output + 'E'
        if r == 6:
            Output = Output + 'F'
        if r == 7:
            Output = Output + 'G'
        if r == 8:
            Output = Output + 'H'
        if r == 9:
            Output = Output + 'I'
        if r == 10:
            Output = Output + 'J'
        if r == 11:
            Output = Output + 'K'
        if r == 12:
            Output = Output + 'L'
        if r == 13:
            Output = Output + 'M'
        if r == 14:
            Output = Output + 'N'
        if r == 15:
            Output = Output + 'O'
        if r == 16:
            Output = Output + 'P'
        if r == 17:
            Output = Output + 'Q'
        if r == 18:
            Output = Output + 'R'
        if r == 19:
            Output = Output + 'S'
        if r == 20:
            Output = Output + 'T'
        if r == 21:
            Output = Output + 'U'
        if r == 22:
            Output = Output + 'V'
        if r == 23:
            Output = Output + 'W'
        if r == 24:
            Output = Output + 'X'
        if r == 25:
            Output = Output + 'Y'
        if r == 26:
            Output = Output + 'Z'
        if r == 0:
            Output = Output + ' '
        if r == 27:
            Output = Output + '`'
        if r == 28:
            Output = Output + '~'
        if r == 29:
            Output = Output + '1'
        if r == 30:
            Output = Output + '!'
        if r == 31:
            Output = Output + '2'
        if r == 32:
            Output = Output + '@'
        if r == 33:
            Output = Output + '3'
        if r == 34:
            Output = Output + '#'
        if r == 35:
            Output = Output + '4'
        if r == 36:
            Output = Output + '$'
        if r == 37:
            Output = Output + '5'
        if r == 38:
            Output = Output + '%'
        if r == 39:
            Output = Output + '6'
        if r == 40:
            Output = Output + '^'
        if r == 41:
            Output = Output + '7'
        if r == 42:
            Output = Output + '&'
        if r == 43:
            Output = Output + '8'
        if r == 44:
            Output = Output + '*'
        if r == 45:
            Output = Output + '9'
        if r == 46:
            Output = Output + '('
        if r == 47:
            Output = Output + '0'
        if r == 48:
            Output = Output + ')'
        if r == 49:
            Output = Output + '-'
        if r == 50:
            Output = Output + '_'
        if r == 51:
            Output = Output + '='
        if r == 52:
            Output = Output + '+'
        if r == 53:
            Output = Output + '['
        if r == 54:
            Output = Output + '{'
        if r == 55:
            Output = Output + ']'
        if r == 56:
            Output = Output + '}'
        if r == 57:
            Output = Output + '\\'
        if r == 58:
            Output = Output + '|'
        if r == 59:
            Output = Output + ';'
        if r == 60:
            Output = Output + ':'
        if r == 61:
            Output = Output + "'"
        if r == 62:
            Output = Output + '"'
        if r == 63:
            Output = Output + ','
        if r == 64:
            Output = Output + '<'
        if r == 65:
            Output = Output + '.'
        if r == 66:
            Output = Output + '>'
        if r == 67:
            Output = Output + '/'
        if r == 68:
            Output = Output + '?'

        Count = Count+1

    return(Output)
