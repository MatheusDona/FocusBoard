const formLogin = document.getElementById("form-login")
const parametros = new URLSearchParams(window.location.search)
const mensagemLogin = document.getElementById("mensagem-login")

function mostrarMensagemLogin(texto, tipo) {
    mensagemLogin.textContent = texto
    mensagemLogin.className = `mensagem ${tipo}`
}

if (parametros.get("cadastro") === "1") {
    mostrarMensagemLogin("Cadastro realizado! Verifique seu e-mail para confirmar a conta antes de fazer login.", "aviso")
} else if (parametros.get("expirada") === "1") {
    mostrarMensagemLogin("Sua sessão expirou. Faça login novamente para continuar.", "aviso")
} else if (parametros.get("conta_excluida") === "1") {
    mostrarMensagemLogin("Sua conta foi excluída com sucesso.", "sucesso")
}

formLogin.addEventListener("submit", async (event) => {
    event.preventDefault()

    const email = document.getElementById("email").value.trim()
    const senha = document.getElementById("senha").value

    try {
        const resposta = await apiRequest("/login", {
            method: "POST",
            body: JSON.stringify({ email, senha })
        })

        localStorage.setItem("token", resposta.access_token)
        window.location.href = "index.html"
    } catch (erro) {
        const tipo = erro.message.toLowerCase().includes("confirme seu e-mail") ? "aviso" : "erro"
        mostrarMensagemLogin(erro.message, tipo)
    }
})

formLogin.addEventListener("input", () => {
    mensagemLogin.textContent = ""
    mensagemLogin.className = "mensagem"
})
