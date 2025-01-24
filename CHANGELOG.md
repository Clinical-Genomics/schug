# Change Log

# [1.9]
### Changed
- Added retry logic to stream_resource to handle failed chunk downloads with a configurable number of attempts and error handling.
- Commented out in the code all endpoints that are not yet functioning.

# [1.8]
### Changed
- Use custom issue and pull request templates in this repository
- Remove old code once used for downloading data from Ensembl
### Fixed
- Do not include `[success]` lines in the streamed outfiles: genes, transcripts and exons

# [1.7]
### Changed
- Do not download duplicated lines from Ensembl BioMart
- Update Python version to v3.12 in Dockerfile
- Update Python version in pyproject.toml
### Fixed
- Download data from Ensembl BioMart chromosome-wise, to avoid missing exons, for instance (see issue #74)

# [1.6.2]
### Fixed
- Some exons are missing when downloading build 38 data using Ensembl v.113 (Oct 2024). Using v.112 (May 2024) until the problem is fixed. Build 37 not affected.

# [1.6.1]
### Fixed
- Security issue related to starlette version by updating fastapi, starlette and some dependencies
- Updated urlib to v.2.2.3 to address the `urllib3's Proxy-Authorization request header isn't stripped during cross-origin redirects` issue
- Updated certifi to v.2024.7.4 to address the `Certifi removes GLOBALTRUST root certificate` issue

# [1.6]
### Changed
- Updated a number of libraries to address security alerts

## [1.5.1]
### Fixed
- Revert to python 3.8 in Dockerfile to avoid `RuntimeError: can't start new thread` issue

## [1.5]
### Changed
- Updated version of external images used in GitHub actions
- Updated Python version to v3.11 in tests GitHub action
- Removed pytest from the package dependencies
### Fixed
- Converted deprecated Pydantic validators and Config into Pydantic 2 format

## [1.4]
### Changed
- Updated Pydantic(^2.5.2) library and other dependencies
- Support Python>=3.8

## [1.3]
### Fixed
- Typo in instructions to download genes in README document
### Changed
- Code formatted with black and black check GitHub action
- Renamed `schug.load.ensembl.fetch_ensembl_exon_lines` function to `schug.load.ensembl.fetch_ensembl_exons`
- Upgraded Python version from 3.8 to 3.11 in Dockerfile
- Updated several python libraries in poetry.lock

## [1.2]
### Added
- Include also `mane_plus_clinical` and `mane_select` columns in transcripts file downloaded from Ensembl
### Changed
- Updated Uvicorn library
- Accept also `GRCh37` and `GRCh38` as build values when downloading resources

## [1.1]
### Changed
- Move the `schug` directory up in root dir folder
### Fixed
- Use a memory database as default database in demo instance
- Issues flagged by SonarCloud
- `Publish to PyPI` GitHub action

## [1.0.0]
### Added
- Endpoint to Ensembl genes download
- Endpoint to Ensembl transcripts download
- Endpoint to Ensembl exons download
- Dockerfile and docker-compose files
- Push to Docker Hub -prod and stage- GitHub actions
- Publish to PyPI GitHub actions
- Run tests GitHub action
- CHANGELOG file
### Changed
- Run the app with Python>=3.8
### Fixed
- Typing errors in `fetch_ensembl_exons` and `fetch_genes_to_hpo_to_disease` that prevented the app from starting
