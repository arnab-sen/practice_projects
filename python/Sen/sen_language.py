"""
Sen is a Python-based programming language developed by Arnab Sen.
This is currently for educational purposes only.

TODO:
- Check if "=" is in a string, if not then do the variable assignment
"""
def get_script(filename):
    if filename[-4:].lower() != ".sen":
        filename = filename + ".sen"
        
    with open(filename) as file:
        script = file.read().split("\n")

    return script

def interpret_script(script, functions):
    variables = {}
    for line in script:
        l = line.strip()
        if len(l) > 0:
            bracket = l.find("(")

            # Functions
            if bracket != -1:
                args = l[bracket + 1 : l.find(")")].strip()
                #print(variables)
                if args in variables:
                    args = variables[args]
                else:
                    variables[args] = type_cast(args)
                    
                function_name = l[:bracket]
                #print(function_name)
                #print(args)
                functions[function_name](args)
                
            # Variable assignment
            if "=" in line and line.find("=") != len(line) - 1:
                var_name = line[:line.find("=")]
                assignment = line[line.find("=") + 1:]
                variables[var_name.strip()] = type_cast(assignment)
            

def type_cast(string):
    # Determines the type to convert the input string,
    # and returns a the converted variable
    string = string.strip()
    #print(string)

    if string[0] == '"' == string[-1]:
        return string[1 : -1]
    elif string.lower() == "true" or string.lower() == "false":
        return bool(string)
    elif "." in string:
        if "." == string[-1]:
            # Invalid float, so return int part only
            return int(string[-1])
        else:
            return float(string)
    else:
        try:
            return int(string)
        except:
            print("ERROR: Variable {} of unknown type".format(string))
            return string        

def disp(text):
    print(text)

def main():
    script = get_script("test")
    functions = {
                    "disp" : disp
                    }
    
    # Print "Hello, world"
    interpret_script(script, functions)

if __name__ == "__main__":
    main()
