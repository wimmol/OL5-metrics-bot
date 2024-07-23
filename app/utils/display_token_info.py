import re


def display_token_info(token) -> str:
    return (f"Token: {token['name']}\n\n"

            f"New holders: {token['new_users_min_amount']}\n\n"
            
            f"TVL category: {token['token_tvl_category']}\n"
            f"TVL category coefficient: {token['tvl_category_coefficient'] * 100} %\n\n"
            
            f"Start TVL: {token['token_start_tvl']} TON\n"
            f"Current TVL: {token['token_last_tvl']} TON\n"
            f"TVL Change: {token['token_tvl_change']} TON\n\n"

            f"Start price: {token['token_price_before']:.3f} TON\n"
            f"Current price: {token['token_price_after']:.3f} TON\n" 
            f"Price change real: {token['price_change_simple']:.3f} %\n"
            f"Price change normed: {token['price_change_normed']:.3f} %\n\n"

            f"New holders weight: {token['new_holders_weight']} %\n"
            f"TVL change weight: {token['tvl_change_weight']} %\n"
            f"Price change weight: {token['price_change_weight']} %\n\n"

            f"New holders score: {token['new_holders_relative']:.6f}\n"
            f"TVL change score: {token['tvl_change_relative']:.6f}\n"
            f"Price change score: {token['price_change_relative']:.6f}\n\n"
            
            f"Score from request: {token['score']:.3f}\n"
            f"Score calculated: {token['calc_score']:.3f}\n"

            f"Score = \n(New_holders_weight) * (New_holders_score) +"
            f"(TVL_change_weight) * (TVL_change_score) +"
            f"(Price_change_weight) * (Price_change_score)\n\n"
            )
