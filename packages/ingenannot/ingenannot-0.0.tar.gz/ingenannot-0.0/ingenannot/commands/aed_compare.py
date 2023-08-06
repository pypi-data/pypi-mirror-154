#/usr/bin/env python3

import logging
import multiprocessing
import math
import pysam
import sys
from ingenannot.utils import Utils
from ingenannot.utils.gff_reader import GFF3Reader, GTFReader
from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.commands.command import Command

import numpy as np
import seaborn as sns
import matplotlib
import pandas as pd
import re

import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg



class AEDCompare(Command):

    def __init__(self, args):

        self.fof = args.fof
        self.ncol = 6

    def get_aed(self, genes):

        logging.info("Retrieving aed annotations")

        for g in genes:
            for tr in g.lTranscripts:
                if "aed_ev_tr" in tr.dAttributes and "ev_tr" in tr.dAttributes:
                    tr.best_tr_evidence = (tr.dAttributes["ev_tr"][0],float(tr.dAttributes["aed_ev_tr"][0]))
                else:
                    logging.error("Problem: transcript [{}] of gene [{}], source [{}], missing aed_tr annotations".format(tr.id, g.gene_id, g.source))
                if "aed_ev_pr" in tr.dAttributes and "ev_pr" in tr.dAttributes:
                    tr.best_bx_evidence = (tr.dAttributes["ev_pr"][0],float(tr.dAttributes["aed_ev_pr"][0]))
                else:
                    logging.error("Problem: transcript [{}] of gene [{}], source [{}], missing aed_pr annotations".format(tr.id, g.gene_id, g.source))


    def plotCumulativeAED(self, sources, genes, evidence="tr",out="plotCumulativeAED.png", ncol=4):

        colors=["green","red","blue","black","orange","salmon","purple","grey","pink","yellow","brown","beige"]

        plt.style.use('bmh')

        fig = plt.Figure(figsize=(20,20))
        gs = fig.add_gridspec(3,1, height_ratios=(7,7,1),left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.05, hspace=0.1)

        ax_histraw = fig.add_subplot(gs[0, 0])
        ax_histdensity = fig.add_subplot(gs[1, 0], sharex=ax_histraw)
        ax_legend = fig.add_subplot(gs[2, 0])
        ax_histraw.set_title("Cumulative distribution of AED with transcript evidence, with nb of transcripts [a] or density of transcripts [b]",fontsize=20)
        if evidence == "pr":
            ax_histraw.set_title("Cumulative distribution of AED with protein evidence, with nb of transcripts [a] or density of transcripts [b]",fontsize=20)
        if evidence == "best":
            ax_histraw.set_title("Cumulative distribution of AED with best evidence (transcript or protein), with nb of transcripts [a] or density of transcripts [b]",fontsize=20)

        ax_histraw.set_xlim(0.0,1.0)
        ax_histdensity.set_xlabel("AED", fontsize=20)
        ax_histraw.set_ylabel("Nb of transcripts", fontsize=20)
        ax_histdensity.set_ylabel("Normalized Nb of transcripts", fontsize=20)
        ax_histraw.tick_params(labelsize=15)
        ax_histdensity.tick_params(labelsize=15)
        ax_histraw.text(0.05,0.95,"a",transform=ax_histraw.get_xaxis_transform(),size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax_histdensity.text(0.05,0.95,"b",transform=ax_histdensity.get_xaxis_transform(),size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        for i,src in enumerate(sources):
            laed = []
            for g in [x for x in genes if x.source == src]:
                for tr in g.lTranscripts:
                    if evidence == "tr":
                        laed.append(tr.best_tr_evidence[1])
                    if evidence == "pr":
                        laed.append(tr.best_bx_evidence[1])
                    if evidence == "best":
                        laed.append(min(tr.best_tr_evidence[1],tr.best_bx_evidence[1]))
            bins = np.arange(0.0,1.001,0.001)
            ax_histraw.hist(laed, bins=bins, cumulative=True, histtype="step", edgeColor = colors[i], label=src, linewidth=1.5)
            u = ax_histdensity.hist(laed, bins=bins, cumulative=True, histtype="step", density=True, edgeColor = colors[i], label=src, linewidth=1.5)
            logging.info("{} with {} evidences, value at 0.5 AED: {}".format(src, evidence, u[0][500]))

        h,l=ax_histraw.get_legend_handles_labels() # get labels and handles from histx  
        ax_legend.legend(h,l, fontsize=20, ncol=ncol, mode="expand", loc="lower center")
        ax_legend.grid(False)
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)

    def run(self):
        """"launch command"""

        sources = Utils.get_sources_from_fof(self.fof)
        genes = Utils.extract_genes_from_fof(self.fof)
        self.get_aed(genes)
        self.plotCumulativeAED(sources, genes, "tr","cumulative_tr_AED.png",self.ncol)
        self.plotCumulativeAED(sources, genes, "pr","cumulative_pr_AED.png",self.ncol)
        self.plotCumulativeAED(sources, genes, "best","cumulative_best_AED.png",self.ncol)
