import sys
import logging
from zipfile import ZipFile
import itertools
from arrow import utcnow
from multiprocessing import Pool
import os

source_file = './data/five.zip'
pw_chars = 'abcdefghijklmnopqrstuvwxyz'

# logging
log_to_file = False
logfile_name = 'guesser.log'
display_data_on_validation_error = False

# Create logger
logger = logging.getLogger('guesser')
logger.setLevel(logging.INFO)

# Create STDERR handler
stderr_handler = logging.StreamHandler(sys.stderr)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
stderr_handler.setFormatter(formatter)

# Set STDERR handler
logger.handlers = [stderr_handler]

# FILE handler
if log_to_file is True:
    fhandler = logging.FileHandler(filename=logfile_name, mode='a')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)


def get_guesses(possible_chars):
    logger.info("starting to get pw...")
    for x in range(1, len(possible_chars) + 1):
        res = itertools.permutations(possible_chars, x)
        for guess in res:
            yield guess


def crack():
    with ZipFile(source_file) as zf:
        guesses = get_guesses(pw_chars)
        for guess in guesses:
            pw = ''.join(guess)
            b = pw.encode('utf-8')
            try:
                logger.info("guessing {0}".format(pw))
                zf.extractall(pwd=b)
                logger.info("the password is {0}".format(pw))
                break
            except Exception:
                pass
        return pw
computing_time = 0
start_time = utcnow()

pool = Pool(os.cpu_count())
pw = pool.apply(crack)[0]

end_time = utcnow()
time_elapsed = (end_time - start_time).total_seconds() * 1000  # milliseconds
computing_time += time_elapsed

logger.info("tha took {0} ms".format(computing_time))
