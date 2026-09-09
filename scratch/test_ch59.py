# verify ch59
with open(r"c:\Users\ramaw\RD SHARMA OF AI ( A BOOK WHICH MAKE ANY ONE A WHORLD BEST AI ENGINEER)\book_builder\ch59_coding_agents.html", "r", encoding="utf-8") as f:
    text = f.read()

count_dd = text.count("$$")
print("Double dollar count:", count_dd, "(Even?", count_dd % 2 == 0, ")")
for i in range(1, 9):
    p_tag = f"Problem 5.9.{i}"
    print(p_tag, "in text:", p_tag in text)
print("File length:", len(text), "chars")
