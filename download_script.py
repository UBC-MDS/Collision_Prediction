
# author: MDS-2021-22 block3 group21
# date: 2021-11-19

"""Downloads data as a csv file from online to a local filepath via a URL.
Usage: download_script.py --url=<url> --filepath=<filepath> 
 
Options:
--url=<url>             URL from where to download the data (must be in standard csv format)
--out_file=<out_file>   Path (including filename) of where to store the csv file locally
"""

import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def main(url, filepath):
    data = pd.read_csv(url, header=None)
    try:
        data.to_csv(out_file, index=False)
    except:
        os.makedirs(os.path.dirname(filepath))
        data.to_csv(filepath, index=False)

if __name__ == "__main__":
    main(opt["--url"], opt["--filepath"])
