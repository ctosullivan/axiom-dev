"""Allows `python3 -m axiom_validator <paths...>` to run the CLI.

The pre-refactor monolithic file supported `python3 src/axiom_validator.py
<paths...>`; as a package, the equivalent is `python3 -m axiom_validator
<paths...>` with `src/` on PYTHONPATH. This is a CLI-invocation detail,
not a behaviour the contract or the protected tests fix — see
planning/phase-01-foundation.md Stage 1.4.
"""
import sys

from . import main

if __name__ == "__main__":
    sys.exit(main())
