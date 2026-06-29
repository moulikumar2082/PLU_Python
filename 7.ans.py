file = open("student.txt", "w")
file.write("mouli")
file.close()

file = open("student.txt", "r")
content = file.read()
print(content)
file.close()