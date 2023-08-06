#!/usr/bin/env python3

import logging
import pysam
import multiprocessing

from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.gff_reader import GTFReader, GFF3Reader


class AnnotEditDistance():
    """
    utility class computing necessary
    methods to provide AED between genes
    or transcipts
    """

    def __init__(self):
        """pass"""

    @staticmethod
    def sensitivity(t1, t2, t1_no_utr=False, t2_no_utr=False):
        """
        Compute sensitivity between 2 transcripts
        """

        if (t1.get_nb_shared_bases_with_another_transcript(t2, t1_no_utr, t2_no_utr) + t2.get_nb_specific_bases_vs_another_transcript(t1, t2_no_utr, t1_no_utr)) == 0:
            return 0
        else:
            return  t1.get_nb_shared_bases_with_another_transcript(t2, t1_no_utr, t2_no_utr) / (t1.get_nb_shared_bases_with_another_transcript(t2, t1_no_utr, t2_no_utr) + t2.get_nb_specific_bases_vs_another_transcript(t1, t2_no_utr, t1_no_utr))

    @staticmethod
    def specificity(t1, t2, t1_no_utr=False, t2_no_utr=False):
        """
        Compute specificity between 2 transcripts
        """

        return  t1.get_nb_shared_bases_with_another_transcript(t2, t1_no_utr, t2_no_utr) / (t1.get_nb_shared_bases_with_another_transcript(t2, t1_no_utr, t2_no_utr) + t1.get_nb_specific_bases_vs_another_transcript(t2, t1_no_utr, t2_no_utr))

    @staticmethod
    def accuracy(t1, t2, t1_no_utr=False, t2_no_utr=False):
        """
        Compute accuracy
        """

        return (AnnotEditDistance.sensitivity(t1,t2,t1_no_utr,t2_no_utr) + AnnotEditDistance.specificity(t1,t2,t1_no_utr,t2_no_utr))/2

    @staticmethod
    def incongruence(t1, t2, t1_no_utr=False, t2_no_utr=False):
        """
        Compute incongruence/distance between 2 transcripts
        """

        return 1 - AnnotEditDistance.accuracy(t1,t2,t1_no_utr,t2_no_utr)

    @staticmethod
    def annot_edit_distance_between_2_gene_releases(g1, g2):
        """
        Compute AED for 2 annotation releases
        It takes into account alternative transcripts
        and the AED is computed based on closest
        distance/incongruence between transcripts
        """

        distances = []
        for t1 in g1.lTranscripts:
            distance = 1.0
            for t2 in g2.lTranscripts:
                distance = min(distance, AnnotEditDistance.incongruence(t1,t2))
            distances.append(distance)

        if distances:
            return sum(distances) / len(distances)
        else:
            return 1.0

    @staticmethod
    def compute_aed(genes, gff_file, stranded, source, penalty_overflow, evtype="tr",cds_only=False, procs=1):
        '''compute aedpr'''

        if procs > 1:
            ratio = 100
            pool = multiprocessing.Pool(procs)
            results = [pool.apply_async(AnnotEditDistance._aed_job, (genes[i:i + ratio],gff_file,stranded, source, penalty_overflow, evtype, cds_only, idx+1, len(range(0, len(genes), ratio)))) for idx,i in enumerate(range(0, len(genes), ratio))]
            new_genes = []
            for i,r in enumerate(results):
                r_genes = r.get()
                new_genes.extend(r_genes)
            genes = new_genes
            pool.close()
            pool.join()

        else:
            genes = AnnotEditDistance._aed_job(genes,gff_file, stranded, source, penalty_overflow, evtype, cds_only, 1,1)

        return genes

    def _aed_job(genes, transcript_file, stranded=False, source="unknown", penalty_overflow=0.0, evtype="tr", cds_only=False, idx=1, tot=1):

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
                                if evtype == "tr" or evtype == "lg":
                                    if cds_only:
                                        aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=True, t2_no_utr=False)
                                    else:
                                        aed = min(AnnotEditDistance.incongruence(tr,gt, t1_no_utr=True, t2_no_utr=False),
                                        AnnotEditDistance.incongruence(tr,gt, t1_no_utr=False, t2_no_utr=False))
                                #if evtype == "lg":
                                #    aed = AnnotEditDistance.incongruence(tr,gt, t1_no_utr=False, t2_no_utr=False)
                                if penalty_overflow > 0.0 and aed < 1.0:
                                    if tr.get_nb_specific_bases_vs_another_transcript(gt,self_no_utr=True) > 0 or gt.get_nb_specific_bases_vs_another_transcript_specific_positions(tr,tr.get_min_cds_start(),tr.get_max_cds_end(), other_no_utr=True) > 0:
                                        aed += penalty_overflow
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


