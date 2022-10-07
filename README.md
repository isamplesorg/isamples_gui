# isamples_gui
Repository for the iSamples GUI app
## Check out the code
1. `git clone git@github.com:isamplesorg/isamples_gui.git`
2. `git submodule update --init --recursive` (this one may need to be executed multiple times as isamples_frictionless gets updates)
## Setting the resource path to find the schema.json
By default, the app will try to use the built-in `isamples_simple_schema.json` when constructing the frictionless
package.  In order for the app to find it, it will look in the directory specified in the `RESOURCEPATH` environment variable.  When the
application bundle is constructed using `py2app`, this will be the `Resources` directory in the application bundle.
However, if you are running in an IDE, you will need to explicitly set the environment variable to the directory that
has the `isamples_simple_schema.json` for this to work properly.  Of course, you can also manually choose your own
frictionless schema file when running the app.
### Setting up the environment
1. `mkvirtualenv isamples_gui` or `workon isamples_gui`
2. poetry install
### Building the app on macOS
`python setup.py py2app`
### Building the app on Windows
1. Configuring dependency : update the `python` and `pyinstaller` dependency.
2. Download the [frictionless library](https://github.com/frictionlessdata/framework/releases/tag/v4.40.8/) and unzip the `frictionless/` directory to the project root directory. This folder and other necessary static files will be copied manually during the build process as we can see in the  `isamplesGUI.spec` :
```
datas=[
        ('isamples_frictionless/isamples_frictionless/isamples_simple_schema.json','.'),
        ('isampleslogo.ico','.'),
        ('frictionless','./frictionless')
    ],
```
3. Build the app by executing the following command `pyinstaller iSamplesGUI.spec`.