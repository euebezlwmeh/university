# 7. Генератор для объединения последовательностей по
# заданной стратегии. Сверните возвращемые последовательности 
# в зависимости от типа данных в них.
# К генератору должна быть применена хотя бы одна из функций map, reduce, filter.

from functools import reduce 

def genFunc(seq1, seq2, func):
    if isinstance(seq1, list) and isinstance(seq2, list):
        for i in list(map(func, seq1, seq2)):
            yield i
    elif isinstance(seq1, str) and isinstance(seq2, str):
        for i in list(map(func, seq1, seq2)):
            yield i
    else:
        raise ValueError("Unsupported data types")

def f1(a, b):
    return a + b #sum

def f2(a, b):
    return a * b #mult

seq1 = 'abc'
seq2 = 'def'

for res in genFunc(seq1, seq2, f1):
    print(res)

print(reduce(f1, genFunc(seq1, seq2, f1)))
