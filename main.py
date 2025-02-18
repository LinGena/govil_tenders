from dotenv import load_dotenv
import schedule
from parsers.gov_il.parser import ParseGovIl
from utils.logger import Logger
import time

load_dotenv(dotenv_path='.env',override=True)

logger = Logger().get_logger(__name__)

def main(count_try:int = 0):
    if count_try == 0:
        start_parse = time.time()
        print(f'Start parser at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_parse))}')
    if count_try > 2:
        print('3 attempts failed')
        return None
    try:
        status = ParseGovIl().run()
        if not status:
            return main(count_try+1)
    except Exception as ex:
        logger.error(ex)
    end_parse = time.time()
    duration = end_parse - start_parse
    print(f'Finish parser at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_parse))}')
    print(f'Total execution time: {duration:.2f} seconds')

if __name__ == "__main__":
    main()
    schedule.every(5).hours.do(main)
    while True:
        schedule.run_pending()

    