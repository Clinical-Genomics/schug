import json
from typing import List
from urllib.parse import urlencode

from pydantic import BaseModel
from urllib.request import urlopen, Request


class rest_api_fetcher(BaseModel):
    hgnc_server: str = "https://rest.genenames.org"
    ensembl_38_server: str = "https://rest.ensembl.org"
    ensembl_37_server: str = "https://grch37.rest.ensembl.org"
    hpo_server: str = "https://hpo.jax.org"

    def rest_action(
        self,
        endpoint: str,
        server: str,
        headers: dict = None,
        params: dict = None,
        data=None,
    ):
        if headers is None:
            headers: dict = {}
        if params:
            endpoint += "?" + urlencode(params)

        request = Request(server + endpoint, headers=headers, data=data)
        response = urlopen(request)
        content = response.read()
        if content:
            data = json.loads(content)
        return data

    def search_all_hgnc_genes(self) -> List[dict]:
        return self.rest_action(
            endpoint="/search/alias_symbol/*",
            server=self.hgnc_server,
            headers={"Accept": "application/json"},
        )["response"]["docs"]

    def fetch_all_hgnc_genes(self):
        return self.rest_action(
            endpoint="/fetch/status/Approved",
            server=self.hgnc_server,
            headers={"Accept": "application/json"},
        )["response"]["docs"]

    def fetch_hgnc_gene(self, hgnc_id: str):
        return self.rest_action(
            endpoint="/fetch/hgnc_id/" + hgnc_id,
            server=self.hgnc_server,
            headers={"Accept": "application/json"},
        )["response"]["docs"]

    def fetch_ensembl_gene(self, symbol: str, server):
        return self.rest_action(
            endpoint="/lookup/id/" + symbol,
            server=server,
            headers={"Accept": "application/json"},
        )

    def fetch_multiple_ensembl_gene(self, symbols: List[str], server):
        data = json.dumps({"ids": symbols}).encode(encoding="utf-8")
        return self.rest_action(
            endpoint="/lookup/id",
            server=server,
            headers={"Accept": "application/json", "Content-type": "application/json"},
            data=data,
        )

    def fetch_hpo_gene(
        self, entrez_id: str
    ):  # TODO fix certification error for this endpoint. Maybe use the request package?
        return self.rest_action(
            endpoint="/api/hpo/gene/" + entrez_id,
            server=self.hpo_server,
            headers={"Accept": "application/json"},
        )
