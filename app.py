import pandas as pd
import streamlit as st

"""
Pregunta 1 (0.5 puntos)

Crea una aplicación en Streamlit que cargue el archivo InventarioTechZone.xlsx.
Si el archivo no se encuentra, muestra un mensaje de error amigable y detén la ejecución
"""
try:
    df = pd.read_excel("data/InventarioTechZone.xlsx")
except:
    st.error("No se encontró el archivo InventarioTechZone.xlsx.")


"""
Pregunta 2 (0.5 punto)

Convierte la columna FechaIngreso al tipo datetime y muestra la tabla de inventario utilizando st.dataframe().
"""

df["FechaIngreso"] = pd.to_datetime(df["FechaIngreso"])
st.dataframe(df)

"""
Pregunta 3 (1 puntos)

Implementa un filtro por categoría del producto (Laptop, Monitor, Accesorio, Periférico, Componente).
Debe permitir seleccionar una o múltiples categorías.
"""

categorias = st.multiselect(
    "Selecciona las categorías de productos:",
    options=df["Categoria"].unique(),
    default=None,
)

"""
Pregunta 4 (1 punto)

Agrega un filtro por estado del producto:
- Disponible
- Agotado
- Descontinuado
- Crítico
"""

estado = st.selectbox(
    "Selecciona el estado del producto:",
    options=df["Estado"].unique(),
    index=0,
)

"""
Pregunta 5 (1 punto)

Crea un filtro por rango de precios usando un st.slider.
"""

precio_min, precio_max = st.slider(
    "Selecciona el rango de precios:",
    min_value=float(df["Precio"].min()),
    max_value=float(df["Precio"].max()),
    value=(float(df["Precio"].min()), float(df["Precio"].max())),
)


"""
Pregunta 6 (1 punto)

Incorpora un filtro para buscar por nombre o palabra clave dentro del producto.
"""

palabra_clave = st.text_input("Busca por nombre o palabra clave:")


"""
Pregunta 7 (1 punto)

Añade un filtro por stock mínimo, activado mediante un checkbox.
"""
stock_minimo = st.checkbox("Activar filtro por stock mínimo")
if stock_minimo:
    stock_min = st.number_input("Stock mínimo:", min_value=0, value=0)



"""
Pregunta 8 (1 punto)
Crea un formulario de registro de productos con los siguientes campos:
- Nombre del producto
- Categoría
- Precio unitario
- Stock disponible
- Fecha de ingreso
Valida que:
- El nombre no esté vacío
- El precio sea mayor que 0
- El stock sea mayor o igual a 0
- La fecha no sea futura
Reutiliza la función de generación de código único para guardar los datos.
"""

with st.form("registro_producto"):
    st.subheader("Registro de nuevo producto")
    nombre = st.text_input("Nombre del producto: ")
    categoria = st.selectbox(
        "Categoría:",
        options=["Laptop", "Monitor", "Accesorio", "Periférico", "Componente"],
    )
    precio = st.number_input("Precio unitario: ", min_value=0.01, value=0.01)
    stock = st.number_input("Stock disponible: ", min_value=0, value=0)
    fecha_ingreso = st.date_input("Fecha de ingreso: ")

    if st.form_submit_button("Registrar producto"):
        if not nombre:
            st.error("El nombre del producto no puede estar vacío.")
        elif precio <= 0:
            st.error("El precio debe ser mayor que 0.")
        elif stock < 0:
            st.error("El stock debe ser mayor o igual a 0.")
        elif fecha_ingreso > pd.Timestamp.now().date():
            st.error("La fecha de ingreso no puede ser futura.")
        else:
            st.success("Producto registrado exitosamente.")

"""
Pregunta 9 (1 punto)

Determina automáticamente el estado del producto según el stock:
- "Crítico" si el stock < 5
- "Agotado" si stock = 0
- "Disponible" si stock > 0
- "Descontinuado" solo si el usuario lo selecciona
"""

def determinar_estado(stock, descontinuado):
    if descontinuado:
        return "Descontinuado"
    if stock < 5:
        return "Crítico"
    elif stock == 0:
        return "Agotado"
    else:
        return "Disponible"
    
descontinuado = st.checkbox("Marcar como descontinuado")
df["Estado"] = df["Stock"].apply(determinar_estado, descontinuado=descontinuado)
st.write(df[["Producto", "Stock", "Estado"]])

"""
Pregunta 10 (1 punto)

- Calcula de manera dinámica el valor total del producto:
    ValorTotal = Precio × Stock
- Agrega esta columna a la tabla visual.
- Calcula el margen estimado de ganancia suponiendo un 12% del precio:
    MargenGanancia = Precio × 0.12
- Agrega una columna que calcule los días en inventario:
    DiasEnInventario = FechaActual − FechaIngreso
"""

df["ValorTotal"] = df["Precio"] * df["Stock"]
df["MargenGanancia"] = df["Precio"] * 0.12
df["DiasEnInventario"] = (pd.Timestamp.now() - df["FechaIngreso"]).dt.days
st.dataframe(df)

"""
Pregunta 11 (1 punto)
- Crea un gráfico de barras mostrando la cantidad de productos por categoría.
- Crea un gráfico circular mostrando el valor total por categoría.
- Modifica ambos gráficos para que se muestren uno al lado del otro en un mismo figure.
- Crea un gráfico adicional que muestre el TOP 5 de productos más valiosos, ordenados por ValorTotal.
"""

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
df.groupby("Categoria")["Producto"].count().plot(
    kind="bar", 
    ax=ax[0],
    color="skyblue"
)
ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)
ax[0].set_title("Cantidad de productos por categoría")

df.groupby("Categoria")["ValorTotal"].sum().plot(
    kind="pie", 
    ax=ax[1], 
    autopct="%1.1f%%"
)
ax[1].set_title("Valor total por categoría")
ax[1].set_ylabel("")
st.pyplot(fig)

top_productos = df.sort_values("ValorTotal", ascending=False).head(5)
st.subheader("TOP 5 productos más valiosos")
st.dataframe(top_productos[["Producto", "ValorTotal"]])
