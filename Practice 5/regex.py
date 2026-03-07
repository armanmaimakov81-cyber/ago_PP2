#1:
import re
text = "ab, a, abbb, c"
print(re.findall(r"ab*", text))
#2:
text = "ab, abb, abbb, abbbb"
print(re.findall(r"ab{2,3}", text))
#3:
text = "abc_def, Hello_world, test_case, simple"
print(re.findall(r"[a-z]+_[a-z]+", text))
#4:
text = "Apple, apple, Zebra, RUN, Table"
print(re.findall(r"\b[A-Z][a-z]*\b", text))
#5:
text = "axxxb, a123b, ab, acc"
print(re.findall(r"a.*b", text))
#6:
text = "Python, exercises. hello world"
print(re.sub(r"[ ,.]", ":", text))
#7:
text = "snake_case_string"
words = re.split(r"_", text)
camel_case = "".join(word.capitalize() for word in words)
print(camel_case)
#8:
text = "SplitAtUppercaseLetters"
print(re.findall(r"[A-Z][^A-Z]*", text))
#9:
text = "InsertSpacesBetweenWords"
print(re.sub(r"([a-z])([A-Z])", r"\1 \2", text))
#10:
text = "ConvertCamelCaseToSnakeCase"
print(re.sub(r"([a-z])([A-Z])", r"\1_\2", text).lower())
