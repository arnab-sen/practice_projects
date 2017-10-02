"""Reads in file byte data and outputs a combined file"""
FILE_SEP = b"<FILE>"
SEP = b"<_-_>"

def f2c():
    """Input: Multiple files; Output: A single .COMBINED file"""
    dir_in = "f2c in/"
    dir_out = "f2c out/"
    filenames_in = ["a.txt", "b.txt", "f2.png"]
    contents = {}
    for filename in filenames_in:
        with open(dir_in + filename, "rb") as f:
            contents[filename] = f.read()
    #print(contents)
    with open(dir_out + "c.COMBINED", "wb") as f:
        for filename in contents:
            f.write(FILE_SEP + str.encode(filename) + SEP)
            f.write(contents[filename] + b"\n")

def c2f():
    """Input: A single .COMBINED file; Output: Multiple files"""
    dir_in = "f2c out/"
    dir_out = "c2f out/"
    filename_in = "c.COMBINED"
    contents = []
    sep_contents = {}
    with open(dir_in + filename_in, "rb") as f:
        contents = f.read().split(b"<FILE>")

    for i, item in enumerate(contents):
        if SEP in item:
            data = item.split(SEP)
            sep_contents[bytes.decode(data[0])] = data[1]

    for filename in sep_contents:
        with open(dir_out + filename, "wb") as f:
            f.write(sep_contents[filename])
            
    #print(sep_contents)
    #print(contents[:2])
    #print(bytes.decode(contents[:10]))

def main():
    f2c()
    c2f()

if __name__ == "__main__":
    main()
