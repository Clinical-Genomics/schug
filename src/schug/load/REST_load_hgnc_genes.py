import json
from typing import List
from urllib.parse import urlencode

from pydantic import BaseModel
from urllib.request import urlopen, Request

hgnc_server: str = "http://rest.genenames.org/"


class REST_api_fetcher(BaseModel):
    hgnc_server: str = "http://rest.genenames.org"
    ensembl_38_server: str = "https://rest.ensembl.org"
    ensembl_37_server: str = "https://grch37.rest.ensembl.org"

    def REST_action(
        self, endpoint: str, server: str, headers: dict = None, params: dict = None
    ):
        if headers is None:
            headers: dict = {}
        if params:
            endpoint += "?" + urlencode(params)

        request = Request(server + endpoint, headers=headers)
        response = urlopen(request)
        content = response.read()
        if content:
            data = json.loads(content)
        return data

    def fetch_all_hgnc_genes(self) -> List[dict]:
        return self.REST_action(
            endpoint="/search/alias_symbol/*",
            server=hgnc_server,
            headers={"Accept": "application/json"},
        )["response"]["docs"]

    def fetch_ensembl_gene(self, symbol: str, server):
        return self.REST_action(
            endpoint="/lookup/symbol/homo_sapiens/" + symbol,
            server=server,
            headers={"Accept": "application/json"},
            params={"expand": 1},
        )
