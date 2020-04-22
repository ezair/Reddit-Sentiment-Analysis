"""
@author Eric Zair
@file nltk_downloaded.py
@description    All this file does is download all required nltk packages when it is run.
                This script will be called in the 'dev_setup.sh' script so everything is
                ready for when the user runs the program.
"""
import nltk


def main():
    nltk.download()


if __name__ == '__main__':
    main()
