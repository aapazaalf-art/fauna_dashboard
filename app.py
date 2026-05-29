# 5. Tabla de Detalle y Exportación Masiva
st.subheader("📋 Tabla de Detalle y Exportación")

with st.expander("🔧 Configuración de Columnas (opcional)", expanded=False):
    st.info("ℹ️ Por defecto se muestran **todas las columnas**. Puedes desmarcar las que no necesites.")
    all_cols = [c for c in ['UM_id', 'Ecozona', 'Departamento', 'Periodo', 'Nombre científico', 'Nombre común', 
                            'Familia', 'Clase', 'Tipo de registro', 'CUA', 'Zona UTM', 
                            'Altitud (m)', 'Distancia (m)', 'Número de foto'] if c in df_filtered.columns]
    sel_cols = st.multiselect("Columnas a visualizar y descargar:", options=all_cols, default=all_cols)

# Preparar dataset para tabla y exportación (siempre usa TODAS las filas filtradas)
export_df = df_filtered[sel_cols] if sel_cols else df_filtered

st.markdown(f"📥 **{len(export_df):,} registros completos** coinciden con los filtros activos.")
st.dataframe(export_df, use_container_width=True, hide_index=True)

# Botón de descarga masiva
csv_data = export_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=f"⬇️ Descargar TODOS los registros filtrados ({len(export_df):,} filas)",
    data=csv_data,
    file_name="fauna_export_completa.csv",
    mime="text/csv",
    use_container_width=True
)
st.caption("✅ La descarga incluye únicamente las filas que cumplen con los filtros seleccionados en el sidebar, con la información completa de cada registro.")
