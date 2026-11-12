import json
import os
import smtplib
from email.message import EmailMessage
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


def _enviar_por_resend(destinatario: str, assunto: str, conteudo: str, api_key: str):
    """
    Envia e-mails pela API HTTPS do Resend.
    Isso evita depender das portas SMTP bloqueadas no Render Free.
    """
    remetente = os.getenv("EMAIL_REMETENTE")
    if not remetente:
        raise ValueError(
            "Configure EMAIL_REMETENTE com um remetente verificado no Resend."
        )

    payload = {
        "from": remetente,
        "to": [destinatario],
        "subject": assunto,
        "text": conteudo,
    }

    requisicao = Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(requisicao, timeout=20) as resposta:
            if resposta.status < 200 or resposta.status >= 300:
                raise RuntimeError(
                    f"Resend retornou um status inesperado: {resposta.status}"
                )
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Falha no envio pelo Resend (HTTP {erro.code}): {detalhe}"
        ) from erro
    except URLError as erro:
        raise RuntimeError(
            f"Não foi possível conectar ao serviço de e-mail: {erro.reason}"
        ) from erro


def _enviar_por_smtp(destinatario: str, assunto: str, conteudo: str):
    """Fallback SMTP para desenvolvimento local, mantendo o comportamento atual."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    if not remetente or not senha:
        raise ValueError(
            "Configure RESEND_API_KEY para produção ou EMAIL_REMETENTE e "
            "EMAIL_SENHA para envio SMTP local."
        )

    mensagem = EmailMessage()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto
    mensagem.set_content(conteudo)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(mensagem)
    except (smtplib.SMTPException, OSError) as erro:
        raise RuntimeError(f"Erro ao enviar e-mail por SMTP: {erro}") from erro


def enviar_email(destinatario: str, assunto: str, conteudo: str):
    """
    Prioriza Resend quando RESEND_API_KEY estiver configurada.
    Sem a chave, mantém o envio SMTP usado no ambiente local.
    """
    api_key = os.getenv("RESEND_API_KEY")

    if api_key:
        _enviar_por_resend(destinatario, assunto, conteudo, api_key)
        return

    _enviar_por_smtp(destinatario, assunto, conteudo)
