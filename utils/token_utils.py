TOK_FILE = "token.txt"

def get_token() -> str:
    with open(TOK_FILE, "r") as tokfile:
        return tokfile.read().strip()
