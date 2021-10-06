# How is everything linked?

In short the order of reliability is the following:


1. HGNC
2. Ensembl
3. The rest

It is a challenge to merge information from multiple sources and there needs to be some rules that defines the "truth".
We use [hgnc] as the most reliable source since this is a manually curated database.
HGNC is promise that each gene have a unique gene identifier in the form if a HGNC ID, Schug also use this as the primary
identifier of a gene since symbols tend to vary over time. HGNC does also provide a stable gene symbol for each gene.

## Gene coordinates

HGNC do not provide a mapping from gene id to coordinates so schug use Ensembl as the resource for location of genes.
Mapping from Ensembl Gene ID (ENSG) to HGNC ID is done by Ensembl.

## Genes to transcripts

Genes are linked to transcripts in Ensembl, Shoug only consider ensembl transcripts

## Transcripts and exons

Transcript and exon definitions are taken from Ensembl only, also the linking between transcripts and exons are 
done by ensembl.

## Primary transcript

The primary transcript is decided by hgnc and is expressed in NM-form

## Transcript identifiers

Transcripts, just like genes, have different nomenclatures. We use the ensembl version to describe location of the 
transcripts. For naming schug will use the refseq nomenclature first hand. This is the naming starting with `NM`. 


[hgnc]: https://www.genenames.org