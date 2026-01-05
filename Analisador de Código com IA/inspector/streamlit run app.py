import streamlit as st
import os
import config
import scanner
import analyzer
import summarizer

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Código IA",
    page_icon="🔍",
    layout="wide"
)

# --- Cabeçalho e Introdução ---
st.title("🔍 Analisador de Código com IA")
st.markdown("""
Esta ferramenta lê projetos locais, identifica riscos de segurança e gera um relatório executivo explicando o código.
Ideal para entender bases de código legadas ou novas de forma rápida.
""")

# --- Verificação de Configuração ---
if not config.OPENROUTER_API_KEY:
    st.error("⚠️ **Erro de Configuração:** A chave da API (`OPENROUTER_API_KEY`) não foi encontrada.")
    st.info("Por favor, crie um arquivo `.env` na raiz do projeto e adicione sua chave da OpenRouter.")
    st.stop() # Interrompe a execução se não houver chave

# --- Barra Lateral (Inputs) ---
with st.sidebar:
    st.header("Configurações")
    
    # Campo para o caminho do projeto
    project_path = st.text_input(
        "Caminho do Projeto", 
        value=".", 
        help="Digite o caminho completo da pasta do projeto ou use '.' para a pasta atual."
    )
    
    st.divider()
    
    # Informações do Modelo
    st.caption(f"Modelo IA: `{config.OPENROUTER_MODEL}`")
    st.caption(f"Timeout: {config.TIMEOUT_SECONDS}s")

# --- Área Principal ---
st.divider()

# Botão de Ação
if st.button("🚀 Iniciar Análise", type="primary", use_container_width=True):
    
    # 1. Validação do Caminho
    if not os.path.isdir(project_path):
        st.error(f"❌ O caminho informado não é um diretório válido: `{project_path}`")
    else:
        try:
            # 2. Barra de Progresso e Status
            # Usamos st.status para mostrar o progresso passo a passo
            with st.status("Analisando projeto...", expanded=True) as status:
                
                # Passo A: Escanear Arquivos
                st.write("📂 Escaneando arquivos locais...")
                scanned_files = scanner.scan_project(project_path)
                
                if not scanned_files:
                    st.warning("Nenhum arquivo compatível foi encontrado no diretório.")
                    status.update(label="Análise finalizada (vazia)", state="complete", expanded=False)
                    st.stop()
                
                st.write(f"✅ {len(scanned_files)} arquivos encontrados para análise.")

                # Passo B: Analisar Segurança
                st.write("🔒 Verificando segurança estática...")
                security_findings = analyzer.analyze_security(scanned_files)
                
                if security_findings:
                    st.warning(f"⚠️ {len(security_findings)} possíveis riscos de segurança encontrados.")
                else:
                    st.success("✅ Nenhum risco óbvio encontrado na verificação estática.")

                # Passo C: Gerar Relatório com IA
                st.write("🤖 Gerando relatório executivo com IA (isso pode levar um momento)...")
                report = summarizer.generate_report(scanned_files, security_findings)
                
                status.update(label="Análise concluída com sucesso!", state="complete", expanded=False)

            # 3. Exibição dos Resultados
            st.success("Relatório gerado com sucesso!")
            
            # Organização em Abas
            tab_resumo, tab_detalhes = st.tabs(["📝 Resumo Executivo", "⚙️ Detalhes Técnicos"])

            with tab_resumo:
                st.markdown(report)

            with tab_detalhes:
                st.subheader("Arquivos Analisados")
                st.caption("Lista de arquivos que foram enviados para a IA.")
                file_paths = [f['path'] for f in scanned_files]
                st.write("\n".join([f"- {p}" for p in file_paths]))

                st.divider()
                
                st.subheader("Achados de Segurança (Detalhado)")
                if not security_findings:
                    st.info("Nenhum achado de segurança registrado.")
                else:
                    for finding in security_findings:
                        with st.expander(f"🚨 {finding['file']} (Linha {finding['line']})"):
                            st.markdown(f"**Categoria:** {finding['category']}")
                            st.markdown(f"**Descrição:** {finding['description']}")
                            st.code(finding['snippet'], language="text")

        except ValueError as ve:
            st.error(f"Erro de Validação: {ve}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado durante a análise.")
            st.exception(e) # Mostra o erro completo para debug
