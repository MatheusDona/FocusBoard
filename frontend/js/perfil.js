const emailAtual = document.getElementById("email-atual")
const inputNome = document.getElementById("usuario")

if (!localStorage.getItem("token")) {
    window.location.href = "login.html"
}

async function carregarPerfil() {
    try {
        const usuario = await apiRequest("/usuarios/me")

        emailAtual.textContent = usuario.email
        inputNome.value = usuario.nome

    } catch (erro) {
        if (erro.message !== "Sessão expirada") {
            alert(erro.message)
        }
    }
}

document.getElementById("form-nome").addEventListener("submit", async (event) => {
    event.preventDefault()

    const nome = inputNome.value.trim()

    try {
        await apiRequest("/usuarios/me/nome", {
            method: "PATCH",
            body: JSON.stringify({ nome })
        })

        mostrarMensagem("mensagem-nome", "Nome atualizado com sucesso!", "sucesso")
    } catch (erro) {
        mostrarMensagem("mensagem-nome", erro.message, "erro")
    }
})

document.getElementById("form-senha").addEventListener("submit", async (event) => {
    event.preventDefault()

    const senha_atual = document.getElementById("senha_antiga").value
    const nova_senha = document.getElementById("senha_nova").value
    const confirmar_senha = document.getElementById("confirmar_senha").value

    if (nova_senha !== confirmar_senha) {
        mostrarMensagem("mensagem-senha", "As senhas precisam ser iguais", "erro")
        return
    }

    try {
        await apiRequest("/usuarios/me/senha", {
            method: "PATCH",
            body: JSON.stringify({
                senha_atual,
                nova_senha,
                confirmar_senha
            })
        })

        mostrarMensagem("mensagem-senha", "Senha alterada com sucesso!", "sucesso")
        document.getElementById("form-senha").reset()

    } catch (erro) {
        mostrarMensagem("mensagem-senha", erro.message, "erro")
    }
})

document.getElementById("confirmar-sair-btn").addEventListener("click", () => {
    localStorage.removeItem("token")
    window.location.href = "login.html"
})

function mostrarMensagem(id, texto, tipo) {
    const mensagem = document.getElementById(id)

    mensagem.textContent = texto
    mensagem.className = `mensagem ${tipo}`
}

inputNome.addEventListener("input", () => {
    const mensagem = document.getElementById("mensagem-nome")
    mensagem.className = "mensagem"
    mensagem.textContent = ""
})

document.getElementById("form-senha").addEventListener("input", () => {
    const mensagem = document.getElementById("mensagem-senha")
    mensagem.className = "mensagem"
    mensagem.textContent = ""
})

carregarPerfil()