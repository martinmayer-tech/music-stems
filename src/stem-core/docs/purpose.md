# stem-core: purpose

stem-core holds the two-pass separation function and the `stems` command. Step 1 adds the package skeleton only.

The service and the command line call this component. It calls `audio-separator` once step 2 adds it.

This component owns no data, so it has no data contract.
