from bs4 import BeautifulSoup

grades = []
file = open("grade_html/mixed.html", "r")
soup = BeautifulSoup(file.read())
for s in soup.find_all("option"):
    grades.append(s.string)
print(grades)
