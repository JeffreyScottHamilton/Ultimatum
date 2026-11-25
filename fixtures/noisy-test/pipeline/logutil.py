import warnings


def log(stage, msg):
    print(f"[pipeline:{stage}] {msg}")


def legacy(name):
    warnings.warn(f"{name} is deprecated and will be removed in 2.0", DeprecationWarning, stacklevel=3)
