const formLogin = document.getElementById("form-login")

const parametros = new URLSearchParams(window.location.search)

if (parametros.get("expirada") === "1") {
    alert("Sua sessão expirou. Faça login novamente.")
}

formLogin.addEventListener("submit", async (event) => {
    event.preventDefault()

    const email = document.getElementById("email").value
    const senha = document.getElementById("senha").value

    try {
        const resposta = await apiRequest("/login", {
            method: "POST",
            body: JSON.stringify({
                email,
                senha
            })
        })

        localStorage.setItem("token", resposta.access_token)

        window.location.href = "index.html"

    } catch (erro) {
        alert(erro.message)
    }
})