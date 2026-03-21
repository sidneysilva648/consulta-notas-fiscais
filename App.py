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

# === CABEÇALHO ===
st.title("🧾 Consulta de Nota Fiscal")
st.caption("Digite o número da nota fiscal para visualizar os dados do cliente")

st.divider()

# === FORMULÁRIO DE CONSULTA ===
col1, col2 = st.columns([3, 1])

with col1:
    numero_nf = st.text_input(
        "Número da Nota Fiscal",
        placeholder="Ex: 123456",
        label_visibility="collapsed"
    )

with col2:
    consultar = st.button("🔍 Consultar", use_container_width=True)

# === PROCESSAR CONSULTA ===
if consultar or numero_nf:
    if not numero_nf.strip():
        st.warning("Digite o número da nota fiscal.")
    else:
        with st.spinner("Consultando Salesforce..."):
            dados, erro = buscar_nota_fiscal(numero_nf.strip())

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
                <div class="valor">📄 {dados['numero_nf']}</div>
                
                <div class="label">Telefone</div>
                <div class="valor">📞 {dados['telefone']}</div>
                
                <div class="label">Ponto de Referência</div>
                <div class="valor">📍 {dados['ponto_referencia']}</div>
                
                <div class="label">Status</div>
                <div class="valor">📋 {dados['status']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Botão para copiar telefone
            st.code(dados['telefone'], language=None)
            
            # Histórico de consultas na sessão
            if "historico" not in st.session_state:
                st.session_state.historico = []
            
            if numero_nf not in [h["nf"] for h in st.session_state.historico]:
                st.session_state.historico.append({
                    "nf": numero_nf,
                    "telefone": dados['telefone'],
                    "referencia": dados['ponto_referencia']
                })

# === HISTÓRICO DE CONSULTAS ===
if "historico" in st.session_state and st.session_state.historico:
    st.divider()
    st.subheader("📋 Consultas recentes")
    
    for item in reversed(st.session_state.historico[-5:]):
        with st.expander(f"NF: {item['nf']}"):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Telefone:** {item['telefone']}")
            col2.markdown(f"**Referência:** {item['referencia']}")

st.divider()
st.caption("Sistema de consulta interno — Bemol S.A.")
