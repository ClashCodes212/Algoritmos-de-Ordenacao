def selection_sort(arr):
    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    trocas = 0
    
    for i in range(n):
        # Assume que o atual é o menor
        min_idx = i
        
        # Procura o verdadeiro menor no restante da lista
        for j in range(i + 1, n):
            comparacoes += 1
            if lista[j] < lista[min_idx]:
                min_idx = j
        
        # Se encontrou alguém menor, faz a troca
        if min_idx != i:
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
            trocas += 1
    
    return lista, comparacoes, trocas