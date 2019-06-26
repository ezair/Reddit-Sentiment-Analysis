'''
Author:	Eric Zair
File:	linter.py
Decription:	Very simple script that is used to check all litner for every python file in
			this project.
			To run with docker, run the following command:
				docker-compose run app python3 linter.py
'''
import subprocess
subprocess.call('pylint_runner')
