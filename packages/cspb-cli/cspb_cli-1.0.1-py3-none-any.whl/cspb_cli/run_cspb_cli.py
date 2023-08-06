#!/bin/python3
# Copyright 2020 Gerard L. Muir 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and or sell
#  copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.

##################
#
# Package Entry point to run the Cluster System Power Board Command Line Interface
# from the pip installed package.
#
##################

import getopt
import sys
try:
    from cspb_cli import cspb_cli # This import is for the pip installed cspb_cli package.
except ImportError:
    import cspb_cli # This import is for local non-packaged use.
    
def run_cli():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"v")
    except getopt.GetoptError:
        print('run_cspb_cli.py -v')
        sys.exit(2)
    
    app = cspb_cli.pb_cli(opts)
    app.cmdloop()
            
if __name__ == '__main__':
    run_cli()
