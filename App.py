import streamlit as st
from salesforce_tools import buscar_nota_fiscal

st.set_page_config(
    page_title="Consulta Nota Fiscal",
    page_icon="🧾",
    layout="centered"
)

st.markdown("""
<style>
    .resultado-card {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
    .erro-card {
        background: #fff5f5;
        border: 1px solid #feb2b2;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
    .label {
        font-size: 12px;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 2px;
    }
    .valor {
        font-size: 18px;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧾 Consulta de Nota Fiscal")
st.caption("Digite o número da nota fiscal e a série para visualizar os dados")

st.divider()

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    numero_nf = st.text_input("Número da NF", placeholder="Ex: 009952081")
with col2:
    serie = st.text_input("Série", placeholder="Ex: 104")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    consultar = st.button("🔍 Consultar", use_container_width=True)

if consultar:
    if not numero_nf.strip():
        st.warning("Digite o número da nota fiscal.")
    else:
        with st.spinner("Consultando Salesforce..."):
            dados, erro = buscar_nota_fiscal(numero_nf.strip(), serie.strip())

        if erro:
            st.markdown(f"""
            <div class="erro-card">
                <b>❌ {erro}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("Nota fiscal encontrada!")
            st.markdown(f"""
            <div class="resultado-card">
                <div class="label">Número da Nota Fiscal</div>
                <div class="valor">📄 {dados['numero_nf']} — Série {dados['serie']}</div>
                <div class="label">Telefone</div>
                <div class="valor">📞 {dados['telefone']}</div>
                <div class="label">Ponto de Referência</div>
                <div class="valor">📍 {dados['ponto_referencia']}</div>
                <div class="label">Status</div>
                <div class="valor">📋 {dados['status']}</div>
                <div class="label">Data do Documento</div>
                <div class="valor">📅 {dados['data']}</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("Sistema de consulta interno — Bemol S.A.")


#git add . ; git commit -m "msg" ; git push#


