import cProfile

# To profile a block of code:
out_path = "C:/path/filename.prof"
cp = cProfile.Profile()
cp.enable()
# Block of code to profile goes here.
cp.disable()
cp.dump_stats(out_path)


# To profile a function:
def profile_func(func_to_profile: str, out_path: str) -> None:
    # func_to_profile = 'function_name(arg1, arg2, arg3)'
    # out_path = "C:/path/filename.prof"
    cProfile.runctx(func_to_profile, globals(), locals(), out_path)
