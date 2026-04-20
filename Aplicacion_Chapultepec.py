import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Optimización Chapultepec - MAC UNAM", layout="wide")
st.title("🌲 Optimización de Rutas: Bosque de Chapultepec")
st.markdown("**Proyecto de Análisis de Redes | Emiliano Ruiz Sánchez y Ricardo López Ramírez**")

# --- DATOS DEL MODELO ---
@st.cache_data
def cargar_grafo():
    nodos_info = {
        'N1': 'Lago', 'N2': 'Casa del Lago', 'N3': 'Zoo Aventuras',
        'N4': 'Zoológico', 'N5': 'Museo Axolote', 'N6': 'Herpetario',
        'N7': 'Jardín Botánico', 'N8': 'Orquideario', 'N9': 'Castillo',
        'N10': 'Ahuehuete', 'N11': 'Semi Lago', 'N12': 'F. Quijote',
        'N13': 'Sor Juana', 'N14': 'F. Ranas', 'N15': 'Aviario'
    }
    
    aristas = [
        ('N1', 'N2', 43), ('N2', 'N3', 91), ('N3', 'N4', 250), ('N4', 'N5', 51),
        ('N5', 'N6', 154), ('N6', 'N7', 670), ('N7', 'N8', 90), ('N8', 'N9', 270),
        ('N9', 'N10', 100), ('N10', 'N11', 190), ('N11', 'N12', 240), ('N12', 'N13', 200),
        ('N13', 'N14', 380), ('N14', 'N15', 300), ('N2', 'N4', 200), ('N3', 'N5', 120), 
        ('N4', 'N6', 180), ('N5', 'N7', 220), ('N6', 'N8', 150), ('N7', 'N9', 200), 
        ('N8', 'N10', 210), ('N9', 'N11', 170), ('N10', 'N12', 160), ('N11', 'N13', 140), 
        ('N12', 'N14', 180), ('N13', 'N15', 220), ('N1', 'N3', 130), ('N2', 'N5', 160), 
        ('N4', 'N7', 300), ('N6', 'N9', 250), ('N8', 'N11', 230), ('N10', 'N13', 210), 
        ('N11', 'N14', 190), ('N12', 'N15', 260)
    ]
    
    G = nx.Graph()
    for origen, destino, peso in aristas:
        G.add_edge(origen, destino, weight=peso)
    return G, nodos_info

G, dict_nodos = cargar_grafo()

# Colores y posiciones maestras
mapa_colores = {
    'N1': '#87CEFA', 'N2': '#87CEFA', 'N11': '#87CEFA', # Agua
    'N3': '#FFB347', 'N4': '#FFB347', 'N5': '#FFB347', 'N6': '#FFB347', 'N15': '#FFB347', # Fauna
    'N7': '#98FB98', 'N8': '#98FB98', 'N10': '#98FB98', # Flora
    'N9': '#DDA0DD', 'N12': '#DDA0DD', 'N13': '#DDA0DD', 'N14': '#DDA0DD' # Cultura
}

posiciones = {
    'N1': (0, 10), 'N2': (3, 15), 'N3': (5, 20), 'N4': (6, 10),
    'N5': (10, 18), 'N6': (14, 20), 'N7': (19, 14), 'N8': (18, 8),
    'N9': (15, 0), 'N10': (11, 6), 'N11': (8, 2), 'N12': (5, 5),
    'N13': (2, 0), 'N14': (0, -6), 'N15': (6, -8)
}

# --- SIDEBAR: NAVEGACIÓN ---
menu = st.sidebar.radio(
    "Menú de Proyecto:",
    ("1. Animación de la Red", "2. Ruta Más Corta (Dijkstra)", "3. Matriz de Rutas (Floyd-Warshall)", "4. Análisis de Sensibilidad", "5. Modelo de Programación Lineal")
)

# --- 1. ANIMACIÓN DE LA RED ---
if menu == "1. Animación de la Red":
    st.header("Visualización Animada de la Red")
    st.write("Presiona el botón para observar la construcción secuencial de los nodos con efecto de desvanecimiento.")
    
    col_mapa, col_leyenda = st.columns([3, 1])
    
    with col_mapa:
        if st.button("▶️ Iniciar Animación de Red"):
            plot_placeholder = st.empty()
            nodos_ordenados = sorted(G.nodes(), key=lambda x: int(x[1:]))
            
            for i in range(1, len(nodos_ordenados) + 1):
                nodos_visibles = nodos_ordenados[:i]
                nodo_actual = nodos_ordenados[i-1]
                
                for alfa in [0.2, 0.4, 0.6, 0.8, 1.0]:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    nodos_previos = nodos_ordenados[:i-1]
                    
                    if nodos_previos:
                        nx.draw_networkx_nodes(G, posiciones, nodelist=nodos_previos, 
                                               node_color=[mapa_colores[n] for n in nodos_previos],
                                               node_size=900, edgecolors='black', ax=ax)
                    
                    nx.draw_networkx_nodes(G, posiciones, nodelist=[nodo_actual], 
                                           node_color=[mapa_colores[nodo_actual]],
                                           node_size=900, edgecolors='black', alpha=alfa, ax=ax)
                    
                    G_sub = G.subgraph(nodos_visibles)
                    nx.draw_networkx_edges(G_sub, posiciones, edge_color='gray', width=1.2, alpha=alfa * 0.5, ax=ax)
                    nx.draw_networkx_labels(G_sub, posiciones, font_size=10, font_weight='bold', ax=ax)
                    
                    labels = nx.get_edge_attributes(G_sub, 'weight')
                    nx.draw_networkx_edge_labels(G_sub, posiciones, edge_labels=labels, font_size=8, 
                                                 font_color='red', bbox=dict(facecolor='white', alpha=alfa*0.7, edgecolor='none'), ax=ax)
                    
                    ax.set_xlim(-2, 21); ax.set_ylim(-10, 22)
                    plt.axis('off')
                    plot_placeholder.pyplot(fig)
                    plt.close(fig)
                    time.sleep(0.05)
            st.success("Red completada.")
        else:
            st.info("Haz clic en el botón superior para generar la red.")

    with col_leyenda:
        st.subheader("Significado")
        st.dataframe(pd.DataFrame(list(dict_nodos.items()), columns=["ID", "Lugar"]), hide_index=True)

# --- 2. DIJKSTRA ---
elif menu == "2. Ruta Más Corta (Dijkstra)":
    st.header("📍 Calculadora Dijkstra")
    st.write("Selecciona tu punto de partida y destino. El mapa resaltará visualmente el trayecto óptimo encontrado por el algoritmo.")
    
    opciones = [f"{k} - {v}" for k, v in dict_nodos.items()]
    c1, c2 = st.columns(2)
    with c1: or_sel = st.selectbox("Origen:", opciones, index=0)
    with c2: des_sel = st.selectbox("Destino:", opciones, index=8)
    
    u, v = or_sel.split(" - ")[0], des_sel.split(" - ")[0]
    
    if u != v:
        try:
            ruta = nx.shortest_path(G, source=u, target=v, weight='weight')
            costo = nx.shortest_path_length(G, source=u, target=v, weight='weight')
            
            st.success(f"**Costo mínimo total:** {costo} metros")
            st.write("**Secuencia de la ruta:** " + " ➡️ ".join([f"**{n}**" for n in ruta]))
            
            fig, ax = plt.subplots(figsize=(14, 9))
            
            nx.draw_networkx_nodes(G, posiciones, node_color='#E0E0E0', node_size=600, edgecolors='white', ax=ax)
            nx.draw_networkx_edges(G, posiciones, edge_color='#E0E0E0', width=1.0, ax=ax)
            nx.draw_networkx_labels(G, posiciones, font_size=9, font_color='gray', ax=ax)
            
            aristas_ruta = list(zip(ruta, ruta[1:]))
            colores_ruta = [mapa_colores[n] for n in ruta]
            
            nx.draw_networkx_nodes(G, posiciones, nodelist=ruta, node_color=colores_ruta, node_size=1000, edgecolors='black', linewidths=2, ax=ax)
            nx.draw_networkx_edges(G, posiciones, edgelist=aristas_ruta, edge_color='red', width=3.5, ax=ax)
            nx.draw_networkx_labels(G, posiciones, labels={n: n for n in ruta}, font_size=11, font_weight='bold', ax=ax)
            
            edge_labels = nx.get_edge_attributes(G, 'weight')
            path_edge_labels = { (origen, destino): edge_labels.get((origen, destino), edge_labels.get((destino, origen))) for origen, destino in aristas_ruta }
            nx.draw_networkx_edge_labels(G, posiciones, edge_labels=path_edge_labels, font_size=10, font_color='red', font_weight='bold', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'), ax=ax)
            
            ax.set_xlim(-2, 21); ax.set_ylim(-10, 22)
            plt.axis('off')
            st.pyplot(fig)
            
        except nx.NetworkXNoPath:
            st.error("No hay ruta disponible entre estos puntos.")
    else:
        st.warning("El origen y el destino son el mismo punto.")

# --- 3. FLOYD-WARSHALL ---
elif menu == "3. Matriz de Rutas (Floyd-Warshall)":
    st.header("📊 Algoritmo Floyd-Warshall (Paso a Paso)")
    st.write("Observa cómo la matriz de **Costos ($D$)** mantiene el color verde, mientras la matriz de **Rutas ($P$)** se ilumina con los colores geográficos.")
    
    nodos_lista = sorted(G.nodes(), key=lambda x: int(x[1:]))
    n = len(nodos_lista)
    
    idx_to_nodo = {i: nodo for i, nodo in enumerate(nodos_lista)}
    nodo_to_idx = {nodo: i for i, nodo in enumerate(nodos_lista)}
    
    D = np.full((n, n), np.inf)
    P = np.full((n, n), "", dtype=object)
    
    for i in range(n):
        D[i][i] = 0
        P[i][i] = "-"
        
    for u, v, data in G.edges(data=True):
        i, j = nodo_to_idx[u], nodo_to_idx[v]
        peso = data['weight']
        D[i][j] = peso; D[j][i] = peso
        P[i][j] = v; P[j][i] = u
        
    historial_D = [D.copy()]
    historial_P = [P.copy()]
    
    for k in range(n):
        D_k = historial_D[-1].copy()
        P_k = historial_P[-1].copy()
        for i in range(n):
            for j in range(n):
                if D_k[i][k] + D_k[k][j] < D_k[i][j]:
                    D_k[i][j] = D_k[i][k] + D_k[k][j]
                    P_k[i][j] = P_k[i][k]
        historial_D.append(D_k); historial_P.append(P_k)
        
    k_seleccionado = st.slider("Selecciona la iteración $k$ (Nodo intermedio evaluado):", min_value=0, max_value=n, value=0)
    
    if k_seleccionado == 0:
        st.info("💡 **Iteración $k=0$:** Matriz inicial de adyacencias directas.")
    else:
        nodo_k = idx_to_nodo[k_seleccionado - 1]
        st.info(f"💡 **Iteración $k={k_seleccionado}$:** Evaluando caminos pasando por **{nodo_k} ({dict_nodos[nodo_k]})**.")
        
        st.markdown("### 📝 Análisis de mejoras en esta iteración:")
        D_prev = historial_D[k_seleccionado - 1]
        D_curr = historial_D[k_seleccionado]
        cambios = False
        for i in range(n):
            for j in range(n):
                if D_curr[i][j] < D_prev[i][j]:
                    cambios = True
                    val_ant = "Infinito" if D_prev[i][j] == np.inf else int(D_prev[i][j])
                    st.markdown(f"- La ruta **{idx_to_nodo[i]} ➡️ {idx_to_nodo[j]}** bajó de `{val_ant}` a `{int(D_curr[i][j])}` m.")
        if not cambios: st.markdown("- *Pasar por este nodo no mejoró ninguna ruta existente.*")

    st.markdown("---")
    col_D, col_P = st.columns(2)
    with col_D:
        st.subheader(f"Matriz de Costos $D^{{({k_seleccionado})}}$")
        df_D_disp = pd.DataFrame(historial_D[k_seleccionado], index=nodos_lista, columns=nodos_lista).replace(np.inf, np.nan)
        st.dataframe(df_D_disp.style.format(na_rep='inf', precision=0).background_gradient(cmap='Greens', axis=None).highlight_null(color='lightgray'), use_container_width=True, height=500)
    with col_P:
        st.subheader(f"Matriz de Rutas $P^{{({k_seleccionado})}}$")
        df_P = pd.DataFrame(historial_P[k_seleccionado], index=nodos_lista, columns=nodos_lista)
        def color_rutas(val): return f'background-color: {mapa_colores[val]}; color: black' if val in mapa_colores else 'background-color: #f0f2f6; color: gray'
        try: styler_P = df_P.style.map(color_rutas)
        except AttributeError: styler_P = df_P.style.applymap(color_rutas)
        st.dataframe(styler_P, use_container_width=True, height=500)

# --- 4. SENSIBILIDAD (DOS CASOS GRÁFICOS) ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Análisis de Sensibilidad ('What-If')")
    st.write("Exploración de dos escenarios de alteración en la red y su impacto en las decisiones de enrutamiento, evaluados gráficamente.")
    
    escenario = st.radio("Selecciona el caso de estudio:", [
        "Caso 1: Bloqueo Total de Ruta (Cierre por mantenimiento)", 
        "Caso 2: Aumento de Costo (Congestión extrema en fin de semana)"
    ])
    
    if escenario == "Caso 1: Bloqueo Total de Ruta (Cierre por mantenimiento)":
        st.subheader("🚧 Caso 1: Cierre del tramo N6 - N7")
        st.write("**Situación:** El paso directo entre el **Herpetario (N6)** y el **Jardín Botánico (N7)** se cierra totalmente por obras.")
        
        bloqueo = st.checkbox("Aplicar Bloqueo (Eliminar arco N6-N7)")
        
        G_s = G.copy()
        if bloqueo:
            G_s.remove_edge('N6', 'N7')
            st.warning("Arco N6-N7 eliminado de la red. El algoritmo recalculará usando caminos alternativos.")
        else:
            st.info("Red en estado normal.")
            
        try:
            ruta = nx.shortest_path(G_s, source='N6', target='N9', weight='weight')
            costo = nx.shortest_path_length(G_s, source='N6', target='N9', weight='weight')
            
            col1, col2 = st.columns(2)
            col1.metric("Costo de la Ruta (N6 ➡️ N9)", f"{costo} m", delta=f"+{costo-420} m (Desvío)" if bloqueo else "0 m")
            col2.write("**Secuencia Óptima:**")
            col2.write(" ➡️ ".join([f"**{n}**" for n in ruta]))
            
            fig, ax = plt.subplots(figsize=(14, 9))
            nx.draw_networkx_nodes(G, posiciones, node_color='#E0E0E0', node_size=500, edgecolors='white', ax=ax)
            nx.draw_networkx_edges(G, posiciones, edge_color='#E0E0E0', width=1.0, ax=ax)
            
            aristas_ruta = list(zip(ruta, ruta[1:]))
            colores_ruta = [mapa_colores[n] for n in ruta]
            
            nx.draw_networkx_nodes(G, posiciones, nodelist=ruta, node_color=colores_ruta, node_size=800, edgecolors='black', linewidths=2, ax=ax)
            nx.draw_networkx_edges(G, posiciones, edgelist=aristas_ruta, edge_color='red', width=3.5, ax=ax)
            nx.draw_networkx_labels(G, posiciones, labels={n: n for n in ruta}, font_size=10, font_weight='bold', ax=ax)
            
            edge_labels = nx.get_edge_attributes(G, 'weight')
            path_edge_labels = { (u, v): edge_labels.get((u,v), edge_labels.get((v,u))) for u, v in aristas_ruta }
            nx.draw_networkx_edge_labels(G, posiciones, edge_labels=path_edge_labels, font_color='red', font_weight='bold', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.2'), ax=ax)
            
            if bloqueo and G.has_edge('N6', 'N7'):
                nx.draw_networkx_edges(G, posiciones, edgelist=[('N6', 'N7')], edge_color='red', width=2.0, style='dashed', ax=ax)
                x_mid, y_mid = (posiciones['N6'][0] + posiciones['N7'][0])/2, (posiciones['N6'][1] + posiciones['N7'][1])/2 + 0.8
                ax.text(x_mid, y_mid, "❌ CERRADO", color='red', fontsize=11, ha='center', va='center', backgroundcolor='white', fontweight='bold')
                
            ax.set_xlim(-2, 21); ax.set_ylim(-10, 22); plt.axis('off')
            st.pyplot(fig)
            
        except nx.NetworkXNoPath:
            st.error("Ruta incomunicada.")
            
    elif escenario == "Caso 2: Aumento de Costo (Congestión extrema en fin de semana)":
        st.subheader("🚶‍♂️ Caso 2: Congestión en el tramo N1 - N3")
        st.write("**Situación:** Es domingo y la ruta del **Lago (N1)** hacia el **Zoo Aventuras (N3)** está abarrotada de visitantes. Evaluaremos cómo este aumento de costo (de 130m a 450m) obliga al algoritmo a abandonar esa ruta y buscar una alternativa.")
        
        congestion = st.checkbox("Simular Congestión (Aumentar peso N1-N3 a 450)")
        
        G_s = G.copy()
        if congestion:
            G_s['N1']['N3']['weight'] = 450
            st.warning("El tramo N1-N3 ahora cuesta 450 metros equivalentes por el tráfico peatonal. Recalculando...")
        else:
            st.info("Tráfico fluido. El tramo N1-N3 cuesta sus 130 metros originales.")
            
        try:
            ruta = nx.shortest_path(G_s, source='N1', target='N5', weight='weight')
            costo = nx.shortest_path_length(G_s, source='N1', target='N5', weight='weight')
            
            col1, col2 = st.columns(2)
            col1.metric("Costo de la Ruta (N1 ➡️ N5)", f"{costo} m", delta=f"+{costo-250} m (Desvío inteligente)" if congestion else "0 m")
            col2.write("**Secuencia Óptima:**")
            col2.write(" ➡️ ".join([f"**{n}**" for n in ruta]))
            
            fig, ax = plt.subplots(figsize=(14, 9))
            nx.draw_networkx_nodes(G, posiciones, node_color='#E0E0E0', node_size=500, edgecolors='white', ax=ax)
            nx.draw_networkx_edges(G, posiciones, edge_color='#E0E0E0', width=1.0, ax=ax)
            
            if congestion:
                nx.draw_networkx_edges(G, posiciones, edgelist=[('N1', 'N3')], edge_color='darkorange', width=4.0, ax=ax)
                x_mid, y_mid = (posiciones['N1'][0] + posiciones['N3'][0])/2, (posiciones['N1'][1] + posiciones['N3'][1])/2 + 1.2
                ax.text(x_mid, y_mid, "⚠️ SATURADO (450m)", color='darkorange', fontsize=11, ha='center', va='center', backgroundcolor='white', fontweight='bold')
                
            aristas_ruta = list(zip(ruta, ruta[1:]))
            colores_ruta = [mapa_colores[n] for n in ruta]
            
            nx.draw_networkx_nodes(G, posiciones, nodelist=ruta, node_color=colores_ruta, node_size=800, edgecolors='black', linewidths=2, ax=ax)
            nx.draw_networkx_edges(G, posiciones, edgelist=aristas_ruta, edge_color='red', width=3.5, ax=ax)
            nx.draw_networkx_labels(G, posiciones, labels={n: n for n in ruta}, font_size=10, font_weight='bold', ax=ax)
            
            edge_labels = nx.get_edge_attributes(G_s, 'weight')
            path_edge_labels = { (u, v): edge_labels.get((u,v), edge_labels.get((v,u))) for u, v in aristas_ruta }
            nx.draw_networkx_edge_labels(G_s, posiciones, edge_labels=path_edge_labels, font_color='red', font_weight='bold', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.2'), ax=ax)
            
            ax.set_xlim(-2, 21); ax.set_ylim(-10, 22); plt.axis('off')
            st.pyplot(fig)
            
        except nx.NetworkXNoPath:
            st.error("Ruta incomunicada.")

# --- 5. MODELO DE PROGRAMACIÓN LINEAL ---
elif menu == "5. Modelo de Programación Lineal":
    st.header("📐 Modelo de Programación Lineal (MPL)")
    st.write("Planteamiento matemático para el problema de la **Ruta Más Corta** basado en las ecuaciones de Conservación de Flujo.")
    
    st.subheader("1. Variables de Decisión")
    st.markdown("""
    Sea $x_{ij} \in \{0, 1\}$ una variable binaria donde:
    * $x_{ij} = 1$ si el arco que va del nodo $i$ al nodo $j$ forma parte de la ruta óptima.
    * $x_{ij} = 0$ en caso contrario.
    """)
    
    st.subheader("2. Función Objetivo")
    st.markdown("Minimizar la distancia total caminada en la red de Chapultepec, multiplicando el costo en metros de cada arco por su respectiva variable de decisión:")
    st.latex(r"\min Z = 43x_{1,2} + 43x_{2,1} + 91x_{2,3} + 91x_{3,2} + \dots + 260x_{12,15} + 260x_{15,12}")
    
    st.subheader("3. Restricciones (Conservación de Flujo)")
    st.markdown("El modelo garantiza que la ruta sea continua desde el Origen (Oferta = 1) hasta el Destino (Demanda = 1), pasando por Nodos de Transbordo (Balance = 0). Ejemplo de ruta **N1 (Lago)** a **N9 (Castillo)**:")
    
    st.markdown("**A) Nodo Origen (N1 - Salida neta de 1):**")
    st.latex(r"(x_{1,2} + x_{1,3}) - (x_{2,1} + x_{3,1}) = 1")
    
    st.markdown("**B) Nodo Destino (N9 - Llegada neta de 1):**")
    st.latex(r"(x_{9,2} + x_{9,6} + x_{9,7} + x_{9,8} + x_{9,10} + x_{9,11}) - (x_{2,9} + x_{6,9} + x_{7,9} + x_{8,9} + x_{10,9} + x_{11,9}) = -1")
    
    st.markdown("**C) Nodos de Transbordo (Ejemplo N2 - Lo que entra es igual a lo que sale):**")
    st.latex(r"(x_{2,1} + x_{2,3} + x_{2,4} + x_{2,5}) - (x_{1,2} + x_{3,2} + x_{4,2} + x_{5,2}) = 0")
    st.caption("*Esta ecuación igualada a 0 se repite iterativamente para los 12 nodos de transbordo restantes.*")
    
    st.subheader("4. Naturaleza de las variables")
    st.latex(r"x_{ij} \in \{0, 1\} \quad \forall (i,j) \in A")
