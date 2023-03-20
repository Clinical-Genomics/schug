# Change Log

## [unreleased]
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
