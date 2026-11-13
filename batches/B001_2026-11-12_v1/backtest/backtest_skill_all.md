# Backtest B001 | run skill_all
batch_id: B001 | run_tag: skill_all | config: v1 | trading: v1 | code: df816a6 | src_main: 1c46c3cb | src_core: acecdfba | src_config: e209020d | src_trading: a686d509 | window: 2024-01-01 to 2025-12-31 | pairs: FBP/OFG,AVA/NWE,GPI/ABG,ONTO/CAMT,GNK/SBLK,GPRE/REX,ICHR/UCTT,WIRE/ATKR,UFPI/BCC,L/CNA,FMX/KOF,IEP/CVI | cost_mult: 1.0 | slippage_bps: 2.0 | ticker_costs: none
source_check: matches repo
params: {"beta_lookback":252,"z_lookback":60,"entry_z":2.0,"exit_z":0.0,"stop_z":4.0,"max_hold_days":60,"gross_leverage":1.0,"borrow_rate":0.01,"entry_mode":"cross","unblock_z":0.5,"coint_pvalue":0.1,"min_half_life":5.0,"max_half_life":60.0,"hl_z_mult":1.0,"hl_hold_mult":3.0}

## Scorecard
```csv
pair,trades,total_return,annual_return,sharpe,max_dd,win_rate,profit_factor,avg_hold_days,time_in_mkt,exit_target,exit_stop,exit_time,exit_other,fees,borrow,positive_years,filtered_hl,filtered_cadf,rejected_orders,open_at_end,delisted
FBP/OFG,6,-0.0239,-0.0120,-0.44,0.0366,0.500,0.50,6.0,0.072,1,5,0,0,217,60,0/2,0,30,0,False,False
AVA/NWE,2,-0.0144,-0.0072,-0.31,0.0270,0.500,0.26,23.5,0.094,0,1,1,0,40,83,1/2,0,46,0,False,False
GPI/ABG,3,0.0712,0.0358,0.97,0.0207,1.000,,14.7,0.088,2,0,1,0,12,53,1/2,8,39,0,False,False
ONTO/CAMT,1,0.0523,0.0263,0.53,0.0588,1.000,,28.0,0.056,1,0,0,0,5,34,1/2,22,49,0,False,False
GNK/SBLK,2,0.0264,0.0133,0.56,0.0144,1.000,,9.5,0.038,2,0,0,0,97,33,1/2,4,46,0,False,False
GPRE/REX,1,-0.0224,-0.0113,-0.62,0.0254,0.000,0.00,8.0,0.016,0,1,0,0,75,20,0/2,4,18,0,False,False
ICHR/UCTT,3,0.0820,0.0412,1.07,0.0171,1.000,,13.7,0.082,2,0,1,0,62,71,1/2,0,52,0,False,False
WIRE/ATKR,0,0.0000,0.0000,0.00,0.0000,,,,0.000,0,0,0,0,0,0,0/1,30,8,0,False,True
UFPI/BCC,4,0.0656,0.0329,1.01,0.0290,0.750,46.83,10.0,0.080,3,1,0,0,39,54,1/2,0,41,0,False,False
L/CNA,4,-0.0111,-0.0056,-0.38,0.0276,0.500,0.59,5.5,0.044,2,2,0,0,65,43,0/2,52,33,0,False,False
FMX/KOF,6,-0.0004,-0.0002,-0.00,0.0495,0.500,0.98,8.5,0.116,3,3,0,0,67,102,0/2,0,32,0,True,False
IEP/CVI,3,-0.1695,-0.0851,-1.12,0.2097,0.000,0.00,4.3,0.038,0,3,0,0,318,16,1/2,22,25,0,True,False
```

## P&L by year ($)
```csv
pair,2024,2025
FBP/OFG,-355,-1640
AVA/NWE,-1629,430
GPI/ABG,0,5937
ONTO/CAMT,4359,0
GNK/SBLK,2201,0
GPRE/REX,0,-1868
ICHR/UCTT,6834,0
WIRE/ATKR,0,
UFPI/BCC,0,5468
L/CNA,-924,0
FMX/KOF,0,-33
IEP/CVI,-15857,1736
```
