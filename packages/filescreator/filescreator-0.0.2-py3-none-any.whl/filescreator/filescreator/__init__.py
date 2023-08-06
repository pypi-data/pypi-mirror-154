import os
def create_file(**key):
    for i in key:
        if i == "Filename":
            b = key[i]
            break
        else:
            raise ValueError("No filename specified, please type a filename like this 'Filename='filename.txt'")
    for i in key:
        if i == "Content":
            a = key[i]
            break
    with open(b, "w") as f:
        f.write(a)
    print("File created successfully!")
def write(Filename, Content):
    with open(Filename, "a") as f:
        f.write(Content + "\n")
    print("File written successfully!")
def read(Filename):
    with open(Filename, "r") as f:
        print(f.read())
def delete(Filename):
    os.remove(Filename)
    print("File deleted successfully!")
    