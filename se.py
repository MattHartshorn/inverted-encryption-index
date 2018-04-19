from src.commander import Commander
from src.add import AddCommand
from src.search import SearchCommand
from src.token import TokenCommand
from src.keygen import KeyGenCommand

def main():
    Commander(KeyGenCommand, AddCommand, TokenCommand, SearchCommand).run()

if __name__ == "__main__":
    main()
