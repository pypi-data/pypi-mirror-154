#/usr/bin/env python3

import logging
import multiprocessing
import math
import pysam
import sys
from ingenannot.utils import Utils
from ingenannot.utils.gff_reader import GFF3Reader,GTFReader
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


class AED(Command):

    def __init__(self, args):

        self.input = args.Input
        self.output = args.Output
        self.source = args.source
        self.transcript_gff_file = args.evtr
        self.transcript_gff_file_source = args.evtr_source
        self.transcript_gff_file_stranded = args.evtrstranded
        self.protein_gff_file = args.evpr
        self.protein_gff_file_source = args.evpr_source
        self.protein_gff_file_stranded = args.evprstranded
        self.penalty_overflow = args.penalty_overflow
        self.longread_gff_file = args.longreads
        self.longread_gff_file_source = args.longreads_source
        self.longread_penalty_overflow = args.longreads_penalty_overflow
        self.aedtr = args.aedtr
        self.aedpr = args.aedpr
        self.aed_tr_cds_only = args.aed_tr_cds_only

    def export(self, allgenes):

        with open(self.output, 'w') as f:
            #for tr in sorted(export_tr, key=lambda x: x.start):
            for gene in allgenes:
                    #if gene.gene_id == tr.gene_id and gene.source == tr.source:
#                atts = {'ID':['gene:{}'.format(gene.gene_id)],'source':[gene.source]}
                atts = {'ID':[gene.gene_id],'source':[gene.source]}
                f.write(gene.to_gff3(atts=atts))
                for tr in gene.lTranscripts:
                    if not tr.best_tr_evidence[0]:
                        ev_tr = "None"
                    else:
                        #ev_tr = tr.best_tr_evidence[0].id
                        ev_tr = tr.best_tr_evidence[0]
                    if not tr.best_bx_evidence[0]:
                        ev_bx = "None"
                    else:
                        #ev_bx = tr.best_bx_evidence[0].id
                        ev_bx = tr.best_bx_evidence[0]

#                    atts = {'ID':['mRNA:{}'.format(tr.id)], 'source':[gene.source],'Parent':['gene:{}'.format(gene.gene_id)], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}
                    atts = {'ID':[tr.id], 'source':[gene.source],'Parent':[gene.gene_id], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}

                    if self.longread_gff_file:
                        if not tr.best_lg_evidence[0]:
                            ev_lg = "None"
                        else:
                            ev_lg = tr.best_lg_evidence[0]
                        atts_lg = {'ev_lg': [ev_lg], 'aed_ev_lg':['{:.4f}'.format(tr.best_lg_evidence[1])],'ev_lg_penalty':[tr.lg_penalty]}
                        atts.update(atts_lg)

                    f.write(tr.to_gff3(atts=atts))
                    for i,exon in enumerate(tr.lExons):
#                        atts = {'ID':['exon:{}.{}-{}'.format(gene.gene_id,i+1,gene.source)], 'source':[gene.source],'Parent':['mRNA:{}-{}'.format(gene.gene_id,gene.source)]}
#                        atts = {'ID':['exon:{}'.format(exon.exon_id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                        atts = {'ID':[exon.exon_id], 'source':[gene.source],'Parent':[",".join(exon.lTranscript_ids)]}
                        f.write(exon.to_gff3(atts=atts))
                    for i,cds in enumerate(tr.lCDS):
#                        atts = {'ID':['cds:{}-{}'.format(gene.gene_id,gene.source)], 'source':[gene.source],'Parent':['mRNA:{}-{}'.format(gene.gene_id,gene.source)]}
#                        atts = {'ID':['cds:{}'.format(cds.cds_id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                        atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                        f.write(cds.to_gff3(atts=atts))
        f.close()

    def get_aed(self, genes):
        l_aed_tr = []
        l_aed_pr = []
        for g in genes:
            for tr in g.lTranscripts:
                l_aed_tr.append(min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
                l_aed_pr.append(tr.best_bx_evidence[1])

        return l_aed_tr, l_aed_pr


    def scatter_hist(self, laed, out="", legend="", title=""):
        """scatter plot of AEDs with histograms"""

        plt.style.use('bmh')
        #plt.style.use('seaborn')
        #plt.style.use('ggplot')

        fig = plt.Figure(figsize=(20,20))
        # add gridspec
        gs = fig.add_gridspec(2,2,width_ratios=(7, 2), height_ratios=(2, 7),
                                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                                                            wspace=0.05, hspace=0.05)
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_legend = fig.add_subplot(gs[0, 1])

        ax.scatter(laed[0],laed[1], color="#20C2EF")
        # By using ``transform=vax.get_xaxis_transform()`` the y coordinates are scaled
        # such that 0 maps to the bottom of the axes and 1 to the top.
        ax.vlines(self.aedtr, 0, 1, transform=ax.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax.text(self.aedtr,0.9,self.aedtr,size=20,ha="center", va="center", color='r',bbox=dict(boxstyle="round",fc='#EEEEEE'))
        ax.hlines(self.aedpr, 0, 1, transform=ax.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax.text(0.9,self.aedpr,self.aedpr,size=20,ha="center", va="center", color='r', bbox=dict(boxstyle="round",fc='#EEEEEE'))

        lb,rb,lt,rt = 0,0,0,0

        for i,val in enumerate(laed[0]):
            if laed[0][i] <= self.aedtr and laed[1][i] <= self.aedpr:
                lb += 1
            if laed[0][i] > self.aedtr and laed[1][i] <= self.aedpr:
                rb += 1
            if laed[0][i] <= self.aedtr and laed[1][i] > self.aedpr:
                lt += 1
            if laed[0][i] > self.aedtr and laed[1][i] > self.aedpr:
                rt += 1

        ax.text(self.aedtr/2,self.aedpr/2,lb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr)/2),self.aedpr/2,rb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(self.aedtr/2,1-((1-self.aedpr)/2),lt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr)/2),1-((1-self.aedpr)/2),rt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        ax.set_xlabel("AED with transcript evidence", fontsize=20)
        ax.set_ylabel("AED with protein evidence", fontsize=20)
        ax.tick_params(labelsize=15)

        #ax.margins(0.02)
        #ax.set_xlim((0,1))
        #ax.set_ylim((0,1))

        bins = np.arange(0.0,1.01,0.01)
        ax_histx.hist(laed[0], bins=bins, color = '#36953a', edgecolor = 'black', label="AED transcripts")
        ax_histx.vlines(self.aedtr, 0, 1, transform=ax_histx.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax_histx.tick_params(labelsize=12)
        ax_histx.set_ylabel("Nb. Transcripts", fontsize=20)
        #ax_histx.legend(fontsize=20)
        ax_histy.hist(laed[1], bins=bins, color = '#fc4b67', edgecolor = 'black', orientation='horizontal', label="AED proteins")
        ax_histy.hlines(self.aedpr, 0, 1, transform=ax_histy.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax_histy.tick_params(labelsize=12)
        ax_histy.set_xlabel("Nb. Transcripts", fontsize=20)
        #ax_histy.legend(fontsize=20)

        h,l=ax_histx.get_legend_handles_labels() # get labels and handles from histx  
        hy,ly=ax_histy.get_legend_handles_labels() # get labels and handles from histy
        h.extend(hy)
        l.extend(ly)
        ax_legend.legend(h,l, fontsize=20)
        # Hide grid lines
        ax_legend.grid(False)
        # Hide axes ticks
        #ax_legend.set_xticks([])
        #ax_legend.set_yticks([])
        # change background color
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')

        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)



    def run(self):
        """"launch command"""

        genes = Utils.extract_genes(self.input, True, self.source)

        genes = AnnotEditDistance.compute_aed(genes, self.transcript_gff_file, self.transcript_gff_file_stranded, self.transcript_gff_file_source, self.penalty_overflow, evtype="tr", cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)
        genes = AnnotEditDistance.compute_aed(genes, self.protein_gff_file, self.protein_gff_file_stranded, self.protein_gff_file_source, 0.0, evtype="pr",cds_only=True, procs=Command.NB_CPUS)

        if self.longread_gff_file:
            genes = AnnotEditDistance.compute_aed(genes, self.longread_gff_file, True, self.longread_gff_file_source, self.longread_penalty_overflow, evtype="lg",cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)

        self.export(genes)
        l_aed_tr, l_aed_pr = self.get_aed(genes)
        self.scatter_hist([l_aed_tr, l_aed_pr], "scatter_hist_aed.{}.png".format(self.source),legend=['aed_tr','aed_pr'], title="None")

        return 0
