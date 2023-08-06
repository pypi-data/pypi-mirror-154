import requests
import pandas as pd
import json
from multiprocessing import Pool
import itertools
from .parsers import parse_final_domain

__title__ = "jao-py"
__version__ = "0.3.0"
__author__ = "Frank Boerman"
__license__ = "MIT"


class JaoPublicationToolClient:
    BASEURL = "https://publicationtool.jao.eu/core/api/core/"

    def __init__(self, api_key: str = None):
        self.s = requests.Session()
        self.s.headers.update({
            'user-agent': 'jao-py (github.com/fboerman/jao-py)'
        })

        if api_key is not None:
            self.s.headers.update({
                'Authorization': 'Bearer ' + api_key
            })

    def _starmap_pull(self, url, params, keyname=None):
        r = self.s.get(url, params=params)
        r.raise_for_status()
        if keyname is not None:
            return r.json()[keyname]
        else:
            return r.json()

    def query_final_domain(self, mtu: pd.Timestamp, presolved: bool = None, cne: str = None, co: str = None,
                           urls_only: bool = False) -> list:
        if type(mtu) != pd.Timestamp:
            raise Exception('Please use a timezoned pandas Timestamp object for mtu')
        if mtu.tzinfo is None:
            raise Exception('Please use a timezoned pandas Timestamp object for mtu')
        mtu = mtu.tz_convert('UTC')
        if cne is not None or co is not None or bool is not None:
            filter = {
                'cneName': "" if cne is None else cne,
                'contingency': "" if co is None else co,
                'presolved': presolved
            }
        else:
            filter = None

        # first do a call with zero retrieved data to know how much data is available, then pull all at once
        r = self.s.get(self.BASEURL + "finalComputation/index", params={
            'date': mtu.isoformat(),
            'search': json.dumps(filter),
            'skip': 0,
            'take': 0
        })
        r.raise_for_status()
        # now do new call with all data requested
        # jao servers are not great returning it all at once, but they let you choose your own pagination
        # lets go for chunks of 5000, arbitrarily chosen

        total_num_data = r.json()['totalRowsWithFilter']
        args = []
        for i in range(0, total_num_data, 5000):
            args.append((self.BASEURL + "finalComputation/index", {
                'date': mtu.isoformat(),
                'search': json.dumps(filter),
                'skip': i,
                'take': 5000
            }, 'data'))

        if urls_only:
            return args

        with Pool() as pool:
            results = pool.starmap(self._starmap_pull, args)

        return list(itertools.chain(*results))


class JaoPublicationToolPandasClient(JaoPublicationToolClient):
    def query_final_domain(self, mtu: pd.Timestamp, presolved: bool = None, cne: str = None, co: str = None) -> pd.DataFrame:
        return parse_final_domain(
            super().query_final_domain(mtu=mtu, presolved=presolved, cne=cne, co=co)
        )

