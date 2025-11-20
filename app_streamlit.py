import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

import a_bubble_sort
import b_selection_sort  
import c_insertion_sort
import d_merge_sort
import e_quick_sort
import f_shell_sort

st.set_page_config(page_title="Relatório Final de Algoritmos", layout="wide", page_icon="📊")
st.title("📊 Relatório Final: Análise de Algoritmos")

CONFIG_CORES = {
    "Bubble Sort":    {"cor": "#d62728", "icone": "🔴"}, 
    "Selection Sort": {"cor": "#9467bd", "icone": "🟣"}, 
    "Insertion Sort": {"cor": "#ff7f0e", "icone": "🟠"}, 
    "Shell Sort":     {"cor": "#e377c2", "icone": "🌸"}, 
    "Merge Sort":     {"cor": "#2ca02c", "icone": "🟢"}, 
    "Quick Sort":     {"cor": "#1f77b4", "icone": "🔵"} 
}

# MENU LATERAL
st.sidebar.header("⚙️ Parâmetros do Teste")

tamanho_selecionado = st.sidebar.selectbox(
    "Tamanho Máximo da Entrada (N)",
    options=[10, 100, 1000, 10000],
    index=2
)

tipo_lista = st.sidebar.selectbox("Cenário dos Dados", ["Aleatória", "Ordenada", "Inversa"])

#FUNÇÕES AUXILIARES
@st.cache_data
def gerar_lista(tamanho, tipo):
    # Gera a lista de teste baseada no cenário escolhido.
    if tipo == "Aleatória":
        return random.sample(range(tamanho * 10), tamanho)
    elif tipo == "Ordenada":
        return list(range(tamanho))
    else:
        return list(range(tamanho, 0, -1))

def executar_algoritmo(nome, algoritmo, lista):
    inicio = time.time()
    
    # Tratamento especial para algoritmos recursivos (evitar crash no Streamlit)
    if nome in ["Merge Sort", "Quick Sort"]:
        try:
            _, comp, trocas, recursao = algoritmo(lista)
        except RecursionError:
            return None, 0, 0, 0
    else:
        _, comp, trocas = algoritmo(lista)
        recursao = 0
        
    tempo = time.time() - inicio
    return tempo, comp, trocas, recursao

# --- LÓGICA DE EXECUÇÃO ---
if st.sidebar.button("Gerar Relatório Completo", type="primary"):
    # Define a progressão de tamanhos
    todos_tamanhos = [10, 100, 1000, 10000]
    tamanhos_teste = [t for t in todos_tamanhos if t <= tamanho_selecionado]
    
    algoritmos = [
        ("Bubble Sort", a_bubble_sort.bubble_sort),
        ("Selection Sort", b_selection_sort.selection_sort),
        ("Insertion Sort", c_insertion_sort.insertion_sort),
        ("Shell Sort", f_shell_sort.shell_sort),
        ("Merge Sort", d_merge_sort.merge_sort),
        ("Quick Sort", e_quick_sort.quick_sort)
    ]
    
    dados_consolidados = []
    bar_progress = st.progress(0)
    total_steps = len(tamanhos_teste) * len(algoritmos)
    step = 0
    
    # Loop Principal: Testa cada tamanho para cada algoritmo
    for n in tamanhos_teste:
        lista_base = gerar_lista(n, tipo_lista)
        for nome, funcao in algoritmos:
            step += 1
            bar_progress.progress(step / total_steps)
            
            # Passa uma cópia da lista para não ordenar a original antes do próximo algoritmo
            tempo, comp, trocas, recursao = executar_algoritmo(nome, funcao, lista_base.copy())
            
            if tempo is not None:
                dados_consolidados.append({
                    "Tamanho": n, "Algoritmo": nome, "Tempo (s)": tempo,
                    "Comparações": comp, "Trocas": trocas, "Recursões": recursao
                })
            else:
                 dados_consolidados.append({
                    "Tamanho": n, "Algoritmo": nome, "Tempo (s)": None, 
                    "Comparações": 0, "Trocas": 0, "Recursões": 0
                })

    bar_progress.empty()
    
    # Salva resultados na sessão para persistência visual
    st.session_state['resultados'] = pd.DataFrame(dados_consolidados)
    st.session_state['tamanho_max'] = tamanho_selecionado
    st.session_state['tamanhos_teste'] = tamanhos_teste

# --- VISUALIZAÇÃO DOS RESULTADOS ---
if 'resultados' in st.session_state:
    df = st.session_state['resultados']
    tamanhos_teste = st.session_state['tamanhos_teste']
    
    # 1. Gráfico de Evolução
    st.markdown("---")
    st.header("1. Gráfico de Evolução do Desempenho")
    col_grafico, col_filtros = st.columns([3, 1])
    algoritmos_selecionados = []
    
    # Painel de Filtros do Gráfico
    with col_filtros:
        st.subheader("🎨 Legenda & Filtro")
        for nome_algo, props in CONFIG_CORES.items():
            if st.checkbox(f"{props['icone']} {nome_algo}", value=True):
                algoritmos_selecionados.append(nome_algo)
    
    # Plotagem do Gráfico
    with col_grafico:
        if len(tamanhos_teste) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            df_tempo = df.pivot(index="Tamanho", columns="Algoritmo", values="Tempo (s)")
            marcadores = ['o', 'v', '^', 's', 'p', '*']
            algoritmos_plotados = 0
            
            for i, nome_algo in enumerate(df_tempo.columns):
                if nome_algo in algoritmos_selecionados:
                    cor_linha = CONFIG_CORES[nome_algo]["cor"]
                    ax.plot(df_tempo.index, df_tempo[nome_algo], marker=marcadores[i % len(marcadores)], label=nome_algo, color=cor_linha, linewidth=2)
                    algoritmos_plotados += 1
            
            ax.set_xlabel("Tamanho da Lista (N)")
            ax.set_ylabel("Tempo (s)")
            ax.set_xticks(tamanhos_teste)
            
            if algoritmos_plotados > 0:
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.6)
                st.pyplot(fig)
            else:
                st.warning("Selecione pelo menos um algoritmo na caixa ao lado.")
        else:
            st.info("Gráfico indisponível para N=10 (necessário ao menos 2 pontos).")

    # 2. Tabela de Tempos
    st.markdown("---")
    st.subheader("2. Tabela de Tempo")
    df_tempo_tab = df.pivot(index="Tamanho", columns="Algoritmo", values="Tempo (s)")
    st.dataframe(df_tempo_tab.style.format("{:.6f}"), use_container_width=True)

    # 3. Métricas Detalhadas
    st.markdown("---")
    st.subheader(f"3. Comparações & Trocas (N = {st.session_state['tamanho_max']})")
    df_final = df[df["Tamanho"] == st.session_state['tamanho_max']].copy()
    st.dataframe(df_final[["Algoritmo", "Comparações", "Trocas"]].style.format({"Comparações": "{:,.0f}", "Trocas": "{:,.0f}"}), use_container_width=True, hide_index=True)

    # 4. Recursões
    st.markdown("---")
    st.subheader("4. Recursões")
    df_rec = df_final[df_final["Recursões"] > 0][["Algoritmo", "Recursões"]]
    if not df_rec.empty:
        st.dataframe(df_rec.style.format({"Recursões": "{:,.0f}"}), use_container_width=True, hide_index=True)
    else:
        st.info("Sem recursões.")

    # 5. Resumo Teórico das Complexidades
    st.markdown("---")
    st.header("5. Resumo Teórico")
    data_complexidade = {
        "Algoritmo": ["Bubble Sort", "Selection Sort", "Insertion Sort", "Shell Sort", "Merge Sort", "Quick Sort"],
        "Melhor Caso": ["O(n)", "O(n²)", "O(n)", "O(n log n)", "O(n log n)", "O(n log n)"],
        "Caso Médio": ["O(n²)", "O(n²)", "O(n²)", "Depende do Gap", "O(n log n)", "O(n log n)"],
        "Pior Caso": ["O(n²)", "O(n²)", "O(n²)", "O(n²)", "O(n log n)", "O(n²)"],
    }
    st.table(pd.DataFrame(data_complexidade))

    # 6. Resumo Prático
    st.markdown("---")
    st.header("6. Resumo Prático")
    df_resumo_pratico = df_final[["Algoritmo", "Tempo (s)", "Comparações", "Trocas", "Recursões"]].copy()
    df_resumo_pratico = df_resumo_pratico.sort_values(by="Tempo (s)").reset_index(drop=True)

    st.table(df_resumo_pratico.style.format({
        "Tempo (s)": "{:.6f}",
        "Comparações": "{:,.0f}",
        "Trocas": "{:,.0f}",
        "Recursões": "{:,.0f}"
    }))