import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Rutas Chapultepec - Optimización", layout="wide")
st.title("🌲 Optimización de Rutas en el Bosque de Chapultepec")
st.markdown("**Proyecto de Análisis de Redes y Flujo**")

# --- DATOS DEL MODELO ---
@st.cache_data
def cargar_grafo():
    nodos = {
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
        G.add_edge(nodos[origen], nodos[destino], weight=peso)
    return G, nodos

G, dict_nodos = cargar_grafo()
nombres_nodos = list(G.nodes())

# --- SIDEBAR: CONTROLES ---
st.sidebar.header("🗺️ Navegación")
menu = st.sidebar.radio(
    "Selecciona una sección:",
    ("1. Visualización de la Red", "2. Ruta Más Corta (Dijkstra)", "3. Todas las Rutas (Floyd-Warshall)", "4. Análisis de Sensibilidad")
)

# --- 1. VISUALIZACIÓN ---
if menu == "1. Visualización de la Red":
    st.header("Topología de la Red")
    st.write("Representación gráfica de los 15 nodos y 34 arcos, con distancias obtenidas mediante Google Maps.")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Usamos un layout de resorte para que se organice automáticamente
    pos = nx.spring_layout(G, seed=42) 
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    
    # Etiquetas de los pesos
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7, ax=ax)
    
    st.pyplot(fig)

# --- 2. DIJKSTRA ---
elif menu == "2. Ruta Más Corta (Dijkstra)":
    st.header("📍 Calculadora de Ruta Óptima")
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox("Punto de Origen:", nombres_nodos, index=0)
    with col2:
        destino = st.selectbox("Punto de Destino:", nombres_nodos, index=8)
        
    if origen != destino:
        try:
            ruta = nx.shortest_path(G, source=origen, target=destino, weight='weight')
            costo = nx.shortest_path_length(G, source=origen, target=destino, weight='weight')
            
            st.success(f"**Costo total de la ruta:** {costo} metros")
            st.info("**Ruta a seguir:** " + " ➡️ ".join(ruta))
        except nx.NetworkXNoPath:
            st.error("No hay ruta disponible entre estos puntos.")
    else:
        st.warning("El origen y destino son el mismo punto.")

# --- 3. FLOYD-WARSHALL ---
elif menu == "3. Todas las Rutas (Floyd-Warshall)":
    st.header("📊 Matriz de Distancias Mínimas")
    st.write("Cálculo del costo mínimo entre todo par de nodos en la red.")
    
    # Calculamos y formateamos la matriz
    fw_dict = nx.floyd_warshall(G, weight='weight')
    df_fw = pd.DataFrame(fw_dict).sort_index(axis=0).sort_index(axis=1)
    
    st.dataframe(df_fw.style.background_gradient(cmap='viridis', axis=None))

# --- 4. SENSIBILIDAD ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Escenarios 'What-If'")
    st.markdown("""
    **Escenario 1: Bloqueo de Camino**
    ¿Qué sucede si se cierra el paso principal entre el Herpetario y el Jardín Botánico por obras?
    """)
    # Aquí puedes añadir el código interactivo para remover la arista G.remove_edge() y recalcular
    bloqueo = st.checkbox("Simular cierre del paso Herpetario - Jardín Botánico")
    if bloqueo:
        G_temp = G.copy()
        if G_temp.has_edge('Herpetario', 'Jardín Botánico'):
            G_temp.remove_edge('Herpetario', 'Jardín Botánico')
            st.error("Ruta bloqueada. El tráfico se ha desviado.")
            # Puedes poner un mini-Dijkstra aquí para demostrar el cambio