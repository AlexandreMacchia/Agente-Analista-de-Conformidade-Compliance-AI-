# 🛡️ Agente Analista de Conformidade (Compliance AI)
### **CloudPulseCorp - Inteligência de Auditoria e GRC**

Este projeto é uma solução avançada de **Governança, Riscos e Conformidade (GRC)** que utiliza Inteligência Artificial Generativa para automatizar a auditoria de documentos. O agente analisa contratos, termos e e-mails comparando-os com normas de referência (como LGPD, ISO 27001 ou Políticas Internas) em segundos.

---

## 🚀 Funcionalidades Principais
- **Auditoria Inteligente:** Comparação técnica entre normas regulatórias e documentos operacionais.
- **Detecção de Riscos:** Identificação automática de cláusulas abusivas, omissões e não-conformidades.
- **Relatórios Executivos:** Geração de relatórios profissionais em PDF com status de risco e recomendações.
- **Resiliência de Infraestrutura:** Implementação de lógica de *Retry Automático* para garantir estabilidade mesmo em alta demanda de API.

---

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.13
- **IA Engine:** Google Gemini 2.0 Flash (SDK `google-genai`)
- **Dashboard:** Streamlit
- **Documentação:** FPDF
- **DevOps:** GitHub & Streamlit Cloud

---

## 📋 Como Utilizar

1. **Entrada de Dados:** Insira a norma (base legal) no campo à esquerda.
2. **Documento:** Insira o texto que deseja auditar no campo à direita.
3. **Processamento:** Clique em "Executar Auditoria". O sistema fará até 3 tentativas automáticas em caso de congestionamento de rede.
4. **Resultado:** Visualize a análise na tela e exporte o relatório oficial em PDF.

---

## 🔒 Segurança e Boas Práticas (GRC)
- **Privacidade:** O sistema não armazena os dados sensíveis após a análise.
- **Proteção de Credenciais:** Uso de variáveis de ambiente (`.env`) e segredos criptografados para proteção da API Key.

---

## 👨‍💻 Responsável Técnico
**Alexandre Macchia Araujo** *Desenvolvedor & Analista de GTI na CloudPulseCorp*

"Focado em transformar processos complexos de conformidade em agilidade estratégica para o ambiente corporativo."

---
