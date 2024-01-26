import streamlit as st
import viga
import matplotlib.pyplot as plt

# Interfaz del sidebar
with st.sidebar:
    
    st.title("Propiedades Geométricas")
    b = st.number_input("Base (cm)", value=30.0, placeholder="Base de Viga")
    h = st.number_input("Altura (cm)", value=50.0, placeholder="Altura de Viga")
    r = st.number_input("Recubrimiento (cm)", value=6.0, placeholder="Recubrimiento de Viga")
    
    st.title("Propiedades de los materiales")
    
    fc = st.number_input("$f'c \ (kg/cm^2)$", value=210.0, placeholder="Resistencia a compresión del concreto")
    fy = st.number_input("$f_y \ (kg/cm^2)$", value=4200.0, placeholder="Esfuerzo de fluencia del acero")
    Es = st.number_input("$E_s \ (kg/cm^2)$", value=2000000.0, placeholder="Módulo de elasticidad del acero")
    ecu = st.number_input("$\\varepsilon_{c \mu}$", value=0.003, placeholder="Deformación unitaria máxima del concreto comprimido",step=0.001,format="%.3f")
    phiFlexion = st.number_input("$\\phi_{flexión}$", value=0.9, placeholder="Factor de reducción de resistencia")

# Interfaz de la página principal

st.markdown("# Beam Design | Cálculo a Flexión")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,0.7,1,2,0.7,1,2])

numero1 = col1.number_input("", value=1,key="numero1")
diametro1= col2.selectbox("", viga.tablaAceros["Diametro"], index=8, key="diametro1")
col3.markdown("# \+")

numero2 = col4.number_input("", value=1,key="numero2")
diametro2= col5.selectbox("", viga.tablaAceros["Diametro"], key="diametro2")
col6.markdown("# \+")

numero3 = col7.number_input("", value=1,key="numero3")
diametro3= col8.selectbox("", viga.tablaAceros["Diametro"], key="diametro3")

st.divider()

# Cálculo del área de acero
As = viga.areaAs(numero1,diametro1) + viga.areaAs(numero2,diametro2) + viga.areaAs(numero3,diametro3)
As = round(As,2)

# Cálculos de la viga
calculoViga = viga.calculoFlexion(
                        b=b,
                        h=h,
                        fc=fc,
                        fy=fy,
                        Es=Es,
                        Ecu=ecu,
                        phiFlexion=phiFlexion,
                        acero=As,
                        r =r
)

def graficoSeccion(
    b,
    h,
    r,
):
    # Definir las coordenadas de la sección transversal
    seccion_x = [0, b, b, 0, 0]
    seccion_y = [0, 0, h, h, 0]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(b/10,h/10))
    ax.plot(seccion_x, seccion_y, color='black', linewidth=2, label='Sección')
    ax.fill_between([0,b], h-calculoViga["c_value"], h, color='gray')
    ax.fill_between([6,b-6], r, r+3, color='black')
    ax.text(b/2, r+4, f'$A_s={As} cm^2$', ha='center', va='bottom', color='red')

    # Mostrar el gráfico
    #ax.grid(False)
    
    # Retornar la figura
    return fig



col1, col2 = st.columns(2)

with col1:
    st.pyplot(graficoSeccion(b,h,r))

with col2:
    st.markdown("$As_{min}$"+" = "+f"${calculoViga['aceroMinimo']}$")
    st.markdown("$As_{bal}$"+" = "+f"${calculoViga['aceroBalanceado']}$")
    st.markdown("$As_{max}$"+" = "+f"${calculoViga['aceroMaximo']}$")
    st.markdown(f"$a={calculoViga['a']}$")
    st.markdown(f"$c={calculoViga['c']}$")    
    st.markdown(f"$øM_n={calculoViga['phiMn']}$")
    st.markdown(f"Tipo de falla: {calculoViga['tipoFalla']}")
    st.markdown(f"$\\varepsilon_s={calculoViga['defAs']}$")

