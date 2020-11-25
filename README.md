# grammar-for-primary-numbers
Solver for primary numbers

# Задача
1. Построить машину Тьюринга (*МТ*) и линейный ограниченный автомат (*LBA*), допускающие язык **L** простых чисел в унарной системе счисления.
2. Далее:
	1. Для МТ написать транслятор в КС грамматику, которая порождает тот же язык **L**.
	2. Для LBA написать транслятор в КЗ грамматику, которая порождает тот же язык **L**.
3. Написать генератор слов, выводимых в грамматике.

# Решение
1. Файлы automaton.txt и automaton_lba.txt для МТ и LBA соответственно.
2. 
	1. Файл translator.py
	2. Файл translator_lba.py
3. Файл generator.py

## Запуск
#### Неограниченная грамматика
```bash
pypy3 translator.py
pypy3 run.py grammar.txt <number> 
```

Вместо pypy3 можно использовать python3 (снижает производительность):

```bash
python3 translator.py
python3 run.py grammar.txt <number> 
```
#### КЗ грамматика
```bash
pypy3 translator_lba.py
pypy3 run.py grammar_lba.txt <number>
```
Далее построчно вводим числа. На каждое получим ответ **YES**, если введенное слово выводимо в данной КС грамматике и **NO**, если нет.
