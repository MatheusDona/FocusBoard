const API_URL = "http://127.0.0.1:8000"

function mostrarModalSessaoExpirada() {
    let modal = document.getElementById("sessao-expirada")

    // Cria o modal caso a página ainda não tenha sua marcação.
    if (!modal) {
        modal = document.createElement("div")
        modal.id = "sessao-expirada"
        modal.className = "modal modal-sessao"
        modal.innerHTML = `
            <div class="modal-caixa modal-aviso">
                <div class="modal-icone">!</div>
                <h2>Sessão expirada</h2>
                <p>Sua sessão expirou por segurança. Entre novamente para continuar usando o FocusBoard.</p>
                <button type="button" id="ir-login" class="botao">Ir para o login</button>
            </div>
        `
        document.body.appendChild(modal)
    }

    modal.style.display = "flex"

    const botao = modal.querySelector("#ir-login")
    if (botao && !botao.dataset.listenerAdicionado) {
        botao.dataset.listenerAdicionado = "true"
        botao.addEventListener("click", () => {
            window.location.href = "login.html?expirada=1"
        })
    }
}

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("token")
    const headers = { ...options.headers }

    if (options.body) headers["Content-Type"] = "application/json"
    if (token) headers["Authorization"] = `Bearer ${token}`

    const resposta = await fetch(`${API_URL}${endpoint}`, { ...options, headers })

    let dados = null
    if (resposta.status !== 204) {
        try { dados = await resposta.json() } catch { dados = null }
    }

    if (resposta.status === 401 && token) {
        localStorage.removeItem("token")
        mostrarModalSessaoExpirada()
        throw new Error("Sessão expirada")
    }

    if (!resposta.ok) {
        throw new Error(dados?.detail || "Erro na comunicação com o servidor")
    }

    return dados
}


// Alterna a visibilidade das senhas nos campos que possuem o botão de olho.
document.querySelectorAll("[data-password-toggle]").forEach((botao) => {
    botao.addEventListener("click", () => {
        const campo = document.getElementById(botao.dataset.passwordToggle)
        if (!campo) return

        const mostrar = campo.type === "password"
        campo.type = mostrar ? "text" : "password"
        botao.setAttribute("aria-label", mostrar ? "Ocultar senha" : "Mostrar senha")
        botao.setAttribute("title", mostrar ? "Ocultar senha" : "Mostrar senha")
        botao.classList.toggle("senha-visivel", mostrar)
    })
})
