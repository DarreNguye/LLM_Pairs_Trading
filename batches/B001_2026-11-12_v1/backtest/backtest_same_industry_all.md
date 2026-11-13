# Backtest B001 | run same_industry_all
batch_id: B001 | run_tag: same_industry_all | config: v1 | trading: v1 | code: df816a6 | src_main: 1c46c3cb | src_core: acecdfba | src_config: e209020d | src_trading: a686d509 | window: 2024-01-01 to 2025-12-31 | pairs: FFIV/MSFT,LNG/TRP,VRSN/ZS,GILD/OGN,FICO/UBER,AMT/IRM,OTIS/PH,NET/PANW,MU/TXN,ETN/GGG,AER/R,BPOP/CMA | cost_mult: 1.0 | slippage_bps: 2.0 | ticker_costs: none
source_check: matches repo
params: {"beta_lookback":252,"z_lookback":60,"entry_z":2.0,"exit_z":0.0,"stop_z":4.0,"max_hold_days":60,"gross_leverage":1.0,"borrow_rate":0.01,"entry_mode":"cross","unblock_z":0.5,"coint_pvalue":0.1,"min_half_life":5.0,"max_half_life":60.0,"hl_z_mult":1.0,"hl_hold_mult":3.0}

## Scorecard
```csv
pair,trades,total_return,annual_return,sharpe,max_dd,win_rate,profit_factor,avg_hold_days,time_in_mkt,exit_target,exit_stop,exit_time,exit_other,fees,borrow,positive_years,filtered_hl,filtered_cadf,rejected_orders,open_at_end,delisted
FFIV/MSFT,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,33,38,0,False,False
LNG/TRP,1,-0.0229,-0.0115,-0.66,0.0289,0.000,0.00,21.0,0.042,0,1,0,0,10,31,0/2,1,35,0,False,False
VRSN/ZS,1,-0.0392,-0.0197,-0.53,0.0550,0.000,0.00,7.0,0.014,0,1,0,0,5,20,0/2,5,44,0,False,False
GILD/OGN,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,0,3,0,False,False
FICO/UBER,2,-0.0842,-0.0423,-0.88,0.1092,0.000,0.00,7.0,0.028,0,2,0,0,15,23,0/2,20,17,0,False,False
AMT/IRM,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,1,56,0,False,False
OTIS/PH,1,-0.0302,-0.0152,-0.52,0.0542,0.000,0.00,14.0,0.028,0,1,0,0,8,16,0/2,0,49,0,False,False
NET/PANW,2,0.0803,0.0403,0.32,0.1053,0.500,1.92,12.5,0.050,1,1,0,0,15,38,1/2,26,40,0,False,False
MU/TXN,1,0.0392,0.0197,0.92,0.0145,1.000,,11.0,0.022,1,0,0,0,5,17,1/2,22,28,0,False,False
ETN/GGG,1,-0.0093,-0.0047,-0.71,0.0125,0.000,0.00,3.0,0.006,0,1,0,0,8,2,0/2,36,44,0,False,False
AER/R,5,0.1457,0.0732,1.00,0.0688,0.600,4.45,7.4,0.074,3,2,0,0,42,74,2/2,7,35,0,False,False
BPOP/CMA,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,18,66,0,False,False
```

## P&L by year ($)
```csv
pair,2024,2025
FFIV/MSFT,0,0
LNG/TRP,0,-1907
VRSN/ZS,-3269,0
GILD/OGN,0,0
FICO/UBER,-7019,0
AMT/IRM,0,0
OTIS/PH,-2519,0
NET/PANW,6690,0
MU/TXN,0,3264
ETN/GGG,0,-778
AER/R,456,11690
BPOP/CMA,0,0
```
