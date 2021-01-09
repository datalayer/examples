#!/usr/bin/env bash

jupyter server --ServerApp.jpserver_extensions="{'simple_ext1': True}" --ServerApp.allow_origin=*
