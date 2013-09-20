#!/bin/sh
jekyll --server --base-url "" &
sleep 1
firefox 127.0.0.1:4000 &
