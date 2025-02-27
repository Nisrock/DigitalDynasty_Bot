# main.py
from bot import Bot
from game import Game
from config import TOKEN

def main():
    game = Game()
    bot = Bot(TOKEN, game)
    bot.run()

if __name__ == '__main__':
    main()