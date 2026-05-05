from search import search_prompt


def main():
    ask = search_prompt()
    while True:
        try:
            q = input("PERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not q or q.lower() in {"sair", "exit", "quit"}:
            return
        print(f"RESPOSTA: {ask(q)}\n")


if __name__ == "__main__":
    main()
