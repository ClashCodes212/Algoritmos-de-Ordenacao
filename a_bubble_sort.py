def bubble_sort(arr):
    # Trabalha com uma cópia para não alterar a lista original
    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    trocas = 0
    
    for i in range(n):
        trocou = False
        # O loop vai até n-i-1 porque os últimos i elementos já estão ordenados
        for j in range(0, n - i - 1):
            comparacoes += 1
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocas += 1
                trocou = True
        
        # Se não houve troca nesta passagem, a lista já está ordenada
        if not trocou:
            break
    
    return lista, comparacoes, trocas