with open("src/App.tsx", "r") as f:
    lines = f.readlines()

new_lines = []
for i, l in enumerate(lines):
    if i in [801, 802, 829]:
        continue
    new_lines.append(l)

with open("src/App.tsx", "w") as f:
    f.writelines(new_lines)
