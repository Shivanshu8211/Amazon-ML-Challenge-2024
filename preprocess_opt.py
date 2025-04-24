string = "6.65in"
string = "3.55\""
string = "14-inch MacBook"
num_started=False
unit_started = False
num=""
unit=""
for i in range(len(string)):
    s=string[i]
    if s == "." and num_started and not unit_started:
        num+=s
    if s == "\"" and num_started and not unit_started:
        unit = "in"
        break
    if s.isdigit() and not unit_started:
        num_started=True
        num+=s
    if s.isnumeric() and unit_started:
        break
    if s.isalpha() and num_started:
        unit_started = True
        unit+=s
    if len(unit)>1:
        break
print(num + " " + unit)