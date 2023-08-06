# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## [0.1.6] - 2022-06-10

### Added

- Enable use of untested strategies with new flag and user warning
- Update various dependency minimum versions
- Minor example logging update

### Fixed
- minor privacy policy link update
- bump omegaconf version requirement due to omegaconf bug

### Changed

### Deprecated


## [0.1.5] - 2022-06-02

### Added

- Bumped latest tested PL patch version to 1.6.4
- Added basic notebook-based example tests a new ipynb-specific extra
- Updated docker definitions
- Extended multi-gpu testing to include both oldest and latest supported PyTorch versions
- Enhanced requirements parsing functionality
### Fixed
- cleaned up acknowledged warnings in multi-gpu example testing
### Changed

### Deprecated

## [0.1.4] - 2022-05-24

### Added

- LR scheduler reinitialization functionality ([#2](https://github.com/speediedan/finetuning-scheduler/pull/2))
- advanced usage documentation
- advanced scheduling examples
- notebook-based tutorial link
- enhanced cli-based example hparam logging among other code clarifications

### Fixed

- addressed URI length limit for custom badge
- allow new deberta fast tokenizer conversion warning for transformers >= 4.19
### Changed

### Deprecated

## [0.1.3] - 2022-05-04

### Added

-

### Changed

- bumped latest tested PL patch version to 1.6.3
### Fixed

-
### Deprecated

-

## [0.1.2] - 2022-04-27

### Added

- added multiple badges (docker, conda, zenodo)
- added build status matrix to readme

### Changed

- bumped latest tested PL patch version to 1.6.2
- updated citation cff configuration to include all version metadata
- removed tag-based trigger for azure-pipelines multi-gpu job

### Fixed

-
### Deprecated

-

## [0.1.1] - 2022-04-15

### Added

- added conda-forge package
- added docker release and pypi workflows
- additional badges for readme, testing enhancements for oldest/newest pl patch versions

### Changed

- bumped latest tested PL patch version to 1.6.1, CLI example depends on PL logger fix ([#12609](https://github.com/PyTorchLightning/pytorch-lightning/pull/12609))

### Deprecated

-

### Fixed

- Addressed version prefix issue with readme transformation for pypi


## [0.1.0] - 2022-04-07

### Added

- None (initial release)

### Changed

- None (initial release)

### Deprecated

- None (initial release)

### Fixed

- None (initial release)
