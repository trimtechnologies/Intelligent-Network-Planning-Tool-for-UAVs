import re

# val = "21S145270"
val = "21145270"

# print(re.search('[a-zA-Z]', val))

print(not any(c.isalpha() for c in val))