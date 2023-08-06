# Version 2.0

Released 2022-06-09

* Model:
    - New thermal model based on Arrhenius-Néel equation
    - Add ability to set all spins to 1 or -1 with init parameter
    - Add labels argument to CustomSpinIce for custom labels
    - Allow CustomSpinIce to read spin labels from table
    - Add ground option to init for Kagome
    - Add KagomeSpinIceRotated
    - Add ability to change hc with set_hc()
    - Add ability to set hc from a grid
    - Add methods for dipolar, thermal and external energy
    - Experimental CUDA support
* Documentation:
    - Brand new user guide and website!
* Encoders:
    - Rework encoder module to allow user-defined encoders with flatspin-run
    - Add phase parameter to sin/triangle/rotate based encoders
    - Add repeat to Constant and ConstantGrid encoders
    - Encoder.get_params() now returns a flat dictionary
* Datasets:
    - Add ability to filter datasets by list of values
    - Add git branch and commit to info.csv
    - Add support for functions in dataset filter
* Command-line tools:
    - flatspin-vectors and flatspin-vertices:
        - Add dark mode
        - Add ability to disable grid
        - Add peem colormap: --cmap peemX where X is a float
        - Add option to disable --grid
        - Add --dpi option
    - flatspin-run and flatspin-run-sweep:
        - Add support for time-varying parameters
        - Add support for reading params_t from file
        - Add --params-file and --sweep-file
        - Disable progress bar when run non-interactively
        - Support N-dimensional input arrays
    - Support for lists in the -i parameter
    - Add --drop-duplicates argument
    - Add --version argument
* Miscellaneous:
    - Improved vertex detection
    - Bug fixes

# Version 1.0

Released 2020-03-05

* First public release.
