inputStr = 'bnbknbknbknbknkbnkbknkbnkkknknknknkbkbkbkbkbnbnbnbbkbkbkbkbnknkbknbknbknkbknbk'
outputStr = ''
numberOfIteration = 10000

for n in xrange(numberOfIteration):
    i = -1
    while i <len(inputStr):
        i = i +1
        if i == (len(inputStr)-1):

            if inputStr[i] == 'k':
                if inputStr[0] == 'k':
                    outputStr = outputStr + 'b'
                elif inputStr[0] == 'n':
                    outputStr = outputStr + 'k'
                elif inputStr[0] == 'b':
                    outputStr = outputStr + 'b'
            elif inputStr[i] == 'n':
                
                if inputStr[0] == 'k':
                    outputStr = outputStr + 'k'
                elif inputStr[0] == 'n':
                    outputStr = outputStr + 'k'
                elif inputStr[0] == 'b':
                    outputStr = outputStr + 'n'
            elif inputStr[i] == 'b':
                if inputStr[0] == 'k':
                    outputStr = outputStr + 'b'
                elif inputStr[0] == 'n':
                    outputStr = outputStr + 'n'
                elif inputStr[0] == 'b':
                    outputStr = outputStr + 'n'
            else:
                print 'Invalid Input!'
                break        
        elif i<len(inputStr):
            if inputStr[i] == 'k':
                if inputStr[i+1] == 'k':
                    outputStr = outputStr + 'b'
                elif inputStr[i+1] == 'n':
                    outputStr = outputStr + 'k'
                elif inputStr[i+1] == 'b':
                    outputStr = outputStr + 'b'
            elif inputStr[i] == 'n':
                
                if inputStr[i+1] == 'k':
                    outputStr = outputStr + 'k'
                elif inputStr[i+1] == 'n':
                    outputStr = outputStr + 'k'
                elif inputStr[i+1] == 'b':
                    outputStr = outputStr + 'n'
            elif inputStr[i] == 'b':
                if inputStr[i+1] == 'k':
                    outputStr = outputStr + 'b'
                elif inputStr[i+1] == 'n':
                    outputStr = outputStr + 'n'
                elif inputStr[i+1] == 'b':
                    outputStr = outputStr + 'n'
            else:
                print 'Invalid Input!'
                break
    print inputStr, outputStr
    inputStr = outputStr
    outputStr = ''