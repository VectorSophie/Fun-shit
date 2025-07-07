def generate_h_fractal(n):
    if n == 1:
        return ["H"]

    prev = generate_h_fractal(n - 1)
    size = len(prev)
    space = " " * size

    top = [line + space + line for line in prev]
    middle = [line * 3 for line in prev]
    bottom = [line + space + line for line in prev]

    return top + middle + bottom

for line in generate_h_fractal(5):
    print(line)
