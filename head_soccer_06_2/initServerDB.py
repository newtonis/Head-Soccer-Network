__author__ = 'newtonis'

from server.database import initDB
from server.database import serverQ

def main():
    initDB.InitDB()

if __name__ == "__main__":
    main()