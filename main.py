import os
import keep_alive
from pipo_client import PipoClient

def main():
  client = PipoClient()
  client.run(os.getenv('TOKEN'))

if __name__ == "__main__":
  keep_alive.keep_alive()
  main()