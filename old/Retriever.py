from multiprocessing import Manager
from util import Pyswiss
from concurrent.futures import ThreadPoolExecutor
from util import fetch_keys
import random

class Retriever(object):
    """
    large scale handling of nodes with s3.
    """
    def __init__(self, n_threads=4):
        self.s3_client = Pyswiss()
        self.n_threads = n_threads

    def _fetch(self, name, d):
        """fetch object from s3 and place it in shared dict d."""
        d[name] = self.s3_client.get("pyrank", name)

    def _sample(self, size):
        entries = fetch_keys("pyrank")
        return random.sample(entries, size)

    def fetch_objects(self, size):
        """
        return dict of keys:objects
        """
        manager = Manager()
        d = manager.dict()

        keys = self._sample(size)

        with ThreadPoolExecutor(max_workers=self.n_threads) as executor:
            for k in keys:
                executor.submit(self._fetch, k, d)
        return dict(d)

    def put_objects(self, batch_dict):
        # TODO multithread
        for k, v in batch_dict.items():
            self.s3_client.put(v, bucket="pyrank", key=k)
        print("success")