#!/bin/bash

#copy everything to tschinux but not files/folders starting with a dot (e.g .git)
scp -r [!.]* tschinux@shoemaker.uberspace.de:/home/tschinux/dl4g/
