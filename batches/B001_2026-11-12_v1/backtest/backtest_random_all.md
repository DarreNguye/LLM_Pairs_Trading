# Backtest B001 | run random_all
batch_id: B001 | run_tag: random_all | config: v1 | trading: v1 | code: df816a6 | src_main: 1c46c3cb | src_core: acecdfba | src_config: e209020d | src_trading: a686d509 | window: 2024-01-01 to 2025-12-31 | pairs: G/OKTA,ERIC/JEF,ROK/QCOM,SPLK/CUZ,WPC/CMS,K/TFII,UEC/FRT,EDU/CWH,NVR/PEG,FDS/PRGO,CNK/KVUE,WST/ADI | cost_mult: 1.0 | slippage_bps: 2.0 | ticker_costs: none
source_check: matches repo
params: {"beta_lookback":252,"z_lookback":60,"entry_z":2.0,"exit_z":0.0,"stop_z":4.0,"max_hold_days":60,"gross_leverage":1.0,"borrow_rate":0.01,"entry_mode":"cross","unblock_z":0.5,"coint_pvalue":0.1,"min_half_life":5.0,"max_half_life":60.0,"hl_z_mult":1.0,"hl_hold_mult":3.0}

## Scorecard
```csv
pair,trades,total_return,annual_return,sharpe,max_dd,win_rate,profit_factor,avg_hold_days,time_in_mkt,exit_target,exit_stop,exit_time,exit_other,fees,borrow,positive_years,filtered_hl,filtered_cadf,rejected_orders,open_at_end,delisted
G/OKTA,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,0,39,0,False,False
ERIC/JEF,1,0.0252,0.0127,0.27,0.0367,1.000,,7.0,0.014,0,1,0,0,69,14,1/2,4,35,0,False,False
ROK/QCOM,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,0,16,0,False,False
SPLK/CUZ,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/1,0,0,0,False,True
WPC/CMS,2,-0.0566,-0.0284,-0.78,0.0651,0.000,0.00,16.0,0.064,0,2,0,0,32,76,0/2,0,41,0,False,False
K/TFII,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/2,42,8,0,False,True
UEC/FRT,1,-0.0816,-0.0410,-0.84,0.0845,0.000,0.00,8.0,0.016,0,1,0,0,65,13,0/2,23,24,0,False,False
EDU/CWH,1,-0.0455,-0.0229,-0.46,0.0685,0.000,0.00,4.0,0.008,0,1,0,0,29,9,0/2,5,28,0,False,False
NVR/PEG,3,0.0158,0.0079,0.22,0.0433,0.333,1.86,12.0,0.072,1,1,1,0,25,59,1/2,7,40,0,False,False
FDS/PRGO,1,-0.0553,-0.0277,-0.88,0.0553,0.000,0.00,8.0,0.016,0,1,0,0,11,21,0/2,15,21,0,False,False
CNK/KVUE,1,0.0204,0.0103,0.77,0.0036,1.000,,3.0,0.006,1,0,0,0,38,8,1/2,0,46,0,False,False
WST/ADI,1,-0.0530,-0.0266,-0.95,0.0562,0.000,0.00,4.0,0.008,0,1,0,0,4,11,0/2,0,31,0,False,False
```

## P&L by year ($)
```csv
pair,2024,2025
G/OKTA,0,0
ERIC/JEF,0,2100
ROK/QCOM,0,0
SPLK/CUZ,0,
WPC/CMS,-2261,-2453
K/TFII,0,0
UEC/FRT,-6800,0
EDU/CWH,0,-3794
NVR/PEG,0,1318
FDS/PRGO,-4604,0
CNK/KVUE,0,1702
WST/ADI,-4417,0
```
