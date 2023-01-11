# v0.0.5

- Message signing and signature verification
- Fixes to help text and parameters specs
- Output chainId and networkId from `aut node info`
- Output XTN quantities as units of Auton (instead of Wei)

# v0.0.4

- New token command for queries and operations on ERC20 tokens (including Newton and Liquid Newton).
- Value is now specified in WHOLE TOKEN UNITS (Auton, Newton, etc) unless a unit suffix is given.  E.g.
  - For Auton: `1gwei` still represents 1 GWei, but `1` now refers to 1 Auton instead.  Decimals can still be used, so `1finney` is the same as `0.001`.
  - For tokens (including Newton), only decimals (e.g. 0.001) can be used.  Maximum precision is determined by the token, and can be queried with `aut token decimals`. See --help text for details.
- Token balances are now always output in units of whole tokens, with decimals used to represent fractional parts (e.g. 1.01).
- Auton balances are still output in Wei.  This inconsistency will be addressed in a future release.
- Support for `attoton` units.
- Entropy for new accounts can be given via a file.
- Show enode of the attached node in `aut node info`
- Small updates to command help text.

# v0.0.3

- Small fixes for command line parameters

# v0.0.2

- Cleaned up some parameter handling
- Improved start-up times
- Added `account import-private-key` command

# v0.0.1

- First revision of the tool with functionality covering most Autonity operations.
