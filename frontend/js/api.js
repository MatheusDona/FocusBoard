const API_URL = "http://127.0.0.1:8000"

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("token")

    const headers = {
        ...options.headers
    }

    if (options.body) {
        headers["Content-Type"] = "application/json"
    }

    if (token) {
        headers["Authorization"] = `Bearer ${token}`
    }

    const resposta = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    })

    const dados = resposta.status === 204
        ? null
        : await resposta.json()

    if (resposta.status === 401 && token) {
        localStorage.removeItem("token")

        const modal = document.getElementById("sessao-expirada")
        modal.style.display = "flex"

        document.getElementById("ir-login").addEventListener("click", () => {
            window.location.href = "login.html"
        })

        throw new Error("Sessão expirada")
    }

    if (!resposta.ok) {
        throw new Error(dados?.detail || "Erro na comunicação com o servidor")
    }

    return dados
}