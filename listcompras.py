
import streamlit as st
import sqlite3
import pandas as pd

# Conexão com o banco de dados SQLite
def create_connection():
    conn = sqlite3.connect('compras.db')
    return conn

# Criar a tabela se não existir
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lista_compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        comprado BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

# Adicionar item à lista
def add_item(item, quantidade, unidade):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lista_compras (item, quantidade, unidade) VALUES (?, ?, ?)', (item, quantidade, unidade))
    conn.commit()
    conn.close()

# Obter todos os itens da lista
def get_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lista_compras')
    items = cursor.fetchall()
    conn.close()
    return items

# Excluir item da lista
def delete_item(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lista_compras WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Excluir todos os itens da lista
def delete_all_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lista_compras')
    conn.commit()
    conn.close()

# Marcar item como comprado
def mark_as_purchased(item_id, purchased):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE lista_compras SET comprado = ? WHERE id = ?', (purchased, item_id))
    conn.commit()
    conn.close()

# Inicializar a aplicação
create_table()

st.title("Lista de Compras")

# Formulário para adicionar um item
item = st.text_input("Digite o item que deseja adicionar:")
quantidade = st.number_input("Digite a quantidade:", min_value=1)
unidade = st.selectbox("Selecione a unidade:", ["quilo", "litro", "unidade"])
if st.button("Adicionar"):
    if item:
        add_item(item, quantidade, unidade)
        st.success(f"'{quantidade} {unidade} de {item}' adicionado à lista!")
    else:
        st.warning("Por favor, insira um item.")

# Exibir itens da lista
st.subheader("Itens na lista de compras:")
items = get_items()
if items:
    items_df = pd.DataFrame(items, columns=["ID", "Item", "Quantidade", "Unidade", "Comprado"])
    items_df["Comprado"] = items_df["Comprado"].apply(lambda x: "✔" if x else "❌")
    st.table(items_df)

    # Opção para marcar item como comprado ou excluir um item
    item_to_update = st.number_input("Digite o ID do item a ser atualizado:", min_value=1, max_value=len(items))
    if st.button("Marcar como comprado"):
        mark_as_purchased(item_to_update, True)
        st.success(f"Item com ID {item_to_update} marcado como comprado!")
    if st.button("Excluir"):
        delete_item(item_to_update)
        st.success(f"Item com ID {item_to_update} excluído!")
    
    # Opção para excluir todos os itens
    if st.button("Excluir todos os itens"):
        delete_all_items()
        st.success("Todos os itens foram excluídos!")
else:
    st.info("A lista de compras está vazia.")