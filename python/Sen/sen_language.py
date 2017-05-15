"""
Sen is a Python-based programming language developed by Arnab Sen.
Currently this is for educational purposes only.
"""
def get_script(filename):
    with open(filename + ".sen") as file:
        script = file.read().split("\n")

    return script

def interpret_script(script, functions):
    for line in script:
        l = line.strip()
        bracket = l.find("(")
        args = l[bracket + 1 : l.find(")")]
        function_name = l[:bracket]
        functions[function_name](args)

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
