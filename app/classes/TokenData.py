class TokensData:
    def __init__(self, tokens):
        self.tokens = tokens
        self.max_new_holders = 0
        self.max_tvl_change = 0
        self.max_price_change = 0
        self.min_tvl_change = 10000000000
        self.min_price_change = 10000000000
        for token in tokens:
            if token['new_users_min_amount'] > self.max_new_holders:
                self.max_new_holders = token['new_users_min_amount']
            if token['token_tvl_change'] > self.max_tvl_change:
                self.max_tvl_change = token['token_tvl_change']
            if token['price_change_normed'] > self.max_price_change:
                self.max_price_change = token['price_change_normed']
            if token['token_tvl_change'] < self.min_tvl_change:
                self.min_tvl_change = token['token_tvl_change']
            if token['price_change_normed'] < self.min_price_change:
                self.min_price_change = token['price_change_normed']
        self.tvl_category = {
            "$10M - $20M": {"low": 10_000_000, "high": None, "coefficient": 1},
            "$5M - $10M": {"low": 5_000_000, "high": 10_000_000, "coefficient": 0.8},
            "$2M - $5M": {"low": 2_000_000, "high": 5_000_000, "coefficient": 0.6},
            "$1M - $2M": {"low": 1_000_000, "high": 2_000_000, "coefficient": 0.5},
            "$0.5M - $1M": {"low": 500_000, "high": 1_000_000, "coefficient": 0.4},
            "$0.1M - $0.5M": {"low": None, "high": 500_000, "coefficient": 0.3},
        }

    def get_token(self, token_name):
        for token in self.tokens:
            if token['name'] == token_name:
                return token

    def get_tvl_category_coefficient(self, token_name):
        return self.tvl_category[self.get_token(token_name)['token_tvl_category']]['coefficient']

    def calc_token_metrics(self, token_name):
        token = self.get_token(token_name)
        tvl_category_coefficient = self.get_tvl_category_coefficient(token_name)
        price_change_weight = 30 * tvl_category_coefficient
        tvl_change_weight = 30 + (30 - price_change_weight) * 3 / 7
        new_holders_weight = 40 + (30 - price_change_weight) * 4 / 7
        new_holders_relative = token['new_users_min_amount'] / self.max_new_holders
        tvl_change_relative = (token['token_tvl_change'] - self.min_tvl_change) / (
                self.max_tvl_change - self.min_tvl_change)
        price_change_relative = (token['price_change_normed'] - self.min_price_change) / (
                self.max_price_change - self.min_price_change)
        score = new_holders_weight * new_holders_relative + tvl_change_weight * tvl_change_relative + \
            price_change_weight * price_change_relative

        token['tvl_category_coefficient'] = tvl_category_coefficient
        token['new_holders_weight'] = new_holders_weight
        token['tvl_change_weight'] = tvl_change_weight
        token['price_change_weight'] = price_change_weight
        token['new_holders_relative'] = new_holders_relative
        token['tvl_change_relative'] = tvl_change_relative
        token['price_change_relative'] = price_change_relative
        token['calc_score'] = score

        self.tokens = map(lambda x: x if x['name'] != token_name else token, self.tokens)

        return token
