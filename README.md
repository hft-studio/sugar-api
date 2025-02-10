# Sugar API

Sugar API is a FastAPI-based service that provides easy access to Velodrome/Aerodrome DeFi protocol data through the Sugar contract. It offers endpoints for retrieving pool statistics, token prices, total value locked (TVL), fees, and rewards data from the blockchain.

## Features

- **Pool Data**: Get detailed information about liquidity pools including reserves, fees, APR, and volume
- **Price Oracle**: Access token prices using the protocol's price oracle
- **TVL Tracking**: Monitor total value locked across all pools
- **Fee Analytics**: Track protocol fees and rewards
- **Pool Search**: Search functionality to find specific pools by symbol or address

## API Endpoints

- `/api/price` - Get current token price
- `/api/pools` - List all pools
- `/api/pools/{address}` - Get detailed stats for specific pool
- `/api/pools/search` - Search pools by query
- `/api/tvl` - Get protocol's total value locked
- `/api/fees` - Get protocol's fee data
- `/api/rewards` - Get protocol's rewards data

## Setup

1. Copy `.env.example` to `.env` and configure your environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `python run.py`

## Environment Variables

Key configuration variables:
- `WEB3_PROVIDER_URI`: RPC endpoint for the blockchain
- `LP_SUGAR_ADDRESS`: Address of the Sugar contract
- `PRICE_ORACLE_ADDRESS`: Address of the Price Oracle contract
- `TOKEN_ADDRESS`: Protocol token address
- `STABLE_TOKEN_ADDRESS`: Stable coin address for price calculations

## Docker

Build and run with Docker:
```bash
docker build -t sugar-api .
docker run -p 5000:5000 sugar-api
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0
