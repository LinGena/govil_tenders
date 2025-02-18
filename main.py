from dotenv import load_dotenv
import schedule
from parsers.gov_il.parser import ParseGovIl
from utils.logger import Logger

load_dotenv(dotenv_path='.env',override=True)

logger = Logger().get_logger(__name__)

def main():
    try:
        ParseGovIl().run()
    except Exception as ex:
        logger.error(ex)
  
if __name__ == "__main__":
    main()
    schedule.every(5).hours.do(main)
    while True:
        schedule.run_pending()

    