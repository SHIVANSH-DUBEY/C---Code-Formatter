global stack  # Declaring stack to keep track of number of loops
global tests  # we will use to check if there are no intentation error
global width_of_tab
stack = []  # initializing the stack
tests = []
width_of_tab = 4  # tab size

raw_code = open("test.cpp", "r")  # open a replica of the original file
lines_array = raw_code.readlines()

def push_to_stack():
    # If a loop is found  we will add 4 more spaces
    stack.append(stack[len(stack) - 1] + width_of_tab)


def inspect(spaces, line_index):
    if (spaces == stack[len(stack) - 1]):
        tests.append(True)
    else:
        tests.append(False)
        print("Indentation error found at line %d. Instead of %d spaces, given code has %d spaces" % (
            line_index, stack[len(stack) - 1], spaces))
        lines_array[line_index-1] = lines_array[line_index-1].lstrip()
        k = " "*stack[len(stack) - 1]
        k += lines_array[line_index-1]
        lines_array[line_index-1] = k


def analyze(file_pointer, char_pointer, lineNumber):
    file_pointer.seek(char_pointer)
    counter = lineNumber
    flag = 0
    while (stack != []):
        for l in file_pointer:
            counter += 1
            if (l.find("/*") != -1):
                flag += 1
            if(flag > 0):
                if(l.find("*/") != -1):
                    flag -= 1
                else:
                    continue
            if (l.find("/*") != -1):
                flag += 1
            if (l.find("{") != -1):
                # In case an opening curly brace is found ,we will add 4 more spaces
                push_to_stack()
            else:  # check for any intentation error in the line
                if (l == '\n'):
                    continue  # we will do noting if the line is empty
                if (l.find("}") != -1):
                    # If we find a closing curly brace , we will pop 4 spaces from the stack
                    stack.remove(stack[len(stack) - 1])
                spaces = 0
                for char in l:
                    # Find number of whitespaces in the beginning of line
                    if (char.isspace() == True):
                        spaces += 1
                    else:
                        break
                # Checking if whitespaces match
                inspect(spaces, counter)
        stack.remove(stack[len(stack) - 1])  # Popping from stack


stack.append(0)  # zero spaces are required at the beginning!
lineNumber = 0  # Keeping track of which line we are at to print out errors
char_pointer = 0
flag = 0  # This is to skip any curly braces inside multiline comment
for line in raw_code:  # Finding the first curly brace
    lineNumber += 1
    char_pointer += len(line)
    if (line.find("/*") != -1):
        flag += 1
    if(flag > 0):
        if(line.find("*/") != -1):
            flag -= 1
        else:
            continue
    if (line.find("/*") != -1):
        flag += 1
    pos = line.find("{")
    if (pos != -1):
        push_to_stack()  # Appending to stack
        break
analyze(raw_code, char_pointer, lineNumber)
if (False not in tests):
    print("The code is already formatted.")

with open('test6.txt', 'w') as file:  # writing the formatted code into new file
    file.writelines(lines_array)
