async function adicionarCarrinho(lanche_id, produto, preco){

    try {
        const resposta = await fetch("/adicionar_carrinho", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                lanche_id: lanche_id,
                produto: produto,
                preco: preco
            })
        });

        const dados = await resposta.json();

        // Atualiza badge na hora
        await atualizarBadge();

        // Mensagem
        mostrarMensagem("Produto adicionado ao carrinho!");

    } catch (error) {
        console.error("Erro ao adicionar ao carrinho:", error);
        alert("Erro ao adicionar produto.");
    }
}

async function atualizarBadge(){

    try {
        const resposta = await fetch("/total_itens");
        const dados = await resposta.json();

        const badge = document.getElementById("badge");

        if (badge) {
            badge.innerText = dados.total;
        }

    } catch (error) {
        console.error("Erro ao atualizar badge:", error);
    }
}

function mostrarMensagem(texto){

    let msg = document.getElementById("mensagem");

    if (!msg) {
        msg = document.createElement("div");
        msg.id = "mensagem";
        msg.style.position = "fixed";
        msg.style.top = "20px";
        msg.style.right = "20px";
        msg.style.background = "#28a745";
        msg.style.color = "white";
        msg.style.padding = "10px 15px";
        msg.style.borderRadius = "8px";
        msg.style.zIndex = "9999";
        document.body.appendChild(msg);
    }

    msg.innerText = texto;

    setTimeout(() => {
        msg.remove();
    }, 2000);
}