**Ferramentas de captura de cliques**

O projeto tem dois gravadores, um por revista. Ambos salvam
os resultados em `tools/captures/` (ignorado pelo Git, para
evitar vazar credenciais).

=== Brasíndice (site) ===

1. Preencha `brasicinde.site_url` em `config/settings.json`.
2. Execute:

   ```powershell
   .\tools\start_capture_brasicinde.ps1
   ```

3. O navegador abre. Faça login e siga a sequência de cliques
   até gerar o arquivo. O Playwright grava o código em tempo
   real e salva em `tools/captures/brasicinde_codegen.py`.
4. Ao terminar, feche o navegador. Revise o script e remova a
   senha (ela deve ir para `.env`, não para o código).

=== SIMPRO (desktop Delphi) ===

O pywinauto não tem gravador nativo. Use o despejador de UI:

1. Abra o SIMPRO e navegue até a primeira tela do fluxo.
2. Neste terminal, execute:

   ```powershell
   python tools/dump_simpro_ui.py
   ```

3. Pressione ENTER para capturar a árvore de controles da
   janela ativa (tipo, nome e automation_id de cada botão/menu).
4. Navegue para a próxima tela e pressione ENTER novamente.
5. Digite `q` para sair e salvar o relatório em
   `tools/captures/simpro_dump_<timestamp>.txt`.

Se a árvore vier vazia ou incompleta com o backend padrão
(`uia`), tente `python tools/dump_simpro_ui.py win32` (comum
em apps Delphi antigos).

=== Próxima etapa ===

Envie os arquivos de captura (ou cole a saída aqui). Com eles,
implementamos `src/brasicinde/automation.py` e
`src/simpro/automation.py` com os cliques reais.
