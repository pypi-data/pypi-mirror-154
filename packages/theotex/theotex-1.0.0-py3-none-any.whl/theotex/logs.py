import logging

debug = logging.getLogger("debug")
debug.setLevel(logging.DEBUG)

debug_handler = logging.StreamHandler()
debug_formatter = logging.Formatter("%(asctime)s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")
debug_handler.setFormatter(debug_formatter)
debug.addHandler(debug_handler)
