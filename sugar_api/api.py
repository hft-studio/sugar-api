from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from .data import Token, Price, LiquidityPool, LiquidityPoolEpoch
from .settings import TOKEN_ADDRESS, STABLE_TOKEN_ADDRESS, PROTOCOL_NAME

app = FastAPI()

@app.get("/api/price")
async def get_price():
    token = await Token.get_by_token_address(TOKEN_ADDRESS)
    [token_price] = await Price.get_prices([token])
    return {
        'symbol': token.symbol,
        'price': token_price.pretty_price,
        'address': token.token_address
    }

@app.get("/api/pools/{address}")
async def get_pool(address: str):
    pool = await LiquidityPool.by_address(address)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    
    tvl = await LiquidityPool.tvl([pool])
    pool_epoch = await LiquidityPoolEpoch.fetch_for_pool(address)
    
    return {
        'address': pool.lp,
        'symbol': pool.symbol,
        'is_stable': pool.is_stable,
        'token0': {
            'address': pool.token0.token_address,
            'symbol': pool.token0.symbol,
            'decimals': pool.token0.decimals
        } if pool.token0 else None,
        'token1': {
            'address': pool.token1.token_address,
            'symbol': pool.token1.symbol,
            'decimals': pool.token1.decimals
        } if pool.token1 else None,
        'reserve0': pool.reserve0.amount if pool.reserve0 else 0,
        'reserve1': pool.reserve1.amount if pool.reserve1 else 0,
        'reserve0_usd': pool.reserve0.amount_in_stable if pool.reserve0 else 0,
        'reserve1_usd': pool.reserve1.amount_in_stable if pool.reserve1 else 0,
        'fees_token0': pool.token0_fees.amount if pool.token0_fees else 0,
        'fees_token1': pool.token1_fees.amount if pool.token1_fees else 0,
        'fees_token0_usd': pool.token0_fees.amount_in_stable if pool.token0_fees else 0,
        'fees_token1_usd': pool.token1_fees.amount_in_stable if pool.token1_fees else 0,
        'pool_fee': pool.pool_fee_percentage,
        'volume': pool.volume,
        'tvl': tvl,
        'apr': pool.apr(tvl),
        'epoch_data': {
            'fees': pool_epoch.total_fees if pool_epoch else 0,
            'bribes': pool_epoch.total_bribes if pool_epoch else 0,
            'total_rewards': (pool_epoch.total_fees + pool_epoch.total_bribes) if pool_epoch else 0
        }
    } 

@app.get("/api/pools")
async def get_pools():
    pools = await LiquidityPool.get_pools()
    return [{
        'address': pool.lp,
        'symbol': pool.symbol,
        'is_stable': pool.is_stable,
        'token0': {
            'address': pool.token0.token_address,
            'symbol': pool.token0.symbol,
            'decimals': pool.token0.decimals
        } if pool.token0 else None,
        'token1': {
            'address': pool.token1.token_address,
            'symbol': pool.token1.symbol,
            'decimals': pool.token1.decimals
        } if pool.token1 else None,
        'reserve0': pool.reserve0.amount if pool.reserve0 else 0,
        'reserve1': pool.reserve1.amount if pool.reserve1 else 0,
        'reserve0_usd': pool.reserve0.amount_in_stable if pool.reserve0 else 0,
        'reserve1_usd': pool.reserve1.amount_in_stable if pool.reserve1 else 0,
        'fees_token0': pool.token0_fees.amount if pool.token0_fees else 0,
        'fees_token1': pool.token1_fees.amount if pool.token1_fees else 0,
        'fees_token0_usd': pool.token0_fees.amount_in_stable if pool.token0_fees else 0,
        'fees_token1_usd': pool.token1_fees.amount_in_stable if pool.token1_fees else 0,
        'pool_fee': pool.pool_fee_percentage,
        'volume': pool.volume
    } for pool in pools]

@app.get("/api/tvl")
async def get_tvl():
    pools = await LiquidityPool.get_pools()
    tvl = await LiquidityPool.tvl(pools)
    tokens = await Token.get_all_listed_tokens()
    return {
        'tvl': tvl,
        'num_tokens': len(tokens),
        'protocol': PROTOCOL_NAME
    }

@app.get("/api/fees")
async def get_fees():
    pools = await LiquidityPool.get_pools()
    fees = sum(map(lambda p: p.total_fees, pools))
    return {
        'total_fees': fees,
        'num_pools': len(pools),
        'protocol': PROTOCOL_NAME
    }

@app.get("/api/rewards")
async def get_rewards():
    lpes = await LiquidityPoolEpoch.fetch_latest()
    fees = sum(map(lambda lpe: lpe.total_fees, lpes))
    bribes = sum(map(lambda lpe: lpe.total_bribes, lpes))
    return {
        'total_fees': fees,
        'total_bribes': bribes,
        'total_rewards': fees + bribes,
        'protocol': PROTOCOL_NAME
    }

@app.get("/api/pools/search")
async def search_pools(q: str = Query(..., description="Search query"), 
                      limit: int = Query(10, description="Maximum number of results")):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
    pools = await LiquidityPool.search(q, limit)
    return [{
        'address': pool.lp,
        'symbol': pool.symbol,
        'is_stable': pool.is_stable,
        'token0': {
            'address': pool.token0.token_address,
            'symbol': pool.token0.symbol
        } if pool.token0 else None,
        'token1': {
            'address': pool.token1.token_address,
            'symbol': pool.token1.symbol
        } if pool.token1 else None
    } for pool in pools] 