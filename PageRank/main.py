import crawler
import page_rank
import sys
import visualizer

argument = sys.argv[1]
if argument == 'crawler':
    crawler.run(sys.argv[2], 3)
elif argument == 'page_rank':
    page_rank.run()
elif argument == 'transition_matrix':
    print(page_rank.build_transition_matrix()[0])
elif argument == 'graph':
    visualizer.run()