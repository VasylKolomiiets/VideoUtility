def break_str(row, n):
    if len(row) <= n  or  n < 2:
        return row
    else:
        return row[:n] + "\n" + break_str(row[n:], n)

if __name__ == "__name__":            
    txt = "test string ttt "

    for i in range(3,16):
        print(F"{20*"-|-"} {i=}")
        print(break_str(txt, i))






        # i_tail = int(0.8*n) - 1
        # blank_index = row.find(" ", i_tail, n+1)
        # if blank_index > 0:
        #     return row[:blank_index] + "\n" + break_str(row[blank_index+1:], n)