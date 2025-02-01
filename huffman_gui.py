import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import heapq
from graphviz import Digraph


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]


def build_huffman_codes(root):
    codes = {}

    def generate_codes(node, current_code):
        if not node:
            return
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(root, "")
    return codes


def encode_text(text, codes):
    return "".join(codes[char] for char in text)


def decode_text(encoded_text, root):
    decoded_text = []
    current = root
    for bit in encoded_text:
        if bit == "0":
            current = current.left
        else:
            current = current.right
        if current.left is None and current.right is None:
            decoded_text.append(current.char)
            current = root
    return "".join(decoded_text)


def generate_huffman_tree_graph(root):
    graph = Digraph()
    graph.node("root", label=f"Freq: {root.freq}")

    def add_nodes(node, parent_label, edge_label):
        if not node:
            return
        label = f"Freq: {node.freq}" if node.char is None else f"Char: {node.char}\nFreq: {node.freq}"
        node_id = id(node)
        graph.node(str(node_id), label=label)
        graph.edge(parent_label, str(node_id), label=edge_label)
        add_nodes(node.left, str(node_id), "0")
        add_nodes(node.right, str(node_id), "1")

    add_nodes(root.left, "root", "0")
    add_nodes(root.right, "root", "1")

    return graph


def process_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Erro", "Digite um texto para codificar!")
        return

    # Construir a árvore de Huffman
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded = encode_text(text, codes)
    decoded = decode_text(encoded, root)

    # Exibir resultados
    codes_display = "\n".join(f"{repr(char)}: {code}" for char, code in codes.items())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Tabela de Conversão:\n{codes_display}\n\n")
    output_text.insert(tk.END, f"Texto Codificado:\n{encoded}\n\n")
    output_text.insert(tk.END, f"Texto Decodificado:\n{decoded}\n\n")

    # Gerar e exibir o gráfico da árvore
    graph = generate_huffman_tree_graph(root)
    graph.render("huffman_tree", format="png", cleanup=True)
    messagebox.showinfo("Árvore Gerada", "A árvore de Huffman foi salva como 'huffman_tree.png'!")


# Criar a interface gráfica
app = tk.Tk()
app.title("Codificador e Decodificador de Huffman")
app.geometry("800x600")

# Entrada de texto
input_label = tk.Label(app, text="Digite o texto para codificar:", font=("Arial", 14))
input_label.pack(pady=10)

input_text = tk.Text(app, height=5, font=("Arial", 12))
input_text.pack(pady=10, padx=20, fill=tk.X)

# Botão para processar o texto
process_button = ttk.Button(app, text="Codificar", command=process_text)
process_button.pack(pady=10)

# Área de saída
output_label = tk.Label(app, text="Resultados:", font=("Arial", 14))
output_label.pack(pady=10)

output_text = tk.Text(app, height=20, font=("Courier New", 12), bg="#f0f0f0")
output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Iniciar o loop da interface
app.mainloop()
