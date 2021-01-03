#!/usr/bin/env bash

exiftool -d %Y%m%d_%H%M%S%%-c.%%e "-filename<CreateDate" .
