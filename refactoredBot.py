from src.Configuration.Configure import Configuration
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH = range(1)

def main():
    updater, bot = Configuration().configure()



if __name__ == '__main__':
    main()