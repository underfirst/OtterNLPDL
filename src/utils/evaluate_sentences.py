from easse.bleu import corpus_bleu
from easse.fkgl import corpus_fkgl
from easse.sari import corpus_sari


def evaluate_sentences(comps, simps, simp_preds, calc_simp_pred_bleu=False, calc_comp_simp_bleu=False):

    comps = [sent.lower() for sent in comps]
    if type(simps[0]) == type([]):
        simps = [[sent.lower() for sent in l] for l in simps]
    else:
        simps = [sent for sent in simps]
    simp_preds = [sent.lower() for sent in simp_preds]
    if type(simps[0]) == type([]):
        refs = simps
    else:
        refs = [simps]

    bleu = corpus_bleu(simp_preds, refs, tokenizer='none')
    sari = corpus_sari(comps, simp_preds, refs, tokenizer="none", use_paper_version=False, use_f1_for_deletion=True)
    fkgl = corpus_fkgl(simp_preds, tokenizer='none')
    result = (bleu, sari, fkgl)
    if calc_simp_pred_bleu:
        result = result + (corpus_bleu(simp_preds, [comps]),)
    if calc_comp_simp_bleu:
        result = result + (corpus_bleu(comps, refs),)
    return result
