const formCadastro = document.getElementById("form-cadastro")

formCadastro.addEventListener("submit", async (event) => {
    event.preventDefault()

    const nome = document.getElementById("usuario").value
    const email = document.getElementById("email").value
    const senha = document.getElementById("senha").value
    const confirmarSenha = document.getElementById("confirmar_senha").value

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem")
        return
    }

    try {
        await apiRequest("/register", {
            method: "POST",
            body: JSON.stringify({
                nome,
                email,
                senha
            })
        })

        alert("Cadastro realizado! Confira seu e-mail para confirmar a conta.")
        window.location.href = "login.html"

    } catch (erro) {
        alert(erro.message)
    }
})