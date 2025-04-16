#!/usr/bin/env python3

import argparse
import os
from ms_conc.calibration_curves import (
    read_peaklist, read_standards,
    ConcentrationEstimator,
    training_from_standard_results,
    train_to_validation
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="SCALiR CLI for metabolomics standard curve fitting.")
    parser.add_argument('--standards', required=True)
    parser.add_argument('--peaklist', required=True)
    parser.add_argument('--program', choices=['Mint', 'Maven', 'internal'], required=True)
    parser.add_argument('--mint_type', default='dense')
    parser.add_argument('--intensity_col', default='peak_max')
    parser.add_argument('--fit_mode', choices=['fixed', 'interval', 'wide'], default='fixed')
    parser.add_argument('--interval', nargs=2, type=float, default=[0.85, 1.15])
    parser.add_argument('--output_prefix', default='scalir_output')
    parser.add_argument('--plot_dir', default='plots')
    parser.add_argument('--logfile', default=None)
    return parser.parse_args()

def main():
    args = parse_args()

    os.makedirs(args.plot_dir, exist_ok=True)

    std_df = read_standards(args.standards)
    results = read_peaklist(args.peaklist, program=args.program, mint_type=args.mint_type)

    estimator = ConcentrationEstimator(fit_mode=args.fit_mode, slope_range=args.interval)
    concentrations = estimator.fit_transform(results, std_df, intensity_col=args.intensity_col)
    parameters = estimator.param_df_

    concentrations.to_csv(f'{args.output_prefix}_concentrations.csv', index=False)
    parameters.to_csv(f'{args.output_prefix}_parameters.csv', index=False)

    for compound in results.peak_label.unique():
        x_train, y_train = training_from_standard_results(std_df, by=args.intensity_col)
        x_viz = x_train.copy()
        y_train_corrected = train_to_validation(x_train, y_train, estimator.params_)

        x_viz['pred_conc'] = estimator.predict(x_viz).pred_conc
        x_viz['Concentration'] = y_train
        x_viz['Corr_Concentration'] = y_train_corrected
        x_viz = x_viz.fillna(-1.0)
        x_viz['in_range'] = x_viz['Corr_Concentration'].apply(lambda x: 2 if x <= 0 else 1)
        x_viz = x_viz[x_viz['Concentration'] > 1e-8]
        dat = x_viz[x_viz.peak_label == compound]
        dat = dat[dat.value > 0]

        plt.figure(figsize=(4, 4))
        for inr, color in zip([2, 1], ['gray', 'black']):
            x_vals = dat.Concentration[dat.in_range == inr]
            y_vals = dat.value[dat.in_range == inr]
            label = 'Out-of-range' if inr == 2 else 'In-range'
            plt.plot(x_vals, y_vals, 'o', color=color, label=label)
        plt.plot(dat.pred_conc[dat.in_range == 1], dat.value[dat.in_range == 1], color='black')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(f'{compound} concentration (μM)', fontsize=14)
        plt.ylabel(f'{compound} response ratio', fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.legend(fontsize=10)
        plt.savefig(os.path.join(args.plot_dir, f'{compound}_standard_curve.png'))
        plt.close()

    if args.logfile:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "scalir_version": "1.0.0",
            "parameters": vars(args)
        }
        with open(args.logfile, 'w') as f:
            json.dump(log_data, f, indent=2)

if __name__ == "__main__":
    main()
