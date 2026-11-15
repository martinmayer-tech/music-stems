# Grep the tests before you move a file

Before a step moves or renames a source file, grep every test folder for its old path. Run `grep -rn "{old path}" src/*/tests ravintio-zero/tests`. Update each match in the same commit as the move.

The tests under `src/*/tests/` read source files by path. A move breaks them with no compile error.
