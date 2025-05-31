
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cuadre de Caja", layout="wide")

st.title("🧾 Cuadre de Caja Diario")

st.sidebar.header("⚙️ Parámetros")
tasa = st.sidebar.number_input("Tasa del día (Bs/$)", min_value=0.1, value=145.0, step=0.1)

st.markdown("### Ingresos por método")
metodos = [
    "P/ VENTA", "P/MOVIL", "BS LIBRO", "$ LIBRO", "ZELLE", "DEVOLUCION",
    "DESCUENTOS", "CREDITO", "S/USO FERRETERIA", "S/MERC SURTIR",
    "S/ MERC NINO", "S/VALE CLIENTE(MERCA)"
]

data = []
for metodo in metodos:
    bs = st.number_input(f"{metodo} (Bs)", key=f"{metodo}_bs", min_value=0.0)
    usd = st.number_input(f"{metodo} ($)", key=f"{metodo}_usd", min_value=0.0)
    conv_usd = bs / tasa if bs > 0 else 0
    data.append([metodo, bs, usd, round(conv_usd, 2)])

df = pd.DataFrame(data, columns=["Método", "Bs", "$", "Convertido $ (Bs/Tasa)"])
df["Total $"] = df["$"] + df["Convertido $ (Bs/Tasa)"]

st.markdown("### 💰 Totales del sistema")
st.dataframe(df, use_container_width=True)
total_bs = df["Bs"].sum()
total_usd = df["$"].sum()
total_convertido = df["Convertido $ (Bs/Tasa)"].sum()
total_final_usd = df["Total $"].sum()

st.write(f"**Total Bs ingresados:** {total_bs:,.2f}")
st.write(f"**Total $ ingresados:** {total_usd:,.2f}")
st.write(f"**Convertido $ desde Bs:** {total_convertido:,.2f}")
st.write(f"**Total sistema ($):** :green[{total_final_usd:,.2f}]")

st.markdown("### 🧮 Efectivo físico")
bs_caja = st.number_input("Bs en caja", min_value=0.0)
usd_caja = st.number_input("$ en caja", min_value=0.0)
bs_sencillo = st.number_input("Bs sencillo", min_value=0.0)
usd_sencillo = st.number_input("$ sencillo", min_value=0.0)

total_fisico_bs = bs_caja + bs_sencillo
total_fisico_usd = usd_caja + usd_sencillo
total_fisico_usd_equivalente = total_fisico_usd + (total_fisico_bs / tasa)

st.write(f"**Total físico equivalente en $:** :blue[{total_fisico_usd_equivalente:,.2f}]")

diferencia = total_fisico_usd_equivalente - total_final_usd
color = "green" if diferencia >= 0 else "red"
st.write(f"**Diferencia ($):** :{color}[{diferencia:,.2f}]")

# Exportar a Excel (opcional)
if st.button("📥 Descargar en Excel"):
    df_export = df.copy()
    df_export.loc["TOTAL"] = df_export.sum(numeric_only=True)
    df_export.to_excel("cuadre_caja.xlsx")
    st.success("Archivo Excel generado: cuadre_caja.xlsx")
