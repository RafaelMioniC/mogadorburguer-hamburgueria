from flask import Flask, render_template, request, redirect, session, url_for
import pymysql

app = Flask(__name__)

app.secret_key = "senha"

conexao = pymysql.connect(
    host="localhost",
    user="local",
    password="mogadorburguer",
    database="hamburgueria"
)

@app.route("/")
def home():

    carrinho = session.get("carrinho", [])

    total_itens = sum(item["quantidade"] for item in carrinho)

    return render_template(
        "index.html",
        total_itens=total_itens
    )

@app.route("/adicionar_carrinho", methods=["POST"])
def adicionar_carrinho():

    dados = request.get_json()

    lanche_id = int(dados["lanche_id"])
    produto = dados["produto"]
    preco = float(dados["preco"])

    if "carrinho" not in session:
        session["carrinho"] = []

    carrinho = session["carrinho"]

    # 🔥 verifica se o item já existe
    for item in carrinho:

        if item["lanche_id"] == lanche_id:

            item["quantidade"] += 1

            session["carrinho"] = carrinho

            total = sum(
                i["quantidade"]
                for i in carrinho
            )

            return {
                "mensagem": "Quantidade atualizada!",
                "total": total
            }

    # 🔥 adiciona novo item
    carrinho.append({
        "lanche_id": lanche_id,
        "produto": produto,
        "preco": preco,
        "quantidade": 1
    })

    session["carrinho"] = carrinho

    total = sum(
        i["quantidade"]
        for i in carrinho
    )

    return {
        "mensagem": "Produto adicionado!",
        "total": total
    }
@app.route("/carrinho")
def carrinho():

    carrinho = session.get("carrinho", [])

    total = sum(
    item["preco"] * item["quantidade"]
    for item in carrinho
)

    return render_template(
        "carrinho.html",
        carrinho = carrinho,
        total = total
    )

@app.route("/total_itens")
def total_itens():

    carrinho = session.get("carrinho", [])

    total = sum(
        item["quantidade"]
        for item in carrinho
    )

    return {"total": total}

@app.route("/limpar_carrinho")
def limpar_carrinho():

    session.pop("carrinho", None)

    return redirect("/")

@app.route("/finalizar", methods=["POST"])
def finalizar():

    nome = request.form.get("nome")
    cep = request.form.get("cep")
    pagamento = request.form.get("pagamento")

    carrinho = session.get("carrinho", [])

    if not carrinho:
        return redirect("/carrinho")

    cursor = conexao.cursor()

    # Cliente
    sql = """
    INSERT INTO cliente(cliente_nome, cliente_cep)
    VALUES(%s, %s)
    """

    cursor.execute(sql, (nome, cep))

    cliente_id = cursor.lastrowid

    # Calcula total
    total = 0

    for item in carrinho:

        sql = """
        SELECT lanche_preco
        FROM lanches
        WHERE lanche_id = %s
        """

        cursor.execute(sql, (item["lanche_id"],))

        preco = cursor.fetchone()[0]

        total += preco * item["quantidade"]

    total = round(total, 2)

    # Pedido
    sql = """
    INSERT INTO pedido
    (cliente_id, pedido_preco, ped_meio)
    VALUES(%s, %s, %s)
    """

    cursor.execute(sql, (
        cliente_id,
        total,
        pagamento
    ))

    pedido_id = cursor.lastrowid

    # Itens do pedido
    sql = """
    INSERT INTO pedido_item
    (pedido_id, lanche_id, item_quantidade)
    VALUES(%s, %s, %s)
    """

    for item in carrinho:

        cursor.execute(sql, (
            pedido_id,
            item["lanche_id"],
            item["quantidade"]
        ))

    conexao.commit()

    session.pop("carrinho", None)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)