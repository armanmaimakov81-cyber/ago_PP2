import os
import shutil
#1:
shutil.copy("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\file_handling\\sample.txt", "C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\file_handling\\backup_sample.txt")
print("File copied")
#2:
if os.path.exists("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\file_handling\\backup_sample.txt"):
    os.remove("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\file_handling\\backup_sample.txt")
    print("File deleted")
else:
    print("File not found")
