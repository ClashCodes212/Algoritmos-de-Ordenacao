import sys
# Aumenta o limite de segurança do Python para evitar erro de recursão em listas grandes
sys.setrecursionlimit(10000)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr, 0, 0, 0
    
    # Escolhe o pivô (elemento do meio)
    pivot = arr[len(arr) // 2]
    
    # Particiona a lista
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Métricas
    comparacoes = len(arr)
    trocas = len(left) + len(right)
    
    # Recursão
    left_sorted, comp_left, trocas_left, recursao_left = quick_sort(left)
    right_sorted, comp_right, trocas_right, recursao_right = quick_sort(right)
    
    # Combina
    resultado = left_sorted + middle + right_sorted
    
    total_comparacoes = comparacoes + comp_left + comp_right
    total_trocas = trocas + trocas_left + trocas_right
    total_recursao = recursao_left + recursao_right + 1
    
    return resultado, total_comparacoes, total_trocas, total_recursao