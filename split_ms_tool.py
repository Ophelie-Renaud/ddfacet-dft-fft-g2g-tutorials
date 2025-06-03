import os
import shutil
import numpy as np
from casacore.tables import table
import argparse

def split_ms(ms_path, output_prefix, criterion='time', n_splits=2):
    assert criterion in ['time', 'scan', 'field', 'spw'], "Critère non supporté pour split standard."

    t = table(ms_path)
    colname = {
        'time': 'TIME',
        'scan': 'SCAN_NUMBER',
        'field': 'FIELD_ID',
        'spw': 'DATA_DESC_ID'
    }[criterion]

    column = t.getcol(colname)
    unique_vals = sorted(set(column))
    print(f"📊 {criterion.upper()} values trouvées : {unique_vals}")

    if n_splits > len(unique_vals):
        print(f"⚠️ Seulement {len(unique_vals)} valeurs distinctes pour {colname}, ajustement de n_splits.")
        n_splits = len(unique_vals)

    groups = [[] for _ in range(n_splits)]
    for i, val in enumerate(unique_vals):
        groups[i % n_splits].append(val)

    for i, group_vals in enumerate(groups):
        val_str = ','.join(map(str, group_vals))
        query_str = f"{colname} IN [{val_str}]"
        sub = t.query(query_str)
        out_path = f"{output_prefix}_{criterion}_{i}.ms"
        if os.path.exists(out_path):
            shutil.rmtree(out_path)
        sub.copy(out_path, deep=True)
        print(f"✅ Split {i} : {sub.nrows()} lignes -> {out_path}")

    t.close()

def split_by_channel(ms_path, output_prefix):
    t = table(ms_path)
    data = t.getcol('DATA')
    n_channels = data.shape[1]
    t.close()

    print(f"📡 Nombre de canaux détectés : {n_channels}")

    for chan_idx in range(n_channels):
        print(f"\n📤 Extraction du canal {chan_idx}")
        out_path = f"{output_prefix}_channel_{chan_idx}.ms"
        if os.path.exists(out_path):
            shutil.rmtree(out_path)
        shutil.copytree(ms_path, out_path)

        t_out = table(out_path, readonly=False)
        data_all = t_out.getcol('DATA')
        masked_data = np.zeros_like(data_all)
        masked_data[:, chan_idx, :] = data_all[:, chan_idx, :]
        t_out.putcol('DATA', masked_data)
        t_out.close()

        print(f"✅ Canal {chan_idx} sauvegardé dans : {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Measurement Set (MS) selon divers critères.")
    parser.add_argument("ms_path", help="Chemin vers le MS d'entrée.")
    parser.add_argument("output_prefix", help="Préfixe ou dossier de sortie.")
    parser.add_argument("--criterion", choices=['time', 'scan', 'field', 'spw', 'channel'], default='time',
                        help="Critère de découpe (par défaut: time).")
    parser.add_argument("--n_splits", type=int, default=2,
                        help="Nombre de splits (non utilisé si criterion=channel).")

    args = parser.parse_args()

    if args.criterion == 'channel':
        split_by_channel(args.ms_path, args.output_prefix)
    else:
        split_ms(args.ms_path, args.output_prefix, criterion=args.criterion, n_splits=args.n_splits)

