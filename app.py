# --- CONFIG HARDWARE PERSISTENCE REGISTRY FILE MANAGEMENT ---
NEW_REGISTRY_FILE = os.path.join(DATA_DIR, "profile_registry_config.csv")
OLD_REGISTRY_FILE = "profile_registry_config.csv"  # Your old root file where the 10 sizes live

def load_profile_registry():
    # 1. First, check if we already migrated to the new data folder
    if os.path.exists(NEW_REGISTRY_FILE):
        try:
            df_reg = pd.read_csv(NEW_REGISTRY_FILE)
            registry = {}
            for _, row in df_reg.iterrows():
                registry[str(row['profile_name'])] = {
                    "target": float(row['target']),
                    "usl": float(row['usl']),
                    "lsl": float(row['lsl']),
                    "seed_mean": float(row['seed_mean']),
                    "seed_sigma": float(row['seed_sigma'])
                }
            if registry:
                return registry
        except Exception:
            pass

    # 2. FALLBACK MIGRATION: If new file doesn't exist, read from old root file so you don't lose your 10 sizes
    if os.path.exists(OLD_REGISTRY_FILE):
        try:
            df_reg = pd.read_csv(OLD_REGISTRY_FILE)
            registry = {}
            for _, row in df_reg.iterrows():
                registry[str(row['profile_name'])] = {
                    "target": float(row['target']),
                    "usl": float(row['usl']),
                    "lsl": float(row['lsl']),
                    "seed_mean": float(row['seed_mean']),
                    "seed_sigma": float(row['seed_sigma'])
                }
            if registry:
                # Safely write it into the new directory so it's migrated forever
                save_profile_registry(registry)
                return registry
        except Exception:
            pass
            
    # 3. Hardcoded defaults only if absolutely no previous files are found anywhere
    default_registry = {
        "750-16 HT-99 Treadweight": {"target": 11.1600, "usl": 11.4948, "lsl": 10.8252, "seed_mean": 11.0137, "seed_sigma": 0.0395},
        "400-8 HT-60 Treadweight": {"target": 2.0200, "usl": 2.0806, "lsl": 1.9594, "seed_mean": 1.9989, "seed_sigma": 0.0216},
        "195 R 15 Tread Profile": {"target": 5.5000, "usl": 5.6650, "lsl": 5.3350, "seed_mean": 5.4850, "seed_sigma": 0.0310}
    }
    save_profile_registry(default_registry)
    return default_registry

def save_profile_registry(registry_dict):
    rows = []
    for name, data in registry_dict.items():
        rows.append({
            'profile_name': name,
            'target': data['target'],
            'usl': data['usl'],
            'lsl': data['lsl'],
            'seed_mean': data['seed_mean'],
            'seed_sigma': data['seed_sigma']
        })
    pd.DataFrame(rows).to_csv(NEW_REGISTRY_FILE, index=False)
