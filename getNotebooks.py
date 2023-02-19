# from ensurepip import version
import logging
import pandas as pd
def script_filter(record):
        if record.name != __name__:
            return False
        return True

handler = logging.StreamHandler()
handler.filters = [script_filter]
logger = logging.getLogger(__name__)
logger.addHandler(handler)
fh = logging.FileHandler('./log/code.log', "w+")
logger.setLevel(logging.INFO)
logger.addHandler(fh)
versions_df = pd.read_csv('ntb_2020_versions.csv').drop(columns=['Unnamed: 0'])
print(versions_df.head(5))
versions_df.info()