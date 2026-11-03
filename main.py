"""Gerenciador de tarefas simples (CRUD) em Python com SQLite."""
import sqlite3

DB_NAME = "tarefas.db"


def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tarefas ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "titulo TEXT NOT NULL, "
        "concluida INTEGER NOT NULL DEFAULT 0)"
    )
    return conn


def adicionar(conn, titulo):
    conn.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
    conn.commit()


def listar(conn):
    return conn.execute("SELECT id, titulo, concluida FROM tarefas").fetchall()


def concluir(conn, id_tarefa):
    cur = conn.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))
    conn.commit()
    return cur.rowcount > 0


def remover(conn, id_tarefa):
    cur = conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()
    return cur.rowcount > 0


def mostrar_menu():
    print("\n=== Gerenciador de Tarefas ===")
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("3 - Concluir tarefa")
    print("4 - Remover tarefa")
    print("0 - Sair")


def main():
    conn = conectar()
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título da tarefa: ").strip()
            if titulo:
                adicionar(conn, titulo)
                print("Tarefa adicionada!")
            else:
                print("O título não pode ser vazio.")
        elif opcao == "2":
            tarefas = listar(conn)
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            for id_tarefa, titulo, concluida in tarefas:
                marca = "[x]" if concluida else "[ ]"
                print(f"{id_tarefa}. {marca} {titulo}")
        elif opcao in ("3", "4"):
            try:
                id_tarefa = int(input("ID da tarefa: "))
            except ValueError:
                print("ID inválido.")
                continue
            acao = concluir if opcao == "3" else remover
            print("Feito!" if acao(conn, id_tarefa) else "Tarefa não encontrada.")
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

    conn.close()


if __name__ == "__main__":
    main()
