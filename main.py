from dotenv import load_dotenv
from parsers.gov_il.parser import ParseGovIl

load_dotenv(dotenv_path='.env',override=True)


def main():
    ParseGovIl().run()
  
if __name__ == "__main__":
    main()

    