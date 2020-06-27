from pstats import Stats, SortKey

filename = 'C:/RSDev/profiler_output/cam_1.prof'
stats = Stats(filename)
stats.sort_stats(SortKey.CUMULATIVE)
# stats.print_stats("image_resize")  # Only show project files.
stats.print_stats()
