import collections
import math
from itertools import count


def build_huffman(freq):
    # Построение дерева Хаффмана и генерация таблицы кодов
    if not freq:
        raise ValueError("Пустой алфавит")

    order = count()
    # Исключение символов с нулевой частотой
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    import heapq

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


# Исследуемый текст (не менее 300 символов, с учётом регистра, пробелов и знаков препинания)
text = (
    "Теория информации и кодирования представляет собой фундаментальный раздел "
    "современной науки, изучающий математические законы передачи, хранения и "
    "обработки информации. Код Хаффмана является одним из наиболее известных "
    "алгоритмов префиксного сжатия данных без потерь."
)

# Подсчёт частот символов
freq = collections.Counter(text)
total_symbols = len(text)

# Построение кодов и расчёт метрик
tree, codes = build_huffman(freq)
probs = {s: w / total_symbols for s, w in freq.items()}

# Вычисление энтропии Шеннона
H_X = -sum(p * math.log2(p) for p in probs.values())

# Вычисление средней длины кодового слова
L_bar = sum(probs[s] * len(codes[s]) for s in freq)

# Вычисление эффективности кодирования
eta = (H_X / L_bar * 100) if L_bar > 0 else 0.0
redundancy = 100.0 - eta

# Расчёт объёмов
utf8_bytes = len(text.encode("utf-8"))
huffman_bits = sum(freq[s] * len(codes[s]) for s in freq)
huffman_bytes_padded = math.ceil(huffman_bits / 8)

print("Длина текста в символах:", total_symbols)
print("Количество уникальных символов:", len(freq))
print("Энтропия H(X):", round(H_X, 4))
print("Средняя длина L:", round(L_bar, 4))
print("Эффективность:", round(eta, 2), "%")
print("Избыточность:", round(redundancy, 2), "%")
print("Объем исходного текста в UTF-8 (байты):", utf8_bytes)
print("Чистый объем сжатых данных (биты):", huffman_bits)
print("Объем с выравниванием до байтов (байты):", huffman_bytes_padded)