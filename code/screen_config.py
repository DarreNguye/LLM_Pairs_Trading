CONFIGS = {
    "v1": dict(
        formation_years=3,     # formation window = this many years ending at AS_OF
        cadf="both",           # "both" = both regression directions must pass (larger p); "min" = either (smaller p)
        correction="none",     # "none" = plain alpha per pair; "bonferroni" = alpha / pairs in the group
        alpha=0.05,            # CADF significance cutoff per pair
        min_price=5.0,         # minimum close over the window
        min_dollar_vol=5e6,    # median daily dollar volume
        hl_range=(5, 60),      # spread half-life, trading days (also main.py's live filter defaults)
        max_beta_drift=0.5,    # |beta(1st half) - beta(2nd half)| / |beta(full)|
        min_cross_per_yr=12,   # spread zero-crossings per year
        max_start_gap=10,      # days a series may start after F_START and still count as "listed all window"
        pool_top_n=1000,       # most liquid stocks with an industry code at AS_OF
    ),
}

# Tuning-set selection (T00X batches only): rank instead of a significance cutoff
TUNING = dict(
    n_select=30,          # keep the 30 best-ranked pairs that pass every non-CADF check
    max_candidates=None,  # None = screen every same-industry pair in the pool; an int caps it (random sample)
    seed=0,               # used only if max_candidates caps the list
)