print("Hello, World!")

import os
print("Current working directory:", os.getcwd())
#os.chdir
#os.mkdir("new_directory")
for file in os.listdir():
    #print("Files in current directory:", file,"   " , os.path.isdir(file))
    print(os.path.abspath(file))

script_dir = os.path.dirname(os.path.abspath(__file__))
print("Script directory:", script_dir)
