#!/bin/bash

time=$(date +"%Y-%m-%d");
/usr/local/bin/python3.8 /demo/weibo_top/weibo_top.py &&
/usr/local/bin/bypy upload /demo/weibo_top/${time}.md weibo
