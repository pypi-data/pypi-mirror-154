#!/usr/bin/env python3

import logging
import multiprocessing
import math
import pysam
import sys
import re
import numpy as np
import seaborn as sns
import matplotlib
import pandas as pd
import copy

import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg

from ingenannot.utils import Utils
from ingenannot.utils.gff_reader import GFF3Reader, GTFReader
from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.commands.command import Command

class Select(Command):

    def __init__(self, args):

        self.fof = args.fof
        self.output = args.Output
        self.clutype = args.clutype
        self.clustranded = args.clustranded
        self.noaed = args.noaed
#        self.nb_sources = args.nbsrc
        self.nb_sources_filtering = args.nbsrc_filter
        self.nbsrc_absolute = args.nbsrc_absolute
        self.transcript_gff_file = args.evtr
        self.transcript_gff_file_source = args.evtr_source
        self.transcript_gff_file_stranded = args.evtrstranded
        self.protein_gff_file = args.evpr
        self.protein_gff_file_source = args.evpr_source
        self.protein_gff_file_stranded = args.evprstranded
        self.aed_tr_cds_only = args.aed_tr_cds_only
        self.penalty_overflow = args.penalty_overflow
        self.aedtr_filtering = args.aedtr
        self.aedpr_filtering = args.aedpr
        self.use_ev_lg = args.use_ev_lg
        self.min_CDS_length = args.min_cds_len
        self.no_partial = args.no_partial
        self.genome_fasta_file = args.genome
        self.longread_gff_file = args.longreads
        self.longread_gff_file_source = args.longreads_source
        self.longread_penalty_overflow = args.longreads_penalty_overflow
        self.gaeval = args.gaeval
        self.prefix = args.prefix
        self.no_export = args.no_export
        self.no_cds_overlap = args.no_cds_overlap

        if self.no_partial and not self.genome_fasta_file:
            raise Exception("genome in fasta format required with no_partial genes")


    def filter_metagenes_required_number_sources(self, metagenes):
        '''filter metagenes with a minimum nb of sources'''

        logging.info("## Filtering metagenes for a required number of sources")
        logging.info("## required number of sources at least : {}".format(self.nbsrc_absolute))
        logging.info("## number of metagenes before filtering of nb sources: {}".format(len(metagenes)))

        filtered_metagenes = []
        for mg in metagenes:
            if mg.get_number_of_src() >= self.nbsrc_absolute:
                filtered_metagenes.append(mg)

        logging.info("## number of metagenes after filtering of nb sources: {}".format(len(filtered_metagenes)))

        return filtered_metagenes


    def _remove_small_cds_included(self, ltr):
        '''In some cases, a small CDS was defined
        when a longer one was predicted by another method
        This could be due to a very small fragmented transcript
        So, in case where no protein evidence support this,
        we remove the small CDS and keep the longest, if
        no penalty CDS structure
        By default only the next tr is analyzed. This prevent 
        multi deletion of protein well supported by other method
        Remove orphan model'''

        new_tr = []
        for i, tr in enumerate(ltr[:-1]):
            to_keep = True
            if tr.best_bx_evidence[1] == 1.0 and (tr.tr_penalty != 'yes' and tr.lg_penalty != 'yes') and (tr.best_tr_evidence[1] != 1.0 or tr.best_lg_evidence[1] != 1.0):
                for tr2 in ltr[i+1:i+2]:
                    if tr2.best_bx_evidence[1] == 1.0 and (tr2.tr_penalty != 'yes' and tr2.lg_penalty != 'yes') and (tr2.best_tr_evidence[1] != 1.0 or tr2.best_lg_evidence[1] != 1.0):
                        if tr2.get_min_cds_start() < tr.get_min_cds_start() or tr2.get_max_cds_end() > tr.get_max_cds_end():
                            if tr.is_cds_included_in_other_cds(tr2):
                                if self.no_partial:
                                    if not tr2.is_cds_partial(self.genome_fasta_file):
                                        logging.debug("CDS of TR: {}, {}, {} is in CDS of TR2: {}, {}, {}, removed".format(tr.id, tr.seqid, tr.start, tr2.id, tr2.seqid, tr2.start))
                                        to_keep = False
                                else:
                                    logging.debug("CDS of TR: {}, {}, {} is in CDS of TR2: {}, {}, {}, removed".format(tr.id, tr.seqid, tr.start, tr2.id, tr2.seqid, tr2.start))
                                    to_keep = False
            if to_keep:
                new_tr.append(tr)
        # add last tr
        new_tr.append(ltr[-1])
        return new_tr


    def filter(self, metagenes, nb_not_exported, coords=None):

        export_tr = []
        not_exported_tr = []

        for mg in metagenes:
            current_mg_export_tr = []
            current_mg_not_export_tr = []
            lsorted_tmp = self._rank_tr(mg.lTranscripts)


            # limit potential transcripts to coordinates (use for rescue overlapping CDS)
            lsorted = []
            if coords:
                for tr in lsorted_tmp:
                    if tr.get_min_cds_start() > coords[0] and tr.get_max_cds_end() < coords[1]:
                        lsorted.append(tr)
                lsorted_tmp = lsorted

            # new to validate
            post_filter = True
            if post_filter:
                lsorted_tmp = self._remove_small_cds_included(lsorted_tmp)


            lfilteredlen = []
            for tr in lsorted_tmp:
                if tr.getCDSTotalLength() >= self.min_CDS_length:
                    lfilteredlen.append(tr)


            lsorted = []
            if self.no_partial:
                #for tr in lsorted_tmp:
                for tr in lfilteredlen:
                    if not tr.is_cds_partial(self.genome_fasta_file):
                        lsorted.append(tr)
                    else:
                        logging.debug("Partial CDS for {}".format(tr.id))
            else:
                lsorted = lfilteredlen


            if len(lsorted) == 0:
                logging.debug("No complete CDS for MetaGene {}, not exported".format(mg.id))
                nb_not_exported += 1
                continue

            # keep first CDS (tr)
            tr = lsorted[0]
            if mg.get_number_of_src() < self.nb_sources_filtering:
                aed_tr = tr.best_tr_evidence[1]
                if self.use_ev_lg:
                    aed_tr = min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])
                if aed_tr <= self.aedtr_filtering or tr.best_bx_evidence[1] <= self.aedpr_filtering:
                    export_tr.append(tr)
                    current_mg_export_tr.append(tr)
                else:
                    nb_not_exported += 1
                    not_exported_tr.append(tr)
                    current_mg_not_export_tr.append(tr)
                    continue
            else:
                export_tr.append(tr)
                current_mg_export_tr.append(tr)

            if len(current_mg_export_tr) > 0:
                # try to rescue other CDS  if no overlap
                for i,tr in enumerate(lsorted[1::]):
                    overlap = False
                    #for j in range(0,i+1): # modif1
                    for j in current_mg_export_tr: #modif2
                        #if tr.overlap_cds_with_other_transcript_cds(lsorted[j]): #modif1
                        if tr.overlap_cds_with_other_transcript_cds(j):  #modif
                            overlap = True
                            break
                    if overlap:
                        #break #modif1
                        continue  # modif2
                    else:
                        # DEBUG
                        if mg.get_number_of_src_overlapping_tr(tr) < self.nb_sources_filtering:
                        # DEBUG: nb source at tr level , too many filtered
#                        if mg.get_number_of_src_overlapping_tr_with_tr_restrictions(tr, current_mg_export_tr) < self.nb_sources_filtering:
                          # DEBUG : too many conserved 
#                        if mg.get_number_of_src() < self.nb_sources_filtering:
                            aed_tr = tr.best_tr_evidence[1]
                            if self.use_ev_lg:
                                aed_tr = min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])
                            if aed_tr <= self.aedtr_filtering or tr.best_bx_evidence[1] <= self.aedpr_filtering:
                                export_tr.append(tr)
                                current_mg_export_tr.append(tr)
#                            else:
#                                for y in current_mg_not_export_tr:
#                                    if tr.overlap_cds_with_other_transcript_cds(y):  #modif
#                                        not_exported_tr.append(tr)
#                                        current_mg_not_export_tr.append(tr)
                        else:
                            export_tr.append(tr)
                            current_mg_export_tr.append(tr)

        logging.debug("{} metagenes not exported".format(nb_not_exported))

        return export_tr, not_exported_tr


    def export(self,allgenes, export_tr, fh):

        source = "ingenannot"
        references = list(set([x.seqid for x in allgenes]))
        Utils.natural_sort(references)

        with open(fh, 'w') as f:
            ID = 0
            for ref in references:
                seq_genes = [g for g in allgenes if g.seqid == ref]
                for tr in sorted([ t for t in export_tr if t.seqid == ref], key=lambda x: x.get_min_cds_start()):
                    for gene in seq_genes:

                        if gene.gene_id == tr.gene_id and gene.source == tr.source:
                            ID += 1
                            #atts = {'ID':['gene:{}'.format(gene.gene_id)],'source':[gene.source]}
                            atts = {'ID':['{}_{:05}'.format(self.prefix,ID)],'gene_source':[gene.gene_id],'source':['{}'.format(gene.source)]}

                            # change gene coordinates in case of selection of one isoform 
                            gene.start = tr.start
                            gene.end = tr.end

                            f.write(gene.to_gff3(atts=atts, source=source))
                            if not tr.best_tr_evidence[0]:
                                ev_tr = "None"
                            else:
                                ev_tr = tr.best_tr_evidence[0]
                            if not tr.best_bx_evidence[0]:
                                ev_bx = "None"
                            else:
                                #ev_bx = tr.best_bx_evidence[0].id
                                ev_bx = tr.best_bx_evidence[0]
    
                            #atts = {'ID':['mRNA:{}'.format(tr.id)], 'source':[gene.source],'Parent':['gene:{}'.format(gene.gene_id)], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}
                            atts = {'ID':['{}_{:05}.1'.format(self.prefix,ID)], 'transcript_source':[tr.id],'source':[gene.source],'Parent':['{}_{:05}'.format(self.prefix,ID)],'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}
    
                            #if self.longread_gff_file:
                            if not tr.best_lg_evidence[0]:
                                ev_lg = "None"
                            else:
                                #ev_lg = tr.best_lg_evidence[0].id
                                ev_lg = tr.best_lg_evidence[0]
                            atts_lg = {'ev_lg': [ev_lg], 'aed_ev_lg':['{:.4f}'.format(tr.best_lg_evidence[1])],'ev_lg_penalty':[tr.lg_penalty]}
                            atts.update(atts_lg)
    
                            f.write(tr.to_gff3(atts=atts,source=source))
    
                            for i,exon in enumerate(tr.lExons):
                                #atts = {'ID':['exon:{}.{}'.format(gene.gene_id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                                atts = {'ID':['exon:{}_{:05}.{}'.format(self.prefix,ID,i+1)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)]}
                                f.write(exon.to_gff3(atts=atts,source=source))
                            for i,cds in enumerate(tr.lCDS):
                                #atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                                atts = { 'ID':['cds:{}_{:05}.1'.format(self.prefix,ID)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)]}
                                f.write(cds.to_gff3(atts=atts,source=source))
                            break
        f.close()



#    @staticmethod
    def _rank_tr(self, transcripts):
        """double sort tr and pr, compare list, when
           discrepency, use distances"""

        l_sorted = []
        l_tr_rank = sorted(transcripts, key=lambda tr: (min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]), tr.best_bx_evidence[1]))
        l_pr_rank = sorted(transcripts, key=lambda tr: (tr.best_bx_evidence[1], min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])))
        for idx in range(0,len(transcripts)):
            tr_to_remove = None
            if l_tr_rank[0] == l_pr_rank[0]:
                tr_to_remove = l_tr_rank[0]
            elif l_tr_rank[0].best_bx_evidence[1] == l_pr_rank[0].best_bx_evidence[1]:
                tr_to_remove = l_tr_rank[0]
            else:
                if self.gaeval:
                    if l_pr_rank[0].gaeval_infos['int'] > l_tr_rank[0].gaeval_infos['int']:
                        tr_to_remove = l_pr_rank[0]
                    else:
                        tr_to_remove = l_tr_rank[0]
                else:
                    tr_delta = l_pr_rank[0].best_tr_evidence[1] - l_tr_rank[0].best_tr_evidence[1]
                    # add stronger weigth on protein distance 
#                    pr_delta = (l_tr_rank[0].best_bx_evidence[1] - l_pr_rank[0].best_bx_evidence[1]) * 1.5
                    pr_delta = l_tr_rank[0].best_bx_evidence[1] - l_pr_rank[0].best_bx_evidence[1]

                    # To validate BUG ? order
                    if tr_delta >= pr_delta:
                        tr_to_remove = l_tr_rank[0]
                    else:
                        tr_to_remove = l_pr_rank[0]
            l_sorted.append(tr_to_remove)
            l_tr_rank.remove(tr_to_remove)
            l_pr_rank.remove(tr_to_remove)

        return l_sorted



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
                if "aed_ev_lg" in tr.dAttributes and "ev_lg" in tr.dAttributes:
                    tr.best_lg_evidence = (tr.dAttributes["ev_lg"][0],float(tr.dAttributes["aed_ev_lg"][0]))

                if "ev_lg_penalty" in tr.dAttributes:
                    tr.lg_penalty = tr.dAttributes["ev_lg_penalty"][0]
                if "ev_tr_penalty" in tr.dAttributes:
                    tr.tr_penalty = tr.dAttributes["ev_tr_penalty"][0]

    def get_values_for_scatter_hist(self, transcripts):

        l_aed_tr = []
        l_aed_tr_no_penalty = []
        l_aed_pr = []
        l_aed_pr_no_penalty = []

        for tr in transcripts:
            l_aed_pr.append(tr.best_bx_evidence[1])
            if self.use_ev_lg:
                l_aed_tr.append(min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
            else:
                l_aed_tr.append(tr.best_tr_evidence[1])

            if tr.tr_penalty != 'yes' and tr.lg_penalty != 'yes':
                l_aed_pr_no_penalty.append(tr.best_bx_evidence[1])
                if self.use_ev_lg:
                    l_aed_tr_no_penalty.append(min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
                else:
                    l_aed_tr_no_penalty.append(tr.best_tr_evidence[1])


        return l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty



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
        ax.vlines(self.aedtr_filtering, 0, 1, transform=ax.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax.text(self.aedtr_filtering,0.9,self.aedtr_filtering,size=20,ha="center", va="center", color='r',bbox=dict(boxstyle="round",fc='#EEEEEE'))
        ax.hlines(self.aedpr_filtering, 0, 1, transform=ax.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax.text(0.9,self.aedpr_filtering,self.aedpr_filtering,size=20,ha="center", va="center", color='r', bbox=dict(boxstyle="round",fc='#EEEEEE'))

        lb,rb,lt,rt = 0,0,0,0
        lb_no_penalty,rb_no_penalty,lt_no_penalty,rt_no_penalty = 0,0,0,0

        for i,val in enumerate(laed[0]):
            if laed[0][i] <= self.aedtr_filtering and laed[1][i] <= self.aedpr_filtering:
                lb += 1
            if laed[0][i] > self.aedtr_filtering and laed[1][i] <= self.aedpr_filtering:
                rb += 1
            if laed[0][i] <= self.aedtr_filtering and laed[1][i] > self.aedpr_filtering:
                lt += 1
            if laed[0][i] > self.aedtr_filtering and laed[1][i] > self.aedpr_filtering:
                rt += 1
        ax.text(self.aedtr_filtering/2,self.aedpr_filtering/2,lb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr_filtering)/2),self.aedpr_filtering/2,rb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(self.aedtr_filtering/2,1-((1-self.aedpr_filtering)/2),lt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr_filtering)/2),1-((1-self.aedpr_filtering)/2),rt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        for i,val in enumerate(laed[2]):
            if laed[2][i] <= self.aedtr_filtering and laed[3][i] <= self.aedpr_filtering:
                lb_no_penalty += 1
            if laed[2][i] > self.aedtr_filtering and laed[3][i] <= self.aedpr_filtering:
                rb_no_penalty += 1
            if laed[2][i] <= self.aedtr_filtering and laed[3][i] > self.aedpr_filtering:
                lt_no_penalty += 1
            if laed[2][i] > self.aedtr_filtering and laed[3][i] > self.aedpr_filtering:
                rt_no_penalty += 1

            ax.text(self.aedtr_filtering/2,self.aedpr_filtering/2-0.05,lb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-self.aedtr_filtering)/2),self.aedpr_filtering/2-0.05,rb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(self.aedtr_filtering/2,1-((1-self.aedpr_filtering)/2)-0.05,lt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-self.aedtr_filtering)/2),1-((1-self.aedpr_filtering)/2)-0.05,rt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0.0,0,0), fc=(.5, 1., 1.)))

        ax.set_xlabel("AED with transcript evidence", fontsize=20)
        ax.set_ylabel("AED with protein evidence", fontsize=20)
        ax.tick_params(labelsize=15)

        #ax.margins(0.02)
        #ax.set_xlim((0,1))
        #ax.set_ylim((0,1))

        bins = np.arange(0.0,1.01,0.01)
        ax_histx.hist(laed[0], bins=bins, color = '#36953a', edgecolor = 'black', label="AED transcripts")
        ax_histx.vlines(self.aedtr_filtering, 0, 1, transform=ax_histx.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax_histx.tick_params(labelsize=12)
        ax_histx.set_ylabel("Nb. Transcripts", fontsize=20)
        #ax_histx.legend(fontsize=20)
        ax_histy.hist(laed[1], bins=bins, color = '#fc4b67', edgecolor = 'black', orientation='horizontal', label="AED proteins")
        ax_histy.hlines(self.aedpr_filtering, 0, 1, transform=ax_histy.get_yaxis_transform(), colors='r', linestyle="dashed")
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

        logging.info("Scatter plot exported in {}".format(out))




    def run(self):
        """"launch command"""

        if not self.noaed:
            if not self.transcript_gff_file:
                raise Exception("missing transcript evidence file: set --evtr parameter")
            if not self.protein_gff_file:
                raise Exception("missing protein evidence file: set --evpr parameter")


        sources = Utils.get_sources_from_fof(self.fof)
        genes = Utils.extract_genes_from_fof(self.fof)

        if self.noaed:
            self.get_aed(genes)
        if self.gaeval:
            gaeval_infos = Utils.extract_gaeval_from_fof(self.fof)
            Utils.add_gaeval_infos_to_transcripts(genes, gaeval_infos)


        clusters = Utils.clusterize(genes, cltype=self.clutype, stranded=self.clustranded, procs=Command.NB_CPUS)
        metagenes = Utils.get_metagenes_from_clusters(clusters)
        nb_metagenes = len(metagenes)
        ##debug
        if self.nbsrc_absolute > 1:
            metagenes = self.filter_metagenes_required_number_sources(metagenes)
        nb_removed_metagenes = nb_metagenes - len(metagenes)

        if not self.noaed:
#           metagenes = self.compute_aed_with_transcripts(metagenes, procs=Command.NB_CPUS)
            metagenes = AnnotEditDistance.compute_aed(metagenes, self.transcript_gff_file, self.transcript_gff_file_stranded, self.transcript_gff_file_source, self.penalty_overflow, evtype="tr", cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)
#            metagenes = self.compute_aed_with_proteins(metagenes, procs=Command.NB_CPUS)
            metagenes = AnnotEditDistance.compute_aed(metagenes, self.protein_gff_file, self.protein_gff_file_stranded, self.protein_gff_file_source, 0.0, evtype="pr", procs=Command.NB_CPUS)

            if self.longread_gff_file:
#                metagenes = self.compute_aed_with_longread_transcripts(metagenes,procs=Command.NB_CPUS)

                metagenes = AnnotEditDistance.compute_aed(metagenes, self.longread_gff_file, True, self.longread_gff_file_source, self.longread_penalty_overflow, evtype="lg", cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)

        transcripts, transcripts_not_exported = self.filter(metagenes, nb_removed_metagenes)

        if self.no_cds_overlap:
            logging.info("Analyzing CDS overlap")
            transcripts, strfr_transcripts_not_exported = self.aed_strand_filter(transcripts)
            nb_rescue = 0
            for strfr in strfr_transcripts_not_exported:
                rescue_tr = self.rescue_tr_overlapping_cds(strfr, metagenes, transcripts)
                if rescue_tr:
                    nb_rescue += 1
                    logging.debug("RESCUE {} instead of {}".format(rescue_tr[0].id, strfr.id))
                    transcripts.append(rescue_tr[0])
                else:

                    #transcripts_not_exported.extend(strfr_transcripts_not_exported)
                    transcripts_not_exported.append(strfr)

            # rescue transcript if a non-overlapp

            logging.info("{} transcripts rescued after overlapping with other CDS".format(nb_rescue))


        l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty = self.get_values_for_scatter_hist(transcripts)


        self.scatter_hist([l_aed_tr, l_aed_pr, l_aed_tr_no_penalty, l_aed_pr_no_penalty], "{}.scatter_hist_aed.png".format(self.output),legend=['aed_tr','aed_pr'], title="all runs - density of aed")
        
        self.export(genes,transcripts,self.output)
        if self.no_export :
            self.export(genes,transcripts_not_exported,"no-export.{}".format(self.output))

        return 0


    def aed_strand_filter(self, transcripts):

        conflict_list = []
        transcripts_not_exported = []

        tr_dict = {}
        references = set([tr.seqid for tr in transcripts])
        for ref in references:
            ref_tr = sorted([tr for tr in transcripts if tr.seqid == ref], key=lambda x: x.get_min_cds_start())
            for i,tr in enumerate(ref_tr[:-1]):
                    tr_dict[(tr.id,tr.source)] = tr
                    for tr2 in ref_tr[i+1:]:
                      if tr.is_feature_spanning(tr2):
                        if tr.overlap_cds_with_other_transcript_cds(tr2):
                            conflict_list.append(((tr.id,tr.source), (tr2.id,tr2.source)))

            # add last tr in dict
            tr_dict[(ref_tr[-1].id,ref_tr[-1].source)] = ref_tr[-1]

        logging.info("{} potential conflicts to resolved".format(len(conflict_list)))

        list_to_remove = []
        for cf in conflict_list:
            #l = self._rank_tr_score([tr_dict[cf[0]],tr_dict[cf[1]]])
            l = self._rank_tr([tr_dict[cf[0]],tr_dict[cf[1]]])
            if l[0] not in list_to_remove:
                list_to_remove.append(l[1])

#        self.export(genes, list_to_remove)
        new_transcripts = []
#        not_exported = 0
        for tr in transcripts:
            if tr not in list_to_remove:
                new_transcripts.append(tr)
            else:
#                not_exported += 1
                transcripts_not_exported.append(tr)

        logging.info("{} transcripts removed due to overlapping with other CDS".format(len(transcripts_not_exported)))

        return new_transcripts, transcripts_not_exported


    def rescue_tr_overlapping_cds(self, tr, metagenes, transcripts):

        tr_before = None
        tr_after = None

        transcripts_sorted = sorted([ tt for tt in transcripts if tt.seqid == tr.seqid ], key=lambda x: x.get_min_cds_start()) 

        for i,t in enumerate(transcripts_sorted[:-1]):
            if tr.get_min_cds_start() > transcripts_sorted[i].get_min_cds_start() and tr.get_max_cds_end() < transcripts_sorted[i+1].get_max_cds_end():
                tr_before = transcripts_sorted[i]
                tr_after = transcripts_sorted[i+1]
        if not tr_before or not tr_after:
            return None
        meta = None
        for m in metagenes:
            if tr in m.lTranscripts:
                meta = copy.deepcopy(m)
                break
        filtered_tr = []
        for tr in meta.lTranscripts:
            if tr.get_min_cds_start() > tr_before.get_max_cds_end() and tr.get_max_cds_end() < tr_after.get_min_cds_start():
                filtered_tr.append(tr)

        if len(filtered_tr) == 0:
            return None

        tr_filt, tr_filt_not_exported = self.filter([meta], 0, coords=(tr_before.get_max_cds_end(),tr_after.get_min_cds_start()))
        if tr_filt:
            return tr_filt
