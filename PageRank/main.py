import crawler
import page_rank
import sys

argument = sys.argv[1]
if argument == 'crawler':
    crawler.run(sys.argv[2], 3)
elif argument == 'page_rank':
    page_rank.run()
