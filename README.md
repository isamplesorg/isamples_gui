# isamples_gui
Repository for the iSamples GUI app
## Check out the code
1. `git clone git@github.com:isamplesorg/isamples_gui.git`
2. `git submodule update --init --recursive` (this one may need to be executed multiple times as isamples_frictionless gets updates)
### Setting up the environment
1. `mkvirtualenv isamples_gui` or `workon isamples_gui`
2. poetry install
### Building the app on macOS
`python setup.py py2app`
### Building the app on Windows
`python setup.py py2exe` (Danny's best guess -- we still need to add this to the project dependencies)
