"""Top-level package for defi-tools."""

__author__ = """Dean Dominguez"""
__email__ = 'deanjdominguez@gmail.com'
__version__ = '0.1.0'

from os import environ

if environ.get('LOCAL', False):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
