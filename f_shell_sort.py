def shell_sort(arr):
    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    trocas = 0
    
    # Sequência de gaps (divisão por 2)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = lista[i]
            j = i
            
            # A primeira comparação do while ocorre sempre
            if j >= gap:
                comparacoes += 1
                
            while j >= gap and lista[j - gap] > temp:
                lista[j] = lista[j - gap]
                trocas += 1
                j -= gap
                
                # Próximas comparações dentro do loop
                if j >= gap:
                    comparacoes += 1
            
            lista[j] = temp
            trocas += 1
        
        gap //= 2
    
    return lista, comparacoes, trocas