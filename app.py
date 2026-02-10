import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import time

# --- 1. CONFIGURAÇÃO DE AMBIENTE ---
load_dotenv()
if "GEMINI_API_KEY" not in os.environ:
    st.error("ERRO: GEMINI_API_KEY não configurada no .env")
    st.stop()

# Inicializa o Cliente com a nova SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configurações Visuais
st.set_page_config(page_title="CloudPulse GRC - Compliance AI", layout="wide", page_icon="🛡️")

# Estilização Profissional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #003366; color: white; font-weight: bold; }
    .stTextArea>div>div>textarea { border-radius: 10px; border: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRA LATERAL (BRANDING) ---
with st.sidebar:
    st.title("🛡️ CloudPulse GRC")
    st.subheader("Governança & Riscos")
    st.markdown("---")
    st.info(f"**Analista Responsável:**\nAlexandre Macchia Araujo")
    st.write(f"**Motor de IA:** Gemini 2.0 Flash")
    st.write(f"**Status:** Online")
    st.markdown("---")
    
    if st.button("🗑️ Limpar Auditoria"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 3. INTERFACE DE ENTRADA ---
st.title("Agente Analista de Conformidade (Compliance AI)")
st.caption(f"Cerquilho/SP - {datetime.now().strftime('%Y')} | CloudPulseCorp AI Division")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📖 Norma de Referência")
    norma = st.text_area("Insira a Lei, ISO ou Política Interna:", 
                        height=300, 
                        placeholder="Ex: LGPD, Normas da CVM, Regimento Interno...",
                        key="input_norma")

with col2:
    st.markdown("### 📄 Documento para Auditoria")
    documento = st.text_area("Insira o Contrato ou Documento para análise:", 
                            height=300, 
                            placeholder="Ex: Cláusulas do contrato de prestação de serviços...",
                            key="input_doc")

st.markdown("---")

# --- 4. LÓGICA DE AUDITORIA COM RETRY AUTOMÁTICO ---
if st.button("🚀 EXECUTAR AUDITORIA DE CONFORMIDADE"):
    if not norma or not documento:
        st.warning("⚠️ Atenção: Preencha a Norma e o Documento para iniciar.")
    else:
        with st.spinner('O Agente está auditando o documento (Tentativa automática de cota)...'):
            
            tentativas_maximas = 3
            sucesso = False
            
            for i in range(tentativas_maximas):
                try:
                    # Prompt Estruturado para GRC
                    prompt_final = f"""
                    Você é o Agente Analista de Conformidade da CloudPulseCorp.
                    Sua tarefa é auditar o DOCUMENTO com base na NORMA fornecida.
                    
                    NORMA: {norma}
                    DOCUMENTO: {documento}
                    
                    FORMATO DE RESPOSTA OBRIGATÓRIO:
                    # 📊 RELATÓRIO DE COMPLIANCE
                    **STATUS:** [CONFORME | RISCO BAIXO | MÉDIO | ALTO]
                    
                    ## 🚩 VIOLAÇÕES IDENTIFICADAS
                    - (Liste as falhas em relação à norma)
                    
                    ## ⚠️ CLÁUSULAS ABUSIVAS / RISCOS
                    - (Liste armadilhas contratuais)
                    
                    ## 💡 PLANO DE AÇÃO (RECOMENDAÇÕES)
                    - (Sugestões para o gestor)
                    """

                    # Chamada oficial para Gemini 2.0 Flash
                    response = client.models.generate_content(
                        model='gemini-2.0-flash', 
                        contents=prompt_final
                    )
                    
                    st.session_state['resultado'] = response.text
                    st.markdown(st.session_state['resultado'])
                    sucesso = True
                    break # Auditoria concluída, sai do loop
                
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        if i < tentativas_maximas - 1:
                            st.warning(f"🔄 Limite de cota atingido. Tentativa {i+1} de {tentativas_maximas}. Aguardando 10s...")
                            time.sleep(10) # Pausa estratégica para resetar a cota
                        else:
                            st.error("❌ **Erro de Cota:** O Google limitou as requisições agora. Aguarde 1 minuto para tentar novamente.")
                    else:
                        st.error(f"❌ Erro Técnico: {e}")
                        break

# --- 5. EXPORTAÇÃO PARA PDF ---
if 'resultado' in st.session_state:
    st.markdown("---")
    
    def gerar_pdf(texto_auditoria):
        pdf = FPDF()
        pdf.add_page()
        # Header Corporativo
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "CLOUDPULSECORP - AUDITORIA DE COMPLIANCE", ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, f"Analista: Alexandre Macchia Araujo | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
        pdf.ln(10)
        
        # Conteúdo
        pdf.set_font("Arial", size=11)
        # Limpeza de caracteres especiais para o PDF padrão
        limpo = texto_auditoria.replace("#", "").replace("**", "").replace("📊", "").replace("🚩", "").replace("⚠️", "").replace("💡", "")
        pdf.multi_cell(0, 8, limpo.encode('latin-1', 'ignore').decode('latin-1'))
        
        return pdf.output(dest='S').encode('latin-1')

    col_btn, col_txt = st.columns([1, 2])
    with col_btn:
        pdf_data = gerar_pdf(st.session_state['resultado'])
        st.download_button(
            label="📥 Baixar Relatório Oficial (PDF)",
            data=pdf_data,
            file_name=f"Compliance_CloudPulse_{datetime.now().strftime('%d%m%Y')}.pdf",
            mime="application/pdf"
        )
    with col_txt:
        st.success("O relatório foi gerado e está pronto para arquivamento ou envio executivo.")