# Function Library Index

This folder reorganizes the functions collected from `lecture01` to `lecture11`
by financial knowledge area.

## time_value_of_money.py

- `annuity_value`: merged from `pv_annuity`, `fv_annuity`, `pv_annuity_due`, `fv_annuity_due`
- `growing_annuity_value`: merged from `pv_growing_annuity`, `fv_growing_annuity`, `pv_growing_annuity_due`, `fv_growing_annuity_due`
- `perpetuity_value`: merged from `pv_perpetuity`, `pv_perpetuity_due`, `pv_growing_perpetuity`, `pv_growing_perpetuity_due`, `pv_perpetuity_delayed`, `pv_growing_perpetuity_delayed`
- `effective_annual_rate`: from `effect`
- `convert_compounding_frequency`: from `effcetiverates`
- `nominal_to_continuous_rate`: from `rmtorc`
- `future_value_continuous`: from `fv_continuous`

## fixed_income.py

- `bond_price`: merged duplicate `bond_price` definitions
- `zero_coupon_bond_price`: from `zero_price`
- `bond_ytm`: from `bond_ytm`
- `macaulay_duration`: from `duration`
- `modified_duration`: from `mod_d`
- `plot_yield_curve`: from `plot_yield`

## equity_analysis.py

- `daily_return`: from `ret_f`
- `annual_return`: from `ret_annual`
- `compounded_group_return`: from grouped return lambda
- `gordon_growth_value`: from `gordon`

## portfolio_theory.py

- `lower_partial_standard_deviation`: from `lpsd_f`
- `two_stock_variance`: from `var2stock`
- `portfolio_variance`: from `portfolio_var`
- `sharpe_ratio`: from `sharperatio`
- `negative_sharpe_ratio_from_n_minus_1_weights`: from `sharperatio_n_minus_1_stocks`

## derivatives.py

- `option_payoff`: merged from `payoff_calls`, `payoff_put`
- `black_scholes_price`: merged from `bs_call`, `bs_put`, `bscall`, `bsCall`
- `implied_volatility`: merged from `implied_vol_call`, `implied_vol_put`, `implied_vol_call_min`, `implied_vol_put_min`
- `implied_volatility_from_option_row`: from option-row lambda
- `option_delta`: merged from `delta_f`, `delta_n`, `delta1_f`, `delta2_f`
- `option_gamma`: merged from `gamma1_f`, `gamma2_f`, `gamma3_f`

## optimization.py

- `quadratic_objective`: from `myfunction`
- `brent_objective`: from `f`
- `squared_distance_objective`: from lambda objective
- `cubic_lambda_example`: from lambda objective
- `constrained_objective`: from constrained lambda objective
- `constraint_one`: from first inequality lambda
- `constraint_two`: from second inequality lambda
- `constraint_three`: from third inequality lambda
