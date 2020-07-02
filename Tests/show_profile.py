from pstats import Stats, SortKey
from RSCompanionAsync.Model.app_defs import profile_outpath

filename = profile_outpath + 'imgworker_796.prof'
stats = Stats(filename)
stats.sort_stats('ncalls')
# stats.sort_stats(SortKey.CUMULATIVE)
# stats.print_stats("RSCompanion")  # Only show project files.
# stats.print_stats(20)  # Show top 20 lines.
# stats.print_stats("RSCompanion", 20)  # Show top 20 lines of project files.
# stats.print_stats(20, "RSCompanion")  # Show only project files of the top 20 lines.
stats.print_stats()

