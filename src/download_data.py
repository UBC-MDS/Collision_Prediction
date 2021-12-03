
# author: MDS-2021-22 block3 group21
# date: 2021-11-19

"""Downloads data as a csv file from online to a local filepath via a URL.
Usage: download_data.py --url=<url> --filepath=<filepath> 
 
Options:
--url=<url>             URL from where to download the data (must be in standard csv format)
--filepath=<filepath>   Path (including filename) of where to store the csv file locally
"""

import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def main(url, filepath):
    data = pd.read_csv(url, header=None)
    
    # Test if we have the given filepath in the directory, if not, create one.
    try:
        data.to_csv(filepath, index=False)
    except:
        os.makedirs(os.path.dirname(filepath))
        data.to_csv(filepath, index=False)

# Test input data type
assert type(opt["--url"]) == str, "The data type of url should be string."
assert type(opt["--filepath"]) == str, "The data type of url should be string."
        
if __name__ == "__main__":
    main(opt["--url"], opt["--filepath"])
    
