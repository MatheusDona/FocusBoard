const formCadastro = document.getElementById("form-cadastro")
const mensagemCadastro = document.getElementById("mensagem-cadastro")

function mostrarMensagemCadastro(texto, tipo = "erro") {
    mensagemCadastro.textContent = texto
    mensagemCadastro.className = `mensagem ${tipo}`
}

formCadastro.addEventListener("submit", async (event) => {
    event.preventDefault()

    const nome = document.getElementById("usuario").value.trim()
    const email = document.getElementById("email").value.trim()
    const senha = document.getElementById("senha").value
    const confirmarSenha = document.getElementById("confirmar_senha").value

    if (senha !== confirmarSenha) {
        mostrarMensagemCadastro("As senhas não coincidem. Confira os campos e tente novamente.")
        return
    }

    try {
        await apiRequest("/register", {
            method: "POST",
            body: JSON.stringify({ nome, email, senha })
        })

        window.location.href = "login.html?cadastro=1"
    } catch (erro) {
        mostrarMensagemCadastro(erro.message)
    }
})

formCadastro.addEventListener("input", () => {
    mensagemCadastro.textContent = ""
    mensagemCadastro.className = "mensagem"
})
