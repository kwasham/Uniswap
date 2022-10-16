# https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v3

import requests
import json
import func_triangular_arb

"""Get Graph QL mid prices for uniswap"""


def retrieve_uniswap_information():
    query = """
        query {
                pools (orderBy: totalValueLockedETH, 
                    orderDirection: desc, 
                    first: 500) {
                    id
                    totalValueLockedETH
                    token0Price
                    token1Price
                    feeTier
                    token0 {id symbol name decimals}
                    token1 {id symbol name decimals}
                 }
            }
        """

    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    req = requests.post(url, json={"query": query})

    return req.json()


if __name__ == "__main__":
    pairs = retrieve_uniswap_information()["data"]["pools"]
    structured_pairs = func_triangular_arb.structure_trading_pairs(pairs, limit=100)

    for t_pair in structured_pairs:
        surface_rate = func_triangular_arb.calc_triangular_arb_surface_rate(t_pair, min_rate=1.5)
        print(surface_rate)
