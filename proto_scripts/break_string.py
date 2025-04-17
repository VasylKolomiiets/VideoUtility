def break_str(row, n, tail=0.7):
    if len(row) <= n  or  n < 2:
        return row
    else:
        i_tail = int(tail*n) - 1
        blank_index = row.find(" ", i_tail, n+1)
        if blank_index > 0:
            return row[:blank_index] + "\n" + break_str(row[blank_index+1:], n, tail)
        return row[:n] + "\n" + break_str(row[n:], n, tail)

if __name__ == "__main__":            
    txt = "Серія 23. Підбір оптимального параметра функції нарізки тексту"
    print("Start", 20*"-->")

    for i in range(8):
        par = 0.5 + i*0.05
        print(F"{20*"-|-"} {par=}")
        print(break_str(txt, 15, par))


# "Серія_20.\nПриклад\nнарізки відео\nнашими\nфункціями.\nДіємо покроково"
# "Серія_20. Приклад нарізки відео нашими функціями. Діємо покроково"

