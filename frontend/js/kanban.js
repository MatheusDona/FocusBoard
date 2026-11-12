const formTarefa = document.getElementById("form-tarefa")

const colunas = {
    "Fazer": document.getElementById("coluna-fazer"),
    "Em andamento": document.getElementById("coluna-andamento"),
    "Feito": document.getElementById("coluna-feito"),
    "Pendente": document.getElementById("coluna-pendente")
}

let tarefas = []
let tarefaEditandoId = null
let tarefaStatusId = null

if (!localStorage.getItem("token")) {
    window.location.href = "login.html"
}

async function carregarTarefas() {
    try {
        tarefas = await apiRequest("/tarefas")
        renderizarTarefas()
    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
}

function renderizarTarefas() {
    Object.values(colunas).forEach(coluna => {
        coluna.querySelectorAll(".card").forEach(card => card.remove())
    })

    tarefas.forEach(tarefa => {
        const coluna = colunas[tarefa.status]

        if (!coluna) return

        const card = document.createElement("div")
        card.className = "card"

        const prazo = tarefa.data_prazo
            ? new Date(`${tarefa.data_prazo}T00:00:00`).toLocaleDateString("pt-BR")
            : "Sem prazo"

        card.innerHTML = `
            <h3>${escaparHTML(tarefa.titulo)}</h3>
            <p>${escaparHTML(tarefa.descricao || "Sem descrição")}</p>
            <p>Prioridade: ${escaparHTML(tarefa.prioridade)}</p>
            <p>Prazo: ${prazo}</p>
            <details class="menu-opcoes">
                <summary title="Opções da tarefa">⋮</summary>

                <div class="menu-dropdown">
                    <button type="button" onclick="editarTarefa(${tarefa.id})">
                        Editar
                    </button>

                    <button type="button" onclick="alterarStatus(${tarefa.id})">
                        Alterar status
                    </button>

                    <button type="button" onclick="excluirTarefa(${tarefa.id})">
                        Excluir
                    </button>
                </div>
            </details>
        `

        coluna.appendChild(card)
    })
}

function escaparHTML(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, caractere => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[caractere])
}

formTarefa.addEventListener("submit", async (event) => {
    event.preventDefault()

    const dados = {
        titulo: document.getElementById("titulo").value,
        descricao: document.getElementById("descricao").value || null,
        prioridade: document.getElementById("prioridade").value,
        data_prazo: document.getElementById("data_prazo").value || null
    }

    try {
        await apiRequest("/tarefas", {
            method: "POST",
            body: JSON.stringify(dados)
        })

        formTarefa.reset()
        window.location.hash = ""
        await carregarTarefas()

    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
})

const formEditar = document.getElementById("form-editar")

formEditar.addEventListener("submit", async (event) => {
    event.preventDefault()

    const dados = {
        titulo: document.getElementById("editar_titulo").value.trim(),
        descricao: document.getElementById("editar_descricao").value || null,
        prioridade: document.getElementById("editar_prioridade").value,
        data_prazo: document.getElementById("editar_prazo").value || null
    }

    try {
        await apiRequest(`/tarefas/${tarefaEditandoId}`, {
            method: "PUT",
            body: JSON.stringify(dados)
        })

        window.location.hash = ""
        await carregarTarefas()

    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
})

const formStatus = document.getElementById("form-status")

formStatus.addEventListener("submit", async (event) => {
    event.preventDefault()

    const status = document.getElementById("status").value

    const tarefa = tarefas.find(item => item.id === tarefaStatusId)

    const hoje = new Date().toLocaleDateString("sv-SE")

    const prazoVencido = tarefa.data_prazo && tarefa.data_prazo < hoje

    if (prazoVencido && tarefa.status === "Pendente" && status !== "Pendente") {
    window.location.hash = "confirmar-prazo"
    return
    }

    try {
        await apiRequest(`/tarefas/${tarefaStatusId}`, { 
                method: "PUT",
                body: JSON.stringify({ status })
            })

        window.location.hash = ""
        await carregarTarefas()

    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
})

async function editarTarefa(id) {
    const tarefa = tarefas.find(item => item.id === id)
    document.querySelectorAll(".menu-opcoes[open]").forEach(menu => menu.removeAttribute("open"))

    if (!tarefa) return

    tarefaEditandoId = id

    document.getElementById("editar_titulo").value = tarefa.titulo
    document.getElementById("editar_descricao").value = tarefa.descricao || ""
    document.getElementById("editar_prioridade").value = tarefa.prioridade
    document.getElementById("editar_prazo").value = tarefa.data_prazo || ""

    window.location.hash = "editar-tarefa"
}

async function alterarStatus(id) {
    const tarefa = tarefas.find(item => item.id === id)

    if (!tarefa) return

    document.querySelectorAll(".menu-opcoes[open]").forEach(menu => menu.removeAttribute("open"))

    tarefaStatusId = id

    document.getElementById("status").value = tarefa.status

    window.location.hash = "trocar-status"
}

let tarefaExclusaoId = null

function excluirTarefa(id) {
    tarefaExclusaoId = id
    document.querySelectorAll(".menu-opcoes[open]").forEach(menu => menu.removeAttribute("open"))

    window.location.hash = "confirmar-exclusao"
}

document.querySelectorAll(".cancelar-modal").forEach(botao => {
    botao.addEventListener("click", () => {
        window.location.hash = ""
    })
})

document.getElementById("confirmar-prazo-btn").addEventListener("click", async () => {
    const status = document.getElementById("status").value

    try {
        await apiRequest(
            `/tarefas/${tarefaStatusId}?confirmar_prazo_vencido=true`,
            {
                method: "PUT",
                body: JSON.stringify({ status })
            }
        )

        window.location.hash = ""
        await carregarTarefas()

    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
})

document.getElementById("cancelar-prazo").addEventListener("click", () => {
    window.location.hash = ""
})

document.getElementById("cancelar-exclusao").addEventListener("click", () => {
    window.location.hash = ""
})

document.getElementById("confirmar-exclusao-btn").addEventListener("click", async () => {
    try {
        await apiRequest(`/tarefas/${tarefaExclusaoId}`, {
            method: "DELETE"
        })

        window.location.hash = ""
        await carregarTarefas()

    } catch (erro) {
        if (erro.message !== "Sessão expirada") alert(erro.message)
    }
})

carregarTarefas()