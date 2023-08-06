#!/usr/bin/env python3

import logging
import pysam

from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.gff_reader import GTFReader, GFF3Reader
from ingenannot.utils.annot_edit_distance import AnnotEditDistance

class ComputeAED():
    """
    pass
    """

    def __init__(self):
        pass

    def compute_aed(genes, gff_file, stranded, source, penalty_overflow, evtype="tr",procs=1):
        '''compute aedpr'''

        if procs > 1:
            ratio = 100
            pool = multiprocessing.Pool(procs)
            results = [pool.apply_async(ComputeAED._aed_job, (genes[i:i + ratio],gff_file,stranded, source, penalty_overflow, evtype, idx+1, len(range(0, len(genes), ratio)))) for idx,i in enumerate(range(0, len(genes), ratio))]
            new_genes = []
            for i,r in enumerate(results):
                r_genes = r.get()
                new_genes.extend(r_genes)
            genes = new_genes

        else:
            genes = ComputeAED._aed_job(genes,gff_file, stranded, source, penalty_overflow, evtype, 1,1)

        return genes

    def _aed_job(genes, transcript_file, stranded=False, source="unknown", penalty_overflow=0.0, evtype="tr", idx=1, tot=1):

        message_type = {"tr":"Transcriptomic", "lg":"Long reads based transcriptomic", "pr":"Proteomic"}
        logging.info("Starting {} evidence analysis {}/{}".format(message_type[evtype],idx, tot))
        tbx = pysam.TabixFile(transcript_file)
        # default gtf (tr and lg type)
        builder = GeneBuilder('gtf')
        if evtype == "pr":
            builder = GeneBuilder('gff3-blastx')

        for g in genes:
            features = []

            if g.seqid not in tbx.contigs:
                continue

            min_start = [g.start-1]
            max_end = [g.end]
            for row in tbx.fetch(g.seqid, g.start-1, g.end):
                min_start.append(int(row.split("\t")[3]))
                max_end.append(int(row.split("\t")[4]))
            for row in tbx.fetch(g.seqid, min(min_start), max(max_end)):
                if evtype == "pr":
                    features.append(GFF3Reader.convertRowToFeature(str(row)))
                else:
                    features.append(GTFReader.convertRowToFeature(str(row)))
            if len(features) > 0:
                evidence_genes = builder.build_all_genes(features, coding_only=True, source=source)
                for tr in g.lTranscripts :
                    best_aed = 1.0
                    for eg in evidence_genes:
                        if stranded:
                            if tr.strand != eg.strand:
                                continue
                        for gt in eg.lTranscripts:
                            flag_penalty = False
                            if evtype == "pr":
                                aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=True, t2_no_utr=True)
                                if aed < best_aed:
                                    tr.best_bx_evidence = (gt.id,aed)
                                    best_aed = aed
                            else:
                                aed = 1.0
                                if evtype == "tr":
                                    aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=True, t2_no_utr=False)
                                if evtype == "lg":
                                    aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=False, t2_no_utr=False)
                                if penalty_overflow > 0.0 and aed < 1.0:
                                    if tr.get_nb_specific_bases_vs_another_transcript(gt,self_no_utr=True) > 0 or gt.get_nb_specific_bases_vs_another_transcript_specific_positions(tr,tr.get_min_cds_start(),tr.get_max_cds_end(), other_no_utr=True) > 0:
                                        aed += self.penalty_overflow
                                        flag_penalty = True
                                if aed < best_aed:
                                    penalty = "undef"
                                    if penalty_overflow > 0.0:
                                        if flag_penalty :
                                            penalty = "yes"
                                        else:
                                            penalty = "no"
                                    if evtype == "tr":
                                        tr.best_tr_evidence = (gt.id,aed)
                                        tr.tr_penalty = penalty
                                    if evtype == "lg":
                                        tr.best_lg_evidence = (gt.id,aed)
                                        tr.lg_penalty = penalty
                                    best_aed = aed
        logging.info("{} evidence analyzed {}/{}".format(message_type[evtype],idx,tot))
        return genes

#
#    def compute_aed_with_longread_transcripts(self, genes, procs=1):
#        '''compute aed longread tr'''
#
#        if procs > 1:
#            ratio = 100
#            pool = multiprocessing.Pool(procs)
#            results = [pool.apply_async(self._aed_with_longread_transcripts, (genes[i:i + ratio],self.longread_gff_file,True, idx+1, len(range(0, len(genes), ratio)))) for idx,i in enumerate(range(0, len(genes), ratio))]
#            new_genes = []
#            for i,r in enumerate(results):
#                r_genes = r.get()
#                new_genes.extend(r_genes)
#            genes = new_genes
#
#        else:
#            genes = self._aed_with_longread_transcripts(genes,self.longread_gff_file, True, 1,1)
#
#        return genes
#
#    def _aed_with_longread_transcripts(self, genes, transcript_file,stranded=True, idx=1, tot=1):
#
#        logging.info("Starting longreads based transcriptomic evidences analysis {}/{}".format(idx, tot))
#        tbx = pysam.TabixFile(transcript_file)
#        builder = GeneBuilder('gtf')
#
#        for g in genes:
#            features = []
#
#            if g.seqid not in tbx.contigs:
#                continue
#
#            min_start = [g.start-1]
#            max_end = [g.end]
#            for row in tbx.fetch(g.seqid, g.start-1, g.end):
#                min_start.append(int(row.split("\t")[3]))
#                max_end.append(int(row.split("\t")[4]))
#            for row in tbx.fetch(g.seqid, min(min_start), max(max_end)):
#                features.append(GTFReader.convertRowToFeature(str(row)))
#            if len(features) > 0:
#                evidence_genes = builder.build_all_genes(features, coding_only=False, source=self.transcript_gff_file_source)
#                for tr in g.lTranscripts :
#                    best_aed = 1.0
#                    for eg in evidence_genes:
#                        if stranded:
#                            if tr.strand != eg.strand:
#                                continue
#                        for gt in eg.lTranscripts:
#                            flag_penalty = False
#                            aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=False, t2_no_utr=False)
#                            if self.longread_penalty_overflow > 0.0 and aed < 1.0:
#                                if tr.get_nb_specific_bases_vs_another_transcript(gt,self_no_utr=True) > 0 or gt.get_nb_specific_bases_vs_another_transcript_specific_positions(tr,tr.get_min_cds_start(),tr.get_max_cds_end(), other_no_utr=True) > 0:
#                                    aed += self.longread_penalty_overflow
#                                    flag_penalty = True
#                            if aed < best_aed:
#                                tr.best_lg_evidence = (gt.id,aed)
#                                if self.longread_penalty_overflow > 0.0:
#                                    if flag_penalty :
#                                        tr.lg_penalty = "yes"
#                                    else:
#                                        tr.lg_penalty = "no"
#                                best_aed = aed
#        logging.info("Longreads based transcriptomic evidences analyzed {}/{}".format(idx,tot))
#
#        return genes
#
#
#    def compute_aed_with_proteins(self, genes, procs=1):
#        '''compute aedpr'''
#
#        if procs > 1:
#            ratio = 100
#            pool = multiprocessing.Pool(procs)
#            results = [pool.apply_async(self._aed_with_proteins, (genes[i:i + ratio],self.protein_gff_file,self.protein_gff_file_stranded, idx+1, len(range(0, len(genes), ratio)))) for idx,i in enumerate(range(0, len(genes), ratio))]
#            new_genes = []
#            for i,r in enumerate(results):
#                r_genes = r.get()
#                new_genes.extend(r_genes)
#            genes = new_genes
#
#        else:
#            genes = self._aed_with_proteins(genes,self.protein_gff_file, self.protein_gff_file_stranded, 1,1)
#
#        return genes
#
#    def _aed_with_proteins(self, genes, blastx_file,stranded=False, idx=1, tot=1):
#
#        logging.info("Starting proteomic evidences analysis {}/{}".format(idx, tot))
#        tbx = pysam.TabixFile(blastx_file)
#        builder = GeneBuilder('gff3-blastx')
#
#        for g in genes:
#            features = []
#
#            if g.seqid not in tbx.contigs:
#                continue
#
#            # select all feat coords
#            min_start = [g.start-1]
#            max_end = [g.end]
#            for row in tbx.fetch(g.seqid, g.start-1, g.end):
#                min_start.append(int(row.split("\t")[3]))
#                max_end.append(int(row.split("\t")[4]))
#            # reselect base on extrem coord (to be sure to have all exons) 
#            for row in tbx.fetch(g.seqid, min(min_start), max(max_end)):
#
#                features.append(GFF3Reader.convertRowToFeature(str(row)))
#            if len(features) > 0:
#                evidence_genes = builder.build_all_genes(features, coding_only=True, source=self.protein_gff_file_source)
#                for tr in g.lTranscripts :
#                    best_aed = 1.0
#                    for eg in evidence_genes:
#                        if stranded:
#                            if tr.strand != eg.strand:
#                                continue
#                        for gt in eg.lTranscripts:
#                            aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=True, t2_no_utr=True)
#                            if aed < best_aed:
#                                tr.best_bx_evidence = (gt.id,aed)
#                                best_aed = aed
#        logging.info("Proteomic evidences analyzed {}/{}".format(idx,tot))
#        return genes
#
#
