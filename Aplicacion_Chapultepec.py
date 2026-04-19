import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import time  # <-- Nueva librería nativa de Python necesaria para la animación

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
        G.add_edge(origen, destino, weight=peso)
    return G, nodos

G, dict_nodos = cargar_grafo()

# Diccionario maestro de colores para mantener consistencia
mapa_colores = {}
for nodo in G.nodes():
    if nodo in ['N1', 'N2', 'N11']:
        mapa_colores[nodo] = '#87CEFA' # Agua
    elif nodo in ['N3', 'N4', 'N5', 'N6', 'N15']:
        mapa_colores[nodo] = '#FFB347' # Fauna
    elif nodo in ['N7', 'N8', 'N10']:
        mapa_colores[nodo] = '#98FB98' # Flora
    else:
        mapa_colores[nodo] = '#DDA0DD' # Cultura

posiciones_fijas = {
    'N1': (0, 10), 'N2': (3, 15), 'N3': (5, 20), 'N4': (6, 10),
    'N5': (10, 18), 'N6': (14, 20), 'N7': (19, 14), 'N8': (18, 8),
    'N9': (15, 0), 'N10': (11, 6), 'N11': (8, 2), 'N12': (5, 5),
    'N13': (2, 0), 'N14': (0, -6), 'N15': (6, -8)
}

# --- SIDEBAR: CONTROLES ---
st.sidebar.header("🗺️ Navegación")
menu = st.sidebar.radio(
    "Selecciona una sección:",
    ("1. Visualización de la Red", "2. Ruta Más Corta (Dijkstra)", "3. Todas las Rutas (Floyd-Warshall)", "4. Análisis de Sensibilidad", "5. Animación de Construcción")
)

# --- 1. VISUALIZACIÓN ESTÁTICA Y CODIFICADA ---
if menu == "1. Visualización de la Red":
    st.header("Topología de la Red (Nodos Codificados)")
    st.write("El mapa utiliza identificadores ($N_1, N_2...$) para mantener la red matemáticamente limpia. Revisa la tabla lateral para conocer el significado geográfico de cada nodo.")
    
    col_mapa, col_leyenda = st.columns([3, 1])
    
    with col_mapa:
        colores_lista = [mapa_colores[n] for n in G.nodes()]
        fig, ax = plt.subplots(figsize=(14, 10))
        
        nx.draw_networkx_nodes(G, posiciones_fijas, node_color=colores_lista, node_size=1000, edgecolors='black', linewidths=1.5, ax=ax)
        nx.draw_networkx_edges(G, posiciones_fijas, edge_color='gray', width=1.5, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(G, posiciones_fijas, font_size=11, font_weight='bold', font_color='black', ax=ax)
        
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, posiciones_fijas, edge_labels=labels, font_size=9, font_color='red', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.5), ax=ax)
        
        legend_handles = [
            mpatches.Patch(color='#87CEFA', label='Cuerpos de Agua'),
            mpatches.Patch(color='#FFB347', label='Zonas de Fauna'),
            mpatches.Patch(color='#98FB98', label='Zonas de Flora'),
            mpatches.Patch(color='#DDA0DD', label='Monumentos / Cultura')
        ]
        ax.legend(handles=legend_handles, loc='upper left', fontsize=10, frameon=True, shadow=True)
        ax.margins(0.1)
        plt.axis('off')
        st.pyplot(fig)
        
    with col_leyenda:
        st.subheader("📋 Nomenclatura")
        st.markdown("---")
        df_nomenclatura = pd.DataFrame(list(dict_nodos.items()), columns=["ID", "Ubicación"])
        st.dataframe(df_nomenclatura, hide_index=True, use_container_width=True)

# --- 2. DIJKSTRA ---
elif menu == "2. Ruta Más Corta (Dijkstra)":
    st.header("📍 Calculadora de Ruta Óptima")
    st.write("Aplicación del **algoritmo de Dijkstra** para encontrar la ruta de costo mínimo.")
    
    opciones_nodos = [f"{k} - {v}" for k, v in dict_nodos.items()]
    
    col1, col2 = st.columns(2)
    with col1:
        seleccion_origen = st.selectbox("Punto de Origen:", opciones_nodos, index=0)
    with col2:
        seleccion_destino = st.selectbox("Punto de Destino:", opciones_nodos, index=8)
        
    origen = seleccion_origen.split(" - ")[0]
    destino = seleccion_destino.split(" - ")[0]
        
    if origen != destino:
        try:
            ruta_ids = nx.shortest_path(G, source=origen, target=destino, weight='weight')
            costo = nx.shortest_path_length(G, source=origen, target=destino, weight='weight')
            
            ruta_texto = [f"**{nodo}** ({dict_nodos[nodo]})" for nodo in ruta_ids]
            
            st.success(f"**Costo total de la ruta:** {costo} metros")
            st.info(" ➡️ ".join(ruta_texto))
        except nx.NetworkXNoPath:
            st.error("No hay ruta disponible entre estos puntos.")
    else:
        st.warning("El origen y el destino son el mismo punto.")

# --- 3. FLOYD-WARSHALL ---
elif menu == "3. Todas las Rutas (Floyd-Warshall)":
    st.header("📊 Matriz de Distancias Mínimas")
    st.write("Matriz generada por el **algoritmo de Floyd-Warshall** con el costo mínimo entre cualquier par de nodos ($N_i, N_j$).")
    
    fw_dict = nx.floyd_warshall(G, weight='weight')
    df_fw = pd.DataFrame(fw_dict).sort_index(axis=0).sort_index(axis=1)
    
    nodos_ordenados = sorted(G.nodes(), key=lambda x: int(x[1:]))
    df_fw = df_fw.reindex(index=nodos_ordenados, columns=nodos_ordenados)
    
    st.dataframe(df_fw.style.background_gradient(cmap='viridis', axis=None), height=600)

# --- 4. SENSIBILIDAD ---
elif menu == "4. Análisis de Sensibilidad":
    st.header("⚠️ Escenarios 'What-If'")
    st.write("Análisis de perturbación en la red: Cambio de la ruta óptima por bloqueo de arcos.")
    
    st.subheader("Escenario 1: Camino Bloqueado (N6 - N7)")
    st.write("Simulemos que el paso directo entre **N6 (Herpetario)** y **N7 (Jardín Botánico)** está en mantenimiento profundo.")
    
    bloqueo = st.checkbox("🚧 Cerrar arco N6 - N7")
    
    G_temp = G.copy()
    if bloqueo:
        if G_temp.has_edge('N6', 'N7'):
            G_temp.remove_edge('N6', 'N7')
            st.error("Arco (N6, N7) eliminado de la red. El flujo se ha desviado.")
    else:
        st.success("La red opera con todos sus arcos disponibles.")
        
    st.write("**Impacto en la ruta: N6 (Herpetario) ➡️ N9 (Castillo)**")
    try:
        ruta_sens = nx.shortest_path(G_temp, source='N6', target='N9', weight='weight')
        costo_sens = nx.shortest_path_length(G_temp, source='N6', target='N9', weight='weight')
        
        ruta_texto_sens = [f"{nodo}" for nodo in ruta_sens]
        
        st.metric(label="Costo de Distancia Total", value=f"{costo_sens} m", delta=f"+{costo_sens - 420} m por desvío" if bloqueo and costo_sens > 420 else "0 m")
        st.info("**Nueva Ruta Óptima:** " + " ➡️ ".join(ruta_texto_sens))
    except nx.NetworkXNoPath:
        st.error("Ruta incomunicada.")

# --- 5. ANIMACIÓN DE CONSTRUCCIÓN ---
elif menu == "5. Animación de Construcción":
    st.header("🎬 Construcción Paso a Paso de la Red")
    st.write("Visualiza cómo se levanta la red de Chapultepec nodo por nodo.")
    
    if st.button("▶️ Iniciar Animación"):
        # Contenedor vacío donde se irán pintando los cuadros
        plot_placeholder = st.empty()
        
        # Ordenamos los nodos del N1 al N15 para la animación
        nodos_ordenados = sorted(G.nodes(), key=lambda x: int(x[1:]))
        
        for i in range(1, len(nodos_ordenados) + 1):
            nodos_actuales = nodos_ordenados[:i]
            # Creamos un subgrafo solo con los nodos que han "aparecido" hasta el momento
            G_sub = G.subgraph(nodos_actuales)
            
            fig, ax = plt.subplots(figsize=(14, 10))
            
            # Obtener colores solo de los nodos actuales
            colores_sub = [mapa_colores[n] for n in G_sub.nodes()]
            
            # Dibujar el subgrafo
            nx.draw_networkx_nodes(G_sub, posiciones_fijas, node_color=colores_sub, node_size=1000, edgecolors='black', linewidths=1.5, ax=ax)
            nx.draw_networkx_edges(G_sub, posiciones_fijas, edge_color='gray', width=1.5, alpha=0.5, ax=ax)
            nx.draw_networkx_labels(G_sub, posiciones_fijas, font_size=11, font_weight='bold', font_color='black', ax=ax)
            
            labels = nx.get_edge_attributes(G_sub, 'weight')
            nx.draw_networkx_edge_labels(G_sub, posiciones_fijas, edge_labels=labels, font_size=9, font_color='red', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.5), ax=ax)
            
            # Fijamos los límites del eje X y Y para que el mapa no esté "brincando" de tamaño
            ax.set_xlim(-2, 21)
            ax.set_ylim(-10, 22)
            ax.margins(0.1)
            plt.axis('off')
            
            # Actualizamos el contenedor con la nueva imagen
            plot_placeholder.pyplot(fig)
            plt.close(fig) # Liberar memoria
            
            # Pausa de medio segundo antes de que aparezca el siguiente nodo
            time.sleep(0.5)
            
        st.success("¡Red completada!")
