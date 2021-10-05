# Schug 

Schug :stew: is a service that gather data about genes, transcripts and exons from multiple sources and merge the 
information. There is a [REST API][rest-api] with relevant endpoints.

## Installation (development)

Make sure [poetry][poetry] is installed

```
git clone https://github.com/Clinical-Genomics/schug
cd schug
poetry install
schug setup --demo
schug serve --reload
```
Go to `http://localhost:8000/docs` and check out the API.

## What is left to do?

The basic structure is outlined and implemented, however there are many details left to implement before 
this can be used.
Some of the basic endpoints are in place but these need to be extended according to the needs of the 
users. Also the gene information needs to be completed, this will be done in a similar fashion as in 
[Scout][scout-genes].

[poetry]: https://python-poetry.org/docs/basic-usage/
[rest-api]: https://realpython.com/api-integration-in-python/
[scout-genes]: https://github.com/Clinical-Genomics/scout/blob/121e9577aaf837eadd6b0e231e0fc5f3e187b920/scout/load/setup.py#L41