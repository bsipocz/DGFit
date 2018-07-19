import argparse

import matplotlib.pyplot as plt
import colorsys
import matplotlib
import numpy as np

from ObsData import ObsData
from DustGrains import DustGrains

if __name__ == "__main__":

    # commandline parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--composition",
                        choices=['astro-silicates', 'astro-carbonaceous',
                                 'astro-graphite',
                                 'astro-PAH-ionized', 'astro-PAH-neutral'],
                        default='astro-silicates',
                        help="Grain composition")
    parser.add_argument("--obsdata", help="transform to observed data grids",
                        action="store_true")
    parser.add_argument("--png", help="save figure as a png file",
                        action="store_true")
    parser.add_argument("--eps", help="save figure as an eps file",
                        action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file",
                        action="store_true")
    args = parser.parse_args()

    DG = DustGrains()
    DG.from_files(args.composition,
                  path='data/indiv_grain/')

    if args.obsdata:
        OD = ObsData(['data/mw_rv31/MW_diffuse_Gordon09_band_ext.dat',
                      'data/mw_rv31/MW_diffuse_Gordon09_iue_ext.dat',
                      'data/mw_rv31/MW_diffuse_Gordon09_fuse_ext.dat'],
                     'data/mw_rv31/MW_diffuse_Gordon09_avnhi.dat',
                     'data/mw_rv31/MW_diffuse_Jenkins09_abundances.dat',
                     'data/mw_rv31/MW_diffuse_Compiegne11_ir_emission.dat',
                     'dust_scat.dat',
                     ext_tags=['band', 'iue', 'fuse'])
        new_DG = DustGrains()
        new_DG.from_object(DG, OD)
        DG = new_DG

    # setup the plots
    fontsize = 12
    font = {'size': fontsize}

    matplotlib.rc('font', **font)

    matplotlib.rc('lines', linewidth=2)
    matplotlib.rc('axes', linewidth=2)
    matplotlib.rc('xtick.major', width=2)
    matplotlib.rc('ytick.major', width=2)

    fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(15, 10))

    ws_indxs = np.argsort(DG.wavelengths)
    ews_indxs = np.argsort(DG.wavelengths_emission)
    waves = DG.wavelengths[ws_indxs]
    for i in range(DG.n_sizes):
        pcolor = colorsys.hsv_to_rgb(float(i) / DG.n_sizes / (1.1), 1, 1)

        ax[0, 0].plot(waves, DG.cabs[i, ws_indxs], color=pcolor)
        ax[0, 0].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[0, 0].set_ylabel('C(abs)')
        ax[0, 0].set_xscale('log')
        ax[0, 0].set_yscale('log')

        ax[0, 1].plot(waves, DG.csca[i, ws_indxs], color=pcolor)
        ax[0, 1].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[0, 1].set_ylabel('C(sca)')
        ax[0, 1].set_xscale('log')
        ax[0, 1].set_yscale('log')

        ax[0, 2].plot(waves, DG.cext[i, ws_indxs], color=pcolor)
        ax[0, 2].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[0, 2].set_ylabel('C(sca)')
        ax[0, 2].set_xscale('log')
        ax[0, 2].set_yscale('log')

        ax[1, 0].plot(DG.wavelengths_scat_a,
                      DG.scat_a_csca[i, :]/DG.scat_a_cext[i, :],
                      'o',
                      color=pcolor)
        ax[1, 0].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[1, 0].set_ylabel('albedo')
        ax[1, 0].set_xscale('log')

        ax[1, 1].plot(DG.wavelengths_scat_g, DG.scat_g[i, :],
                      'o', color=pcolor)
        ax[1, 1].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[1, 1].set_ylabel('g')
        ax[1, 1].set_xscale('log')

        ax[1, 2].plot(DG.wavelengths_emission[ews_indxs],
                      DG.emission[i, ews_indxs], color=pcolor)
        ax[1, 2].set_xlabel(r'$\lambda$ [$\mu m$]')
        ax[1, 2].set_ylabel('Emission')
        ax[1, 2].set_xscale('log')
        ax[1, 2].set_yscale('log')
        cur_ylim = ax[1, 2].get_ylim()
        ax[1, 2].set_ylim([1e-23, 1e-0])

    plt.tight_layout()

    # show or save
    basename = 'DustGrains_diag'
    if args.png:
        fig.savefig(basename+'.png')
    elif args.eps:
        fig.savefig(basename+'.eps')
    elif args.pdf:
        fig.savefig(basename+'.pdf')
    else:
        plt.show()
