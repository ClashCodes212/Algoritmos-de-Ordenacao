def merge_sort(arr):
    if len(arr) <= 1:
        return arr, 0, 0, 0
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Chamadas recursivas
    left_sorted, comp_l, trocas_l, rec_l = merge_sort(left)
    right_sorted, comp_r, trocas_r, rec_r = merge_sort(right)
    
    # Mesclagem
    resultado, comp_m, trocas_m = merge(left_sorted, right_sorted)
    
    total_comparacoes = comp_l + comp_r + comp_m
    total_trocas = trocas_l + trocas_r + trocas_m
    total_recursao = rec_l + rec_r + 1
    
    return resultado, total_comparacoes, total_trocas, total_recursao

def merge(left, right):
    result = []
    i = j = 0
    comparacoes = 0
    trocas = 0
    
    while i < len(left) and j < len(right):
        comparacoes += 1
        # Contamos a movimentação para a lista auxiliar como "troca/escrita"
        trocas += 1
        
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Adiciona o restante
    result.extend(left[i:])
    result.extend(right[j:])
    trocas += len(left[i:]) + len(right[j:])
    
    return result, comparacoes, trocas