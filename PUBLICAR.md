# Publicar o FocusBoard (Vercel + Render + Neon + Resend)

O projeto mantém as regras atuais de cadastro, confirmação de e-mail, login, tarefas e perfil. A mudança no envio de e-mail é somente de transporte: em produção usa Resend por HTTPS; localmente continua aceitando Gmail SMTP como fallback.

## 1. Neon
1. Crie um projeto em https://neon.com/.
2. Em **Connect**, copie a connection string PostgreSQL (de preferência pooled).
3. Guarde-a como `DATABASE_URL`. Não publique essa URL no GitHub nem no frontend.

O banco Neon começa vazio. O SQLite local não é copiado automaticamente.

## 2. Resend: configurar o envio de e-mail
1. Crie uma conta em https://resend.com/.
2. Em **API Keys**, crie uma chave para o FocusBoard.
3. Em **Domains**, adicione e verifique um domínio que você controla, seguindo os registros DNS indicados pelo Resend.
4. Use um remetente desse domínio, por exemplo `FocusBoard <noreply@seudominio.com>`.

O remetente de teste `onboarding@resend.dev` é limitado e não deve ser usado como remetente definitivo para enviar a todos os usuários. Para confirmações de contas de outras pessoas, configure um domínio/remetente autorizado no Resend.

Não é necessário senha Gmail nem SMTP no Render. A aplicação usa a API HTTPS do Resend por meio de `RESEND_API_KEY`.

## 3. GitHub
Envie a pasta inteira do FocusBoard para um repositório GitHub. O `.gitignore` ignora `.env`, bancos SQLite, dependências e arquivos de build. Não envie credenciais reais.

## 4. Render: publicar o backend
1. No Render, escolha **New + > Blueprint** e conecte o repositório.
2. O Render encontrará `render.yaml` na raiz e criará `focusboard-api`.
3. Informe as variáveis:
   - `DATABASE_URL`: connection string do Neon.
   - `RESEND_API_KEY`: chave criada no Resend.
   - `EMAIL_REMETENTE`: remetente verificado, por exemplo `FocusBoard <noreply@seudominio.com>`.
4. O Render gera `SECRET_KEY` automaticamente. As demais configurações já têm valores padrão.
5. Copie a URL pública do serviço, por exemplo `https://focusboard-api.onrender.com`.

## 5. Vercel: publicar o frontend
1. Importe o mesmo repositório GitHub na Vercel.
2. Em **Root Directory**, selecione `frontend`.
3. Build Command: `npm run build`. Output Directory: `dist`.
4. Em **Environment Variables**, crie `API_URL` com a URL pública do Render, sem barra no final.
5. Publique e copie o domínio público da Vercel.

## 6. Conectar os endereços
No Render > Environment:
- `FRONTEND_URL` = domínio público da Vercel.
- `BACKEND_URL` = domínio público do Render.

Salve e faça o redeploy do backend.

## 7. Testar
1. Abra o domínio da Vercel.
2. Cadastre-se com um e-mail que você possa acessar.
3. Confira o recebimento da mensagem do Resend.
4. Abra o link de confirmação, faça login e teste tarefas e perfil.

## Desenvolvimento local
O frontend local continua apontando para `http://127.0.0.1:8000`. O SQLite continua sendo o padrão se `DATABASE_URL` não estiver definido.

Para envio local, você pode preencher `EMAIL_REMETENTE` e `EMAIL_SENHA` com uma senha de app Gmail. Se configurar `RESEND_API_KEY`, o Resend será priorizado.

## Observações
- `API_URL` é incorporada ao JavaScript durante o build da Vercel; se mudar, publique o frontend novamente.
- `DATABASE_URL`, `SECRET_KEY` e `RESEND_API_KEY` ficam somente nas variáveis de ambiente do Render.
- O Render Free pode suspender o serviço após inatividade; o primeiro acesso depois disso pode demorar.
- O banco Neon é o banco de produção. O SQLite local não é transferido automaticamente.
- O fluxo de cadastro e confirmação não foi alterado. Apenas `enviar_email()` ganhou suporte ao Resend, mantendo SMTP como fallback local.
