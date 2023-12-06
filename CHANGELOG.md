# Change Log

## [unreleased]
### Changed
- Updated version of external images used in GitHub actions

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
