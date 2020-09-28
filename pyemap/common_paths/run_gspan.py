# https://github.com/betterenvi/gSpan
# pip install gspan-mining
from gspan_mining.config import parser
from gspan_mining.main import main

args_str = '-s 10 -d False -l 5 -p False -w True graphdata.txt'
FLAGS, _ = parser.parse_known_args(args=args_str.split())

gs = main(FLAGS)

