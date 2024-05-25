import logging
from pathlib import Path


def init_logger(app_name: str = ""):
    if not app_name:
        app_name = __name__
    logger = logging.getLogger(app_name)
    if not logger.handlers:
        # Set ups the logger if it is not already initialised
        logger_filepath = Path.cwd() / "logfile.log"
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s-%(levelname)s: %(message)s")
        fhandler = logging.FileHandler(filename=logger_filepath, mode="a")
        fhandler.setFormatter(formatter)
        fhandler.setLevel(logging.INFO)
        chandler = logging.StreamHandler()
        chandler.setLevel(logging.INFO)
        chandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.addHandler(chandler)
        logger.info(f"Logger initialised in {logger_filepath}")
    return logger


def main():
    log = init_logger()
    log.info("success!")


if __name__ == "__main__":
    main()
