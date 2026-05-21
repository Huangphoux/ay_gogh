from dotenv import dotenv_values

config = dotenv_values(".env")

is_debug = int(config["DEBUG"]) if config["DEBUG"] in ("0", "1") else False
whose_test = config["TEST"]