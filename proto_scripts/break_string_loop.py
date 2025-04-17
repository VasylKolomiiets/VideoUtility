def break_str_iterative(row, n, tail=0.7):
    result = []
    while len(row) > n and n >= 2:
        i_tail = int(tail * n) - 1
        blank_index = row.find(" ", i_tail, n + 1)
        if blank_index > 0:
            result.append(row[:blank_index])
            row = row[blank_index + 1 :]
        else:
            result.append(row[:n])
            row = row[n:]
    result.append(row)  # Додаємо залишок рядка
    return "\n".join(result)


if __name__ == "__main__":            
    txt = "Серія 26. Vibe coding vs AImbiotic coding. ШІмбіотичне програмування"
    print("Start", 20*"-->")

    for i in range(8):
        par = 0.5 + i*0.05
        print(F"{20*"-|-"} {par=}")
        print(break_str_iterative(txt, 15, par))


# "Серія_20.\nПриклад\nнарізки відео\nнашими\nфункціями.\nДіємо покроково"
# "Серія_20. Приклад нарізки відео нашими функціями. Діємо покроково"

