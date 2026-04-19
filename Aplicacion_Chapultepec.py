import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Rutas Chapultepec - Optimización", layout="wide")
st.title("🌲 Optimización de Rutas en el Bosque de Chapultepec")
st.markdown("**Proyecto de Análisis de Redes y Flujo | Enfrentamiento con Rey Boo**")

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

# --- 1. VISUALIZACIÓN ESTÁTICA Y ORDENADA ---
if menu == "1. Visualización de la Red":
    st.header("Topología de la Red (Vista Estructurada)")
    st.write("Mapa estático con coordenadas fijadas manualmente para asegurar la legibilidad de los nodos y los costos de cada ruta.")
    
    # Coordenadas fijas (x, y) aproximando el boceto original
    posiciones_fijas = {
        'Lago': (0, 5),
        'Casa del Lago': (2, 6),
        'Zoo Aventuras': (4, 7),
        'Zoológico': (6, 6),
        'Museo Axolote': (8, 7),
        'Herpetario': (10, 8),
        'Jardín Botánico': (12, 7),
        'Orquideario': (11, 4),
        'Castillo': (9, 3),
        'Ahuehuete': (7, 2),
        'Semi Lago': (5, 1),
        'F. Quijote': (3, 1),
        'Sor Juana': (2, 3),
        'F. Ranas': (1, 0),
        'Aviario': (0, -2)
    }
    
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Dibujar los Nodos
    nx.draw_networkx_nodes(G, posiciones_fijas, 
                           node_color='#a8d5ba', 
                           node_size=800, 
                           edgecolors='black', 
                           ax=ax)
    
    # Dibujar las Aristas (líneas)
    nx.draw_networkx_edges(G, posiciones_fijas, 
                           edge_color='gray', 
                           width=1.5, 
                           ax=ax)
    
    # Textos de los Nodos (Nombres)
    nx.draw_networkx_labels(G, posiciones_fijas, 
                            font_size=9, 
                            font_weight='bold', 
                            ax=ax)
    
    # Textos de los Costos (Distancias)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, posiciones_fijas, 
                                 edge_labels=labels, 
                                 font_size=8, 
                                 font_color='red', 
                                 ax=ax)
    
    # Quitar bordes del gráfico para que se vea limpio
    ax.margins(0.15)
    plt.axis('off')
    
    st.pyplot(fig)

# --- 2. DIJKSTRA ---
elif menu == "2. Ruta Más Corta (Dijkstra)":
    st.header("📍 Calculadora de Ruta Óptima")
    st.write("Aplicación del **algoritmo de Dijkstra** para encontrar la ruta más corta entre dos puntos específicos del parque.")
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
        st.warning("El origen y el destino son el mismo punto.")

# --- 3. FLOYD-WARSHALL ---
elif menu == "3. Todas las Rutas (Floyd-Warshall)":
    st.header("📊 Matriz de Distancias Mínimas")
    st.write("Cálculo del costo mínimo entre *todo par de nodos* en la red usando el **algoritmo de Floyd-Warshall**.")
    
    fw_dict = nx.floyd_warshall(G, weight='weight')
    df_fw = pd.DataFrame(fw_dict).sort_index(axis=0).sort_index(axis=1)
    
    st.dataframe(df_fw.style.background_gradient(cmap='viridis', axis=None))

# --- 4. SENSIBILIDAD ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Escenarios 'What-If'")
    st.write("¿Qué pasa si cambian las condiciones físicas de la red?")
    
    st.subheader("Escenario 1: Camino Bloqueado")
    st.write("Simulemos que el camino directo entre el **Herpetario** y el **Jardín Botánico** (que normalmente cuesta 670m) está cerrado por mantenimiento profundo.")
    
    bloqueo = st.checkbox("🚧 Cerrar paso Herpetario - Jardín Botánico")
    
    G_temp = G.copy()
    if bloqueo:
        if G_temp.has_edge('Herpetario', 'Jardín Botánico'):
            G_temp.remove_edge('Herpetario', 'Jardín Botánico')
            st.error("El camino ha sido bloqueado. El algoritmo recalculará las rutas desviando el tráfico.")
    else:
        st.success("El camino opera con normalidad.")
        
    st.write("**Impacto en la ruta: Herpetario ➡️ Castillo**")
    try:
        ruta_sens = nx.shortest_path(G_temp, source='Herpetario', target='Castillo', weight='weight')
        costo_sens = nx.shortest_path_length(G_temp, source='Herpetario', target='Castillo', weight='weight')
        
        st.metric(label="Distancia Total", value=f"{costo_sens} m", delta=f"+{costo_sens - 420} m de desvío" if bloqueo and costo_sens > 420 else "0 m")
        st.info("**Ruta Actualizada:** " + " ➡️ ".join(ruta_sens))
    except nx.NetworkXNoPath:
        st.error("Ruta incomunicada.")
