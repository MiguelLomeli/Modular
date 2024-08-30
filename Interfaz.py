import streamlit as st
import pandas as pd
import maps_text_search as maps
from datetime import date

# Configuración de la aplicación
st.set_page_config(page_title="Explora el Mundo", page_icon="🌎", layout="centered", initial_sidebar_state="collapsed")

# Inicializar la variable de sesión para la página actual
if "page" not in st.session_state:
    st.session_state.page = "Bienvenida"

# Inicializar una variable en la sesión de Streamlit para almacenar el DataFrame
if "df_resultados" not in st.session_state:
    st.session_state.df_resultados = pd.DataFrame()

# Datos de ejemplo para países, estados y municipios
datos_geograficos = {
    "México": {
        "CDMX": ["Centro Histórico", "Coyoacán", "Polanco", "Roma", "Condesa"],
        "Jalisco": ["Guadalajara", "Puerto Vallarta", "Zapopan", "Tlaquepaque"],
        "Yucatán": ["Mérida", "Valladolid", "Progreso"],
        "Quintana Roo": ["Cancún", "Playa del Carmen", "Tulum", "Cozumel"],
    },
    "Estados Unidos": {
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
        "New York": ["New York City", "Buffalo", "Rochester", "Albany"],
        "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville"],
        "Texas": ["Houston", "Dallas", "Austin", "San Antonio"],
    },
    "España": {
        "Cataluña": ["Barcelona", "Girona", "Tarragona", "Lleida"],
        "Madrid": ["Madrid", "Alcalá de Henares", "Getafe", "Fuenlabrada"],
        "Andalucía": ["Sevilla", "Málaga", "Granada", "Córdoba"],
        "Comunidad Valenciana": ["Valencia", "Alicante", "Castellón de la Plana", "Elche"],
    },
    "Francia": {
        "Île-de-France": ["París", "Versalles", "Boulogne-Billancourt", "Saint-Denis"],
        "Provenza-Alpes-Costa Azul": ["Marsella", "Niza", "Cannes", "Aix-en-Provence"],
        "Nueva Aquitania": ["Burdeos", "Biarritz", "La Rochelle", "Limoges"],
        "Occitania": ["Toulouse", "Montpellier", "Carcasona", "Nimes"],
    },
    "Italia": {
        "Lombardía": ["Milán", "Bérgamo", "Brescia", "Como"],
        "Lacio": ["Roma", "Viterbo", "Latina", "Frosinone"],
        "Toscana": ["Florencia", "Pisa", "Siena", "Lucca"],
        "Véneto": ["Venecia", "Verona", "Padua", "Vicenza"],
    },
    "Argentina": {
        "Buenos Aires": ["Buenos Aires", "La Plata", "Mar del Plata", "Tigre"],
        "Córdoba": ["Córdoba", "Villa Carlos Paz", "Villa María", "Río Cuarto"],
        "Mendoza": ["Mendoza", "San Rafael", "Malargüe", "Luján de Cuyo"],
        "Santa Fe": ["Rosario", "Santa Fe", "Rafaela", "Venado Tuerto"],
    },
    "Brasil": {
        "Río de Janeiro": ["Río de Janeiro", "Niterói", "Petrópolis", "Angra dos Reis"],
        "São Paulo": ["São Paulo", "Campinas", "Santos", "Sorocaba"],
        "Bahía": ["Salvador", "Ilhéus", "Porto Seguro", "Feira de Santana"],
        "Minas Gerais": ["Belo Horizonte", "Ouro Preto", "Uberlândia", "Juiz de Fora"],
    },
    "Japón": {
        "Tokio": ["Tokio", "Shinjuku", "Shibuya", "Akihabara"],
        "Kioto": ["Kioto", "Fushimi", "Arashiyama", "Gion"],
        "Osaka": ["Osaka", "Namba", "Umeda", "Shin-Osaka"],
        "Hokkaido": ["Sapporo", "Hakodate", "Otaru", "Asahikawa"],
    },
    "Australia": {
        "Nueva Gales del Sur": ["Sídney", "Newcastle", "Wollongong", "Byron Bay"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat", "Bendigo"],
        "Queensland": ["Brisbane", "Gold Coast", "Cairns", "Townsville"],
        "Australia Occidental": ["Perth", "Fremantle", "Broome", "Albany"],
    },
}

# Función para mostrar el menú lateral
def show_sidebar():
    st.sidebar.title("Menú")
    pages = ["Bienvenida", "Preferencias de Viaje"]

     # Mostrar solo la opción de resultados si estamos en esa página
    if st.session_state.page == "Resultados de Búsqueda":
        pages.append("Resultados de Búsqueda")

    selected_page = st.sidebar.radio("Ir a:", pages, index=pages.index(st.session_state.page))
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        # No usar st.experimental_rerun() aquí para evitar problemas

show_sidebar()

# Página de Bienvenida
if st.session_state.page == "Bienvenida":
    st.title("¡Bienvenido a Explora el Mundo!")
    
    st.write("""
    Esta aplicación te ayudará a descubrir lugares increíbles de los países que quieras visitar
    según tus gustos y preferencias.
    
    Navega a través del menú lateral para comenzar a personalizar tu experiencia de viaje.
    """)

    if st.button("¡Comienza a Personalizar tu Viaje!"):
        st.session_state.page = "Preferencias de Viaje"
    
    st.write("""
    SmartTrip es una página web la cual te ayuda en tus viajes a crear un itinerario dependiendo del país
    que vayas a visitar y con base a tu gusto.
             
    No solo te dará un itinerario con las posibles actividades que puedes realizar a lo largo del día, 
    sino que también puedes personalizarlo a tu gusto en caso de que ya conozcas algún lugar o tengas 
    preferencias por algún otro.
    """)

    st.image("mapa.jpg", caption="Explora destinos increíbles", use_column_width=True)

# Página de Preferencias de Viaje
elif st.session_state.page == "Preferencias de Viaje":
    st.title("Ingrese tus preferencias para viajar")

    # Pregunta sobre país
    paises = ["Selecciona un país"] + list(datos_geograficos.keys())
    pais_seleccionado = st.selectbox("Selecciona un país:", paises)

    if pais_seleccionado != "Selecciona un país":
        # Mostrar selectbox de estados solo si se ha seleccionado un país
        estados = ["Selecciona un estado"] + list(datos_geograficos.get(pais_seleccionado, {}).keys())
        estado_seleccionado = st.selectbox("Selecciona un estado:", estados)

        if estado_seleccionado != "Selecciona un estado":
            # Mostrar selectbox de municipios solo si se ha seleccionado un estado
            municipios = ["Selecciona un municipio"] + datos_geograficos.get(pais_seleccionado, {}).get(estado_seleccionado, [])
            municipio_seleccionado = st.selectbox("Selecciona un municipio:", municipios)

    # Pregunta sobre tipos de destino
    focus_options = ["Selecciona una opción", "Naturaleza", "Cultura", "Historia", "Gastronomía", "Viaje económico"]
    focus = st.selectbox("¿Qué te gustaría ver?", focus_options)

    # Pregunta sobre fechas de viaje
    start_date = st.date_input("Fecha de inicio del viaje:", min_value=date.today())
    end_date = st.date_input("Fecha de fin del viaje:", min_value=start_date)

    # Mostrar el botón solo si todos los campos están seleccionados
    if (pais_seleccionado != "Selecciona un país" and
        estado_seleccionado != "Selecciona un estado" and
        municipio_seleccionado != "Selecciona un municipio" and
        focus != "Selecciona una opción" and
        start_date and end_date):
        if st.button("Buscar Atracciones"):
            # Establecer parámetros en la sesión y cambiar la página
            st.session_state.page = "Resultados de Búsqueda"
            # Almacenar los parámetros en la sesión de Streamlit
            st.session_state.pais = pais_seleccionado
            st.session_state.estado = estado_seleccionado
            st.session_state.municipio = municipio_seleccionado
            st.session_state.focus = focus
            st.session_state.start_date = start_date.isoformat()
            st.session_state.end_date = end_date.isoformat()

# Página de Resultados de Búsqueda
elif st.session_state.page == "Resultados de Búsqueda":
    pais = st.session_state.get("pais", "")
    estado = st.session_state.get("estado", "")
    municipio = st.session_state.get("municipio", "")
    focus = st.session_state.get("focus", "")
    start_date = st.session_state.get("start_date", "")
    end_date = st.session_state.get("end_date", "")

    if pais and estado and municipio and focus and start_date and end_date:
        st.title(f"Resultados de Búsqueda para {pais}, {estado}, {municipio}")

        # Mostrar los resultados de búsqueda
        focus_dict = {
            "Naturaleza": 1,
            "Cultura": 2,
            "Historia": 3,
            "Gastronomía": 4,
            "Viaje económico": 5
        }

        # Obtener las atracciones usando la función `get_atractions`
        maps.get_atractions(pais, estado, municipio, focus_dict[focus])

        # Leer los resultados desde el CSV generado
        st.session_state.df_resultados = pd.read_csv("places_results.csv")

        if not st.session_state.df_resultados.empty:
            st.write("### Resultados de Búsqueda:")

              # Mostrar los resultados en formato de tabla
            st.write("### Horarios y Detalles")

            # Crear una lista de horas
            horas = ["7:00 AM", "9:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM", "8:00 PM"]

            # Asegúrate de que la cantidad de horas es suficiente para el número de resultados
            num_hours = len(horas)
            num_results = len(st.session_state.df_resultados)

            

            # Mostrar la tabla
            for i, row in st.session_state.df_resultados.head(num_hours).iterrows():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(horas[i % num_hours])  # Mostrar las horas en la columna izquierda
                
                st.markdown('<hr>', unsafe_allow_html=True)

                with col2:
                    # Mejorar la visualización del nombre, dirección, reseñas y botones
                    nombre = row['displayName'].strip("'")
                    direccion = row['shortFormattedAddress']
                    calificacion = row.get('rating', 'N/A')
                    reseñas = row.get('reviews', 'N/A')
                    website_uri = row.get('websiteUri', '#')

                    # Mostrar nombre y dirección
                    st.markdown(f"**{nombre}**")
                    st.write(f"📍 {direccion}")

                    st.markdown(f"⭐ {calificacion}/5")
                
                    if st.button(f"Eliminar", key=f"eliminar_{i}"):
                        st.session_state.df_resultados.drop(i, inplace=True)
                        st.session_state.df_resultados.reset_index(drop=True, inplace=True)
                        # Actualizar el DataFrame en el archivo CSV
                        st.session_state.df_resultados.to_csv("places_results.csv", index=False)

                    # Botón para abrir el sitio web
                    website_uri = row.get('websiteUri', '')
                    if website_uri:
                        st.markdown(f"""
                        <a href="{website_uri}" target="_blank" class="button">Ver Sitio</a>
                        <style>
                        .button {{
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            font-weight: bold;
                            color: #fff;
                            background-color: #0E1117;
                            border: none;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                        .button:hover {{
                            background-color: #007bff;
                        }}
                        </style>
                        """, unsafe_allow_html=True)

            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(st.session_state.df_resultados)
            st.download_button(
                label="Descargar resultados",
                data=csv,
                file_name='resultados_de_busqueda.csv',
                mime='text/csv'
            )
            
            # Mostrar el DataFrame actualizado (opcional, solo si quieres ver la tabla en bruto)
            # st.dataframe(st.session_state.df_resultados)
    else:
        st.write("Por favor, utiliza el botón 'Buscar Atracciones' para ver los resultados.")