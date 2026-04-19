import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Optimización Chapultepec - UNAM", layout="wide")
st.title("🌲 Optimización de Rutas: Bosque de Chapultepec")
st.markdown("**Proyecto de Análisis de Redes | Enfrentamiento con Rey Boo**")

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
    ("1. Animación de la Red", "2. Ruta Más Corta (Dijkstra)", "3. Matriz de Rutas (Floyd-Warshall)", "4. Análisis de Sensibilidad")
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
    opciones = [f"{k} - {v}" for k, v in dict_nodos.items()]
    c1, c2 = st.columns(2)
    with c1: or_sel = st.selectbox("Origen:", opciones, index=0)
    with c2: des_sel = st.selectbox("Destino:", opciones, index=8)
    
    u, v = or_sel.split(" - ")[0], des_sel.split(" - ")[0]
    if u != v:
        try:
            ruta = nx.shortest_path(G, source=u, target=v, weight='weight')
            costo = nx.shortest_path_length(G, source=u, target=v, weight='weight')
            st.success(f"Costo mínimo: {costo} metros")
            st.write("➡️ ".join([f"**{n}**" for n in ruta]))
        except nx.NetworkXNoPath:
            st.error("No hay ruta disponible entre estos puntos.")
    else:
        st.warning("El origen y el destino son el mismo punto.")

# --- 3. FLOYD-WARSHALL (PASO A PASO) ---
elif menu == "3. Matriz de Rutas (Floyd-Warshall)":
    st.header("📊 Algoritmo Floyd-Warshall (Iteraciones $k$)")
    st.write("Exploración profunda usando **Programación Dinámica**. Observa cómo se actualizan las matrices de Costos ($D$) y de Predecesores/Rutas ($P$) al evaluar cada nodo intermedio $k$.")
    
    nodos_lista = sorted(G.nodes(), key=lambda x: int(x[1:]))
    n = len(nodos_lista)
    
    idx_to_nodo = {i: nodo for i, nodo in enumerate(nodos_lista)}
    nodo_to_idx = {nodo: i for i, nodo in enumerate(nodos_lista)}
    
    # Inicialización
    D = np.full((n, n), np.inf)
    P = np.full((n, n), "", dtype=object)
    
    for i in range(n):
        D[i][i] = 0
        P[i][i] = "-"
        
    for u, v, data in G.edges(data=True):
        i, j = nodo_to_idx[u], nodo_to_idx[v]
        peso = data['weight']
        D[i][j] = peso
        D[j][i] = peso
        P[i][j] = v
        P[j][i] = u
        
    historial_D = [D.copy()]
    historial_P = [P.copy()]
    
    # Bucle Principal O(V^3)
    for k in range(n):
        D_k = historial_D[-1].copy()
        P_k = historial_P[-1].copy()
        for i in range(n):
            for j in range(n):
                if D_k[i][k] + D_k[k][j] < D_k[i][j]:
                    D_k[i][j] = D_k[i][k] + D_k[k][j]
                    P_k[i][j] = P_k[i][k]
        historial_D.append(D_k)
        historial_P.append(P_k)
        
    # Interfaz
    k_seleccionado = st.slider("Selecciona la iteración $k$ (Nodo intermedio evaluado):", min_value=0, max_value=n, value=0)
    
    if k_seleccionado == 0:
        st.info("💡 **Iteración $k=0$:** Matriz inicial basada únicamente en las adyacencias directas. Las celdas con `inf` indican que no hay un arco directo.")
    else:
        nodo_k = idx_to_nodo[k_seleccionado - 1]
        st.info(f"💡 **Iteración $k={k_seleccionado}$:** Evaluando si pasar por el nodo intermedio **{nodo_k} ({dict_nodos[nodo_k]})** hace que alguna ruta sea más corta.")
    
    col_D, col_P = st.columns(2)
    
    with col_D:
        st.subheader(f"Matriz de Costos $D^{{({k_seleccionado})}}$")
        df_D = pd.DataFrame(historial_D[k_seleccionado], index=nodos_lista, columns=nodos_lista)
        st.dataframe(df_D.replace(np.inf, 'inf').style.highlight_null(color='lightgray'), use_container_width=True)
        
    with col_P:
        st.subheader(f"Matriz de Rutas $P^{{({k_seleccionado})}}$")
        df_P = pd.DataFrame(historial_P[k_seleccionado], index=nodos_lista, columns=nodos_lista)
        st.dataframe(df_P, use_container_width=True)

# --- 4. SENSIBILIDAD ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Análisis What-If")
    st.write("Bloqueo del arco crítico N6 - N7 (Paso Herpetario - Jardín Botánico).")
    bloqueo = st.checkbox("🚧 Aplicar Bloqueo")
    G_s = G.copy()
    if bloqueo:
        G_s.remove_edge('N6', 'N7')
        st.warning("Arco N6-N7 eliminado. El tráfico ha sido desviado.")
    else:
        st.success("La red opera con todos sus arcos disponibles.")
    
    try:
        r = nx.shortest_path(G_s, source='N6', target='N9', weight='weight')
        c = nx.shortest_path_length(G_s, source='N6', target='N9', weight='weight')
        st.metric("Nueva Distancia N6 -> N9", f"{c} m", delta=f"+{c-420} m por desvío" if bloqueo and c > 420 else "0 m")
        st.write("**Ruta Actualizada:** " + " ➡️ ".join(r))
    except nx.NetworkXNoPath:
        st.error("Ruta incomunicada.")
