# Global Variables to be used across processes.
# Separate file is needed to make globals accessible from different submodules.

# Global variables which need to exist in the scope of each process.
# Variables are added into this dictionary during process initialization.
multiprocess_globals = {}