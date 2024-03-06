# Changelog

## [v0.4.0] - 2024-03-06

### Changed

- Support the Autonity Sumida protocol ([#146](https://github.com/autonity/aut/issues/146))
- Require consensus key for validator registration ([`380b6be`](https://github.com/autonity/aut/commit/380b6be))

### Added

- Support Python 3.12 ([#138](https://github.com/autonity/aut/issues/138))

### Fixed

- Fix `AssertionError` when `contract call` returns multiple values ([#127](https://github.com/autonity/aut/issues/127))
- Fix `TypeError` when `contract call` returns bytes values ([#141](https://github.com/autonity/aut/issues/141))

## [v0.3.0] - 2024-01-15

### Changed

- Require `oracle` address for validator registration ([`b7cf048`](https://github.com/autonity/aut/commit/b7cf048))

### Added

- Add commands for new Autonity Contract protocol functions ([`d63a425`](https://github.com/autonity/aut/commit/d63a425))
- Support the `-h` help flag in addition to `--help` ([`84ab6a1`](https://github.com/autonity/aut/commit/84ab6a1))

### Fixed

- Fix compatibility with Autonity Barada ([`f424804`](https://github.com/autonity/aut/commit/f424804))
- Fix potential crash when listing accounts ([`1886121`](https://github.com/autonity/aut/commit/1886121))
- Fix startup crash due to `ModuleNotFoundError` from eth_rlp ([#137](https://github.com/autonity/aut/issues/137))

[v0.4.0]: https://github.com/autonity/aut/releases/tag/v0.4.0
[v0.3.0]: https://github.com/autonity/aut/releases/tag/v0.3.0
