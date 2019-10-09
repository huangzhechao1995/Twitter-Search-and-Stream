# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 00:44:33 2019

@author: huang
"""

from argparse import ArgumentParser


def get_args():
    argparser = ArgumentParser()
    argparser.add_argument('--credential', type=str, default="credential2.txt")
    argparser.add_argument('--root', type=str, default="D:/GitHub/Twitter-Search-and-Stream")
    argparser.add_argument('--mode',type=str, default="users")
    argparser.add_argument('--db',type=str)
    argparser.add_argument('--targetfile',type=str)
    argparser.add_argument('--filetype',type=str,default='binary')
    argparser.add_argument('--start_date',type=str)
    argparser.add_argument('--date_delta',type=int, default=1)
    argparser.add_argument('--maxTweetsPerDay',type=int, default=60000)
    argparser.add_argument('--first_user',type=int, default=-1)
    argparser.add_argument('--logfilenumber',type=str, default='')
    args = argparser.parse_args()
    return args