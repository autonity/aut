# v0.0.4

- Value is now specified in WHOLE TOKEN UNITS (Auton, Newton, etc) unless a unit suffix is given.  E.g. `1gwei` still represents 1 GWei, but `1` now refers to 1 Auton instead.  Decimals can still be used, so `1finney` is the same as `0.001`.
- Support for `attoton` units.
- Entropy for new accounts can be given via a file.
- Small updates to command help text.

# v0.0.3

- Small fixes for command line parameters

# v0.0.2

- Cleaned up some parameter handling
- Improved start-up times
- Added `account import-private-key` command

# v0.0.1

- First revision of the tool with functionality covering most Autonity operations.
