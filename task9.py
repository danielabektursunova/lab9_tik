import heapq
import math
from collections import Counter
from itertools import count


def build_huffman(freq):
    # Построение дерева Хаффмана и генерация таблицы кодов
    if not freq:
        raise ValueError("Пустой алфавит")

    order = count()
    # Исключение символов с нулевой частотой
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    heapq.heapify(heap)

    if not heap:
        raise ValueError("Все частоты нулевые")

    # Обработка случая с единственным уникальным символом
    if len(heap) == 1:
        symbol = heap[0][2]
        return symbol, {symbol: "0"}

    # Объединение узлов с наименьшими весами
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))

    tree = heap[0][2]
    codes = {}

    # Обход дерева и формирование префиксных кодов
    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


def calculate_metrics(freq, codes):
    # Расчёт вероятностей, энтропии, средней длины и эффективности
    total_symbols = sum(freq.values())
    probs = {s: w / total_symbols for s, w in freq.items() if w > 0}

    # Вычисление энтропии Шеннона
    H_X = -sum(p * math.log2(p) for p in probs.values())

    # Вычисление средней длины кодового слова
    L_bar = sum(probs[s] * len(codes[s]) for s in probs)

    # Вычисление эффективности кодирования
    eta = (H_X / L_bar * 100) if L_bar > 0 else 0.0

    return probs, H_X, L_bar, eta


def encode(text, codes):
    # Кодирование исходного текста в битовую строку
    return "".join(codes[s] for s in text)


def decode(bits, tree):
    # Декодирование битовой строки по дереву
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)

    result, node = [], tree
    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree

    if node is not tree:
        raise ValueError("Неполное кодовое слово")

    return "".join(result)


# Проверка работы программы на контрольном сообщении
text = "ABCADE"
freq = Counter(text)

tree, codes = build_huffman(freq)
probs, H_X, L_bar, eta = calculate_metrics(freq, codes)
encoded_bits = encode(text, codes)
decoded_text = decode(encoded_bits, tree)

# Проверка совпадения декодированного текста с исходным
assert decoded_text == text

print("Частоты символов:", dict(freq))
print("Таблица кодов:", codes)
print("Закодированная строка:", encoded_bits)
print("Длина битовой строки:", len(encoded_bits))
print("Декодированный текст:", decoded_text)
print("Энтропия H(X):", round(H_X, 4))
print("Средняя длина L:", round(L_bar, 4))
print("Эффективность:", round(eta, 2), "%")