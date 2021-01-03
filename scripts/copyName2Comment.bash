#!/usr/bin/env bash

exiftool "-Comment<${FileName;s/\..*//}" .
