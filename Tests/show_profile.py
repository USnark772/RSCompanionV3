from pstats import Stats, SortKey
from Debugging_Profiling.profile_defs import profile_outdir

search_str = "RSCompanion"
# search_str = "cam_controller"
# search_str = "cam_view"
# search_str = "asyncio"
# search_str = "logging"
# search_str = "site-packages"
# search_str = None

top_num_to_show = 30
# top_num_to_show = None

filename = profile_outdir + 'Cam_0.prof'
stats = Stats(filename)
stats.sort_stats(SortKey.CALLS)
if search_str is not None and top_num_to_show is not None:
    stats.print_stats(search_str, top_num_to_show)
elif search_str is not None:
    stats.print_stats(search_str)
elif top_num_to_show is not None:
    stats.print_stats(top_num_to_show)
else:
    stats.print_stats()
