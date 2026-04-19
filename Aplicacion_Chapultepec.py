import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Optimización Chapultepec - UNAM", layout="wide")
st.title("🌲 Optimización de Rutas: Bosque de Chapultepec")
st.markdown("**Proyecto de Análisis de Redes | Emiliano Ruiz Sánchez**")

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

# --- 1. ANIMACIÓN DE LA RED (NUEVA PESTAÑA PRINCIPAL) ---
if menu == "1. Animación de la Red":
    st.header("Visualización Animada de la Red")
    st.write("Presiona el botón para observar la construcción secuencial de los nodos con efecto de desvanecimiento.")
    
    col_mapa, col_leyenda = st.columns([3, 1])
    
    with col_mapa:
        if st.button("▶️ Iniciar Animación de Red"):
            plot_placeholder = st.empty()
            nodos_ordenados = sorted(G.nodes(), key=lambda x: int(x[1:]))
            
            # Bucle por cada nodo para que aparezca uno por uno
            for i in range(1, len(nodos_ordenados) + 1):
                nodos_visibles = nodos_ordenados[:i]
                nodo_actual = nodos_ordenados[i-1]
                
                # Efecto de desvanecimiento (fade-in) para el nodo actual
                for alfa in [0.2, 0.4, 0.6, 0.8, 1.0]:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    # Dibujar nodos previos (opacidad completa)
                    nodos_previos = nodos_ordenados[:i-1]
                    if nodos_previos:
                        nx.draw_networkx_nodes(G, posiciones, nodelist=nodos_previos, 
                                               node_color=[mapa_colores[n] for n in nodos_previos],
                                               node_size=900, edgecolors='black', ax=ax)
                    
                    # Dibujar nodo actual con alfa variable
                    nx.draw_networkx_nodes(G, posiciones, nodelist=[nodo_actual], 
                                           node_color=[mapa_colores[nodo_actual]],
                                           node_size=900, edgecolors='black', alpha=alfa, ax=ax)
                    
                    # Dibujar aristas entre nodos visibles
                    G_sub = G.subgraph(nodos_visibles)
                    nx.draw_networkx_edges(G_sub, posiciones, edge_color='gray', width=1.2, alpha=alfa * 0.5, ax=ax)
                    nx.draw_networkx_labels(G_sub, posiciones, font_size=10, font_weight='bold', ax=ax)
                    
                    # Costos en rojo
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
        ruta = nx.shortest_path(G, source=u, target=v, weight='weight')
        costo = nx.shortest_path_length(G, source=u, target=v, weight='weight')
        st.success(f"Costo mínimo: {costo} metros")
        st.write("➡️ ".join([f"**{n}**" for n in ruta]))

# --- 3. FLOYD-WARSHALL ---
elif menu == "3. Matriz de Rutas (Floyd-Warshall)":
    st.header("📊 Matriz de Distancias Totales")
    fw = nx.floyd_warshall(G, weight='weight')
    df_fw = pd.DataFrame(fw).sort_index(axis=0).sort_index(axis=1)
    orden = sorted(G.nodes(), key=lambda x: int(x[1:]))
    st.dataframe(df_fw.reindex(index=orden, columns=orden).style.background_gradient(cmap='Greens'))

# --- 4. SENSIBILIDAD ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Análisis What-If")
    st.write("Bloqueo del arco crítico N6 - N7 (Paso Herpetario - Jardín Botánico).")
    bloqueo = st.checkbox("🚧 Aplicar Bloqueo")
    G_s = G.copy()
    if bloqueo:
        G_s.remove_edge('N6', 'N7')
        st.warning("Arco N6-N7 eliminado.")
    
    r = nx.shortest_path(G_s, source='N6', target='N9', weight='weight')
    c = nx.shortest_path_length(G_s, source='N6', target='N9', weight='weight')
    st.metric("Nueva Distancia N6 -> N9", f"{c} m", delta=f"{c-420} m" if bloqueo else "0 m")
    st.write("Ruta: " + " -> ".join(r))
