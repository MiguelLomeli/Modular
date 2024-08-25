import streamlit as st

# Configuración de la aplicación
st.set_page_config(page_title="Explora el Mundo", page_icon="🌎", layout="centered")

# Sidebar para la navegación entre páginas
st.sidebar.title("Menu")
page = st.sidebar.radio("Ir a:", ["Bienvenida", "Preferencias de Viaje"])

# Página de Bienvenida
if page == "Bienvenida":
    st.title("¡Bienvenido a Explora el Mundo!")
    st.write("""
    Esta aplicación te ayudará a descubrir lugares increíbles de los paises que quieras visitar
    según tus gustos y preferencias.
    
    Navega a través del menú lateral para comenzar a personalizar tu experiencia de viaje.
    """)

# Página de Preferencias de Viaje
elif page == "Preferencias de Viaje":
    st.title("Dinos tus gustos para viajar por el mundo")

    st.subheader("¿A qué país te gustaría viajar?")
    paises = [
        "México", "Estados Unidos", "Canadá", "España", "Francia", "Italia", "Japón", "Australia", "Argentina",
        "Brasil", "China", "India", "Reino Unido", "Alemania", "Rusia", "Sudáfrica", "Egipto", "Turquía", "Nueva Zelanda",
        # Puedes agregar más países a la lista según necesites
    ]
    pais_seleccionado = st.selectbox("Selecciona un país:", paises)

    # Pregunta sobre tipos de destino
    st.subheader("¿Qué tipo de destinos prefieres?")
    destinos = st.multiselect(
        "Selecciona uno o varios:",
        ["Playas", "Montañas", "Pueblos Mágicos", "Ciudades Coloniales", "Selvas", "Desiertos", "Ruinas Arqueológicas"]
    )

    # Pregunta sobre actividades favoritas
    st.subheader("¿Cuáles son tus actividades favoritas?")
    actividades = st.multiselect(
        "Selecciona una o varias:",
        ["Senderismo", "Snorkel", "Explorar ciudades", "Visitar museos", "Gastronomía", "Compras", "Relajarse"]
    )

    # Pregunta sobre presupuesto
    st.subheader("¿Cuál es tu presupuesto aproximado para un viaje?")
    presupuesto = st.radio(
        "Selecciona una opción:",
        ["Bajo", "Medio", "Alto"]
    )

    # Mostrar los resultados seleccionados
    if st.button("Mostrar preferencias"):
        st.write("### Tus preferencias:")
        st.write("**Destinos preferidos:**", ", ".join(destinos))
        st.write("**Actividades favoritas:**", ", ".join(actividades))
        st.write(f"**Presupuesto:** {presupuesto}")