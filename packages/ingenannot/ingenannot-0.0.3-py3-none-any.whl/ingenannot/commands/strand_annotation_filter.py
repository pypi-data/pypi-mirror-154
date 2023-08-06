#/usr/bin/env python3

import logging
import sys
from  ingenannot.utils import Utils
from ingenannot.commands.command import Command

class StrandAnnotationFilter(Command):

    def __init__(self, args):

        self.input = args.Input
        self.output = args.Output

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

    def _rank_tr(self, transcripts):
        """double sort tr and pr, compare list, when
           discrepency, use distances"""

        l_sorted = []
        l_tr_rank = sorted(transcripts, key=lambda tr: min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
        l_pr_rank = sorted(transcripts, key=lambda tr: tr.best_bx_evidence[1])
        for idx in range(0,len(transcripts)):
            tr_to_remove = None
            if l_tr_rank[0] == l_pr_rank[0]:
                tr_to_remove = l_tr_rank[0]
            elif l_tr_rank[0].best_bx_evidence[1] == l_pr_rank[0].best_bx_evidence[1]:
                tr_to_remove = l_tr_rank[0]
            else:
                tr_delta = l_pr_rank[0].best_tr_evidence[1] - l_tr_rank[0].best_tr_evidence[1]
                pr_delta = l_tr_rank[0].best_bx_evidence[1] - l_pr_rank[0].best_bx_evidence[1]
                if tr_delta >= pr_delta:
                    tr_to_remove = l_tr_rank[0]
                else:
                    tr_to_remove = l_pr_rank[0]
            l_sorted.append(tr_to_remove)
            l_tr_rank.remove(tr_to_remove)
            l_pr_rank.remove(tr_to_remove)

        return l_sorted



    def export(self, allgenes, list_to_remove):

        with open(self.output, 'w') as f:

            for gene in allgenes:
                flag_remove = False
                for tr in gene.lTranscripts:
                    if tr in list_to_remove:
                        # TODO: need to implement removing only the bad transcript if
                        # isoforms, and recompute gene coords
                        # for instance one bad CDS imply removing of the whole gene
                        logging.info("removing gene {} and all transcripts".format(gene.gene_id))
                        flag_remove = True
                        break
                if not flag_remove:
                    #atts = {'ID':['gene:{}'.format(gene.gene_id)],'source':[gene.source]}
                    atts = {'ID':[gene.gene_id],'source':[gene.source]}
                    f.write(gene.to_gff3(atts=atts))
                    #print(gene.gene_id, gene.start, gene.end)
                    for tr in gene.lTranscripts:
                        if not tr.best_tr_evidence[0]:
                            ev_tr = "None"
                        else:
                            ev_tr = tr.best_tr_evidence[0]
                        if not tr.best_bx_evidence[0]:
                            ev_bx = "None"
                        else:
                            ev_bx = tr.best_bx_evidence[0]
                        atts = tr.dAttributes
                        #atts_id = {'ID': ['mRNA:{}'.format(tr.id)],'Parent':['gene:{}'.format(gene.gene_id)]}
                        atts_id = {'ID': [tr.id],'Parent':[gene.gene_id]}
                        atts.update(atts_id)
                        #atts = {'ID':['mRNA:{}'.format(tr.id)], 'source':[gene.source],'Parent':['gene:{}'.format(gene.gene_id)], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}

                        if not tr.best_lg_evidence[0]:
                            ev_lg = "None"
                        else:
                            ev_lg = tr.best_lg_evidence[0]
                        atts_lg = {'ev_lg': [ev_lg], 'aed_ev_lg':['{:.4f}'.format(tr.best_lg_evidence[1])],'ev_lg_penalty':[tr.lg_penalty]}
                        atts.update(atts_lg)

                        f.write(tr.to_gff3(atts=atts))
                        for i,exon in enumerate(tr.lExons):
                            #atts = {'ID':['exon:{}.{}'.format(gene.gene_id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['exon:{}.{}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['exon:{}.{}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':['{}'.format(tr.id)]}
                            atts = {'ID':[exon.exon_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(exon.to_gff3(atts=atts))
                        for i,cds in enumerate(tr.lCDS):
                            #atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['{}'.format(tr.id)]}
                            atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(cds.to_gff3(atts=atts))
        f.close()


    def run(self):
        """"launch command"""

        conflict_list = []
        genes = Utils.extract_genes(self.input)


        self.get_aed(genes)
        tr_dict = {}
        references = set([g.seqid for g in genes])
        for ref in references:
            ref_genes = sorted([g for g in genes if g.seqid == ref], key=lambda x: x.start)
            for i,g in enumerate(ref_genes[:-1]):
                for tr in g.lTranscripts:
                    tr_dict[tr.id] = tr
                    #for g2 in ref_genes[i+1:-1]: # to validate
                    for g2 in ref_genes[i+1:]:
                      if g.is_feature_spanning(g2):
                        for tr2 in g2.lTranscripts:
#                            if tr.get_max_cds_end() > tr2.get_min_cds_start():
                            if tr.overlap_cds_with_other_transcript_cds(tr2):
                          #      print(tr.id, tr.get_max_cds_end(),tr2.id, tr2.get_min_cds_start())
                                conflict_list.append((tr.id, tr2.id))
            # add last tr in dict
            for tr in ref_genes[-1].lTranscripts:
                tr_dict[tr.id] = tr


        logging.info("{} potential conflicts to resolved".format(len(conflict_list)))

        list_to_remove = []
        for cf in conflict_list:
            #l = self._rank_tr_score([tr_dict[cf[0]],tr_dict[cf[1]]])
            l = self._rank_tr([tr_dict[cf[0]],tr_dict[cf[1]]])
            if l[0] not in list_to_remove:
                list_to_remove.append(l[1])

        self.export(genes, list_to_remove)



        return 0

