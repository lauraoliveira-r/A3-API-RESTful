const API_URL = "http://127.0.0.1:8000/produtos/";

async function fetchProdutos() {
    const response = await fetch(API_URL);
    const produtos = await response.json();
    renderProdutos(produtos);
}

async function criarProduto(produto) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(produto),
        });

        if (!response.ok) {
            const error = await response.json();
            console.error("Erro ao criar produto:", error);
            return;
        }

        fetchProdutos();
    } catch (error) {
        console.error("Erro na requisição:", error);
    }
}

async function deletarProduto(id) {
    await fetch(`${API_URL}${id}`, {
        method: "DELETE",
    });
    fetchProdutos();
}

function renderProdutos(produtos) {
    const produtosList = document.getElementById("produtos");
    produtosList.innerHTML = "";
    produtos.forEach((produto) => {
        const li = document.createElement("li");
        li.textContent = `${produto.nome} - R$ ${produto.preco.toFixed(2)}: ${produto.descricao}`;
        const btn = document.createElement("button");
        btn.textContent = "Deletar";
        btn.onclick = () => deletarProduto(produto.id);
        li.appendChild(btn);
        produtosList.appendChild(li);
    });
}

// Adicionar produto via formulário
document.getElementById("product-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const nome = document.getElementById("nome").value;
    const preco = parseFloat(document.getElementById("preco").value);
    const descricao = document.getElementById("descricao").value;

    const produto = { nome, preco, descricao };
    criarProduto(produto);

    // Limpar formulário
    document.getElementById("product-form").reset();
});

// Inicializar a lista de produtos
fetchProdutos();
