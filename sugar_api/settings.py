import os
from dotenv import load_dotenv

from .helpers import load_local_json_as_string, normalize_address

load_dotenv()

# ABIs for Sugar and Price Oracle
# see: https://github.com/velodrome-finance/sugar
# and  https://github.com/velodrome-finance/oracle
LP_SUGAR_ABI = load_local_json_as_string("abi/lp_sugar.json")
PRICE_ORACLE_ABI = load_local_json_as_string("abi/price_oracle.json")

# RPC gateway
WEB3_PROVIDER_URI = os.environ["WEB3_PROVIDER_URI"]
LP_SUGAR_ADDRESS = os.environ["LP_SUGAR_ADDRESS"]
PRICE_ORACLE_ADDRESS = os.environ["PRICE_ORACLE_ADDRESS"]
# when pricing a bunch of tokens, we batch the full list into smaller chunks
PRICE_BATCH_SIZE = int(os.environ["PRICE_BATCH_SIZE"])
PRICE_THRESHOLD_FILTER = int(os.getenv("PRICE_THRESHOLD_FILTER", 10))

# protocol we are dealing with: Velodrome | Aerodrome
PROTOCOL_NAME = os.environ["PROTOCOL_NAME"]
# web app URL
APP_BASE_URL = os.environ["APP_BASE_URL"]

# token we are converting from
TOKEN_ADDRESS = normalize_address(os.environ["TOKEN_ADDRESS"])
# token we are converting to
STABLE_TOKEN_ADDRESS = os.environ["STABLE_TOKEN_ADDRESS"]
# connector tokens for the pricing oracle
# see: https://github.com/velodrome-finance/oracle
CONNECTOR_TOKENS_ADDRESSES = list(
    map(
        lambda a: normalize_address(a),
        os.environ["CONNECTOR_TOKENS_ADDRESSES"].split(","),
    )
)
# additional tokens to include in the token list
ADDITIONAL_TOKEN_ADDRESSES = list(
    map(
        lambda a: normalize_address(a),
        os.environ.get("ADDITIONAL_TOKEN_ADDRESSES", "").split(","),
    )
) if os.environ.get("ADDITIONAL_TOKEN_ADDRESSES") else []

# caching time for sugar tokens calls
SUGAR_TOKENS_CACHE_MINUTES = int(os.environ["SUGAR_TOKENS_CACHE_MINUTES"])
# caching time for sugar liquidity pools calls
SUGAR_LPS_CACHE_MINUTES = int(os.environ["SUGAR_LPS_CACHE_MINUTES"])
# caching time for oracle price calls
ORACLE_PRICES_CACHE_MINUTES = int(os.environ["ORACLE_PRICES_CACHE_MINUTES"])

# default pagination limit for api calls
GOOD_ENOUGH_PAGINATION_LIMIT = 2000

# pagination limit for pools
POOL_PAGE_SIZE = 500
