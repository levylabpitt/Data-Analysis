#!/usr/bin/env python

import yaml

with open("test.yaml", 'r') as stream:
    output = yaml.load(stream)
