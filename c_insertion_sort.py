def insertion_sort(arr):
    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    trocas = 0
    
    for i in range(1, n):
        key = lista[i]
        j = i - 1
        
        # Move elementos maiores que key para a direita
        while j >= 0:
            comparacoes += 1
            if key < lista[j]:
                lista[j + 1] = lista[j]
                trocas += 1
                j -= 1
            else:
                break
                
        lista[j + 1] = key
    
    return lista, comparacoes, trocas