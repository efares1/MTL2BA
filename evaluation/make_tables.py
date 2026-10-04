"""Combine ours_results.tsv, spot_det.tsv, casaal_exclusive.tsv, and
casaal_results.tsv into results.tsv and the LaTeX tables:
  results_table.tex   sizes, median time, CASAAL on the common domain
  scaling_table.tex   R and N families: stage times, peak memory, Spot options
  formulas_table.tex  exact formulas (supplementary material)
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEGENERATE = {'F2', 'F3b'}      # unsatisfiable antecedent with one event per position


def read(fn):
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f, delimiter='\t')}


forms = []
for line in open(os.path.join(HERE, 'formulas.tsv'), encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    fid, desc, ours, cas = line.rstrip('\n').split('\t')
    forms.append((fid, desc, ours, cas))

import re


def pairs(path, pat):
    """Number of distinct (source, target) pairs of transitions."""
    if not os.path.exists(path):
        return ''
    return str(len({m for m in re.findall(pat, open(path, encoding='utf-8').read())}))


ours = read('ours_results.tsv')
small = read('spot_det.tsv')
sym = read('sym_sizes.tsv')
casx = read('casaal_exclusive.tsv')
cas0 = read('casaal_results.tsv')


def ok(r):
    return r.get('status') == 'ok'


cols = ['id', 'description', 'status', 'clocks_f', 'spot_st', 'spot_tr', 'comp_st', 'comp_tr',
        'opt_rounds', 'opt_st', 'opt_tr', 'opt_clk', 'exp_st', 'exp_tr', 'exp_clk', 'exp_inv',
        'exp_diff', 'init_free', 'spot_s', 'opt_s', 'exp_s', 'total_s', 'total_s_min',
        'total_s_max', 'mem_mb', 'det_spot_st', 'det_spot_tr', 'det_exp_st',
        'det_exp_tr', 'det_total_s', 'casaal_x_st', 'casaal_x_tr', 'casaal_x_clk',
        'casaal_x_s', 'casaal_st', 'casaal_tr', 'casaal_clk', 'casaal_exact',
        'exp_pairs', 'casaal_x_pairs', 'sym_tr']
rows = []
for fid, desc, _, _ in forms:
    o, sm, cx, c0 = ours.get(fid, {}), small.get(fid, {}), casx.get(fid, {}), cas0.get(fid, {})
    g = lambda d, k: d.get(k, '') if ok(d) or d is cx or d is c0 else ''
    rows.append([fid, desc, o.get('status', 'missing'), g(o, 'formula_clocks'),
                 g(o, 'spot_states'), g(o, 'spot_trans'), g(o, 'comp_locs'), g(o, 'comp_trans'),
                 g(o, 'opt_rounds'), g(o, 'opt_locs'), g(o, 'opt_trans'), g(o, 'opt_clocks'),
                 g(o, 'exp_locs'), g(o, 'exp_trans'), g(o, 'exp_clocks'), g(o, 'exp_invs'),
                 g(o, 'exp_diffs'), g(o, 'init_free'), g(o, 'spot_s_med'), g(o, 'opt_s_med'),
                 g(o, 'exp_s_med'), g(o, 'total_s_med'), g(o, 'total_s_min'),
                 g(o, 'total_s_max'), g(o, 'mem_mb'),
                 g(sm, 'spot_states'), g(sm, 'spot_trans'), g(sm, 'exp_locs'),
                 g(sm, 'exp_trans'), g(sm, 'total_s'),
                 cx.get('states', ''), cx.get('transitions', ''), cx.get('clocks', ''),
                 cx.get('time_s', ''), c0.get('states', ''), c0.get('transitions', ''),
                 c0.get('clocks', ''), c0.get('exact', ''),
                 pairs(os.path.join(HERE, 'out', fid + '.dot'),
                       r'\n\s*(L\d+) -> (L\d+) \[') if ok(o) else '',
                 pairs(os.path.join(HERE, 'casaal_out_x', fid + '.gv'),
                       r'\n\s*([1-9]\d*) -> (\d+)'),
                 sym.get(fid, {}).get('sym_trans', '') if ok(sym.get(fid, {})) else ''])
with open(os.path.join(HERE, 'results.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(cols)
    w.writerows(rows)
R = {r[0]: dict(zip(cols, r)) for r in rows}


def esc(s):
    return s.replace('&', r'\&').replace('_', r'\_')


def casaal_cell(d):
    if d['casaal_x_st'] in ('', '-', 'error'):
        return '--'
    mark = ''
    if d['casaal_exact'] == 'no':
        mark = r'$^\dagger$'
    return f"{d['casaal_x_st']}/{d['casaal_x_tr']}/{d['casaal_x_clk']}{mark}"


# ------------------------------------------------------------ main table
L = [r'\begin{table*}[t]', r'\centering',
     r'\caption{Evaluation of \texttt{mtl2tba} and comparison with CASAAL on the '
     r'common semantic domain (one event per position).  $|X|$: distinct primitive '
     r'(hatted) timed subformulas after unfolding of the ordinary operators.  Spot: '
     r'B\"uchi automaton returned by Spot (states/transitions, one transition per '
     r'cube).  Opt.: after reset completion and the verified optimizations '
     r'(locations/transitions/clocks).  Export: automaton for UPPAAL (locations, '
     r'transitions, clocks, locations with an invariant, and occurrences of difference '
     r'constraints in the guards).  Sym.: transitions of the symbolic automaton, with '
     r'Boolean labels.  Time: median of five runs of the whole chain, in '
     r'seconds.  CASAAL: states/transitions/clocks of the automaton of CASAAL for the '
     r'formula conjoined with the mutual exclusion of its propositions; transitions '
     r'carry Boolean formulas.  $\dagger$: not equivalent (CASAAL has no hatted '
     r'operator); $\ddagger$: degenerate formula, equivalent to $\Box\neg p$ or '
     r'$\Box\neg e$ with one event per position.  Formulas: Table~S1 of the '
     r'supplementary material.}',
     r'\label{tab:evaluation}', r'\small',
     r'\begin{tabular}{@{}lrrrrrrrrrrrrrr@{}}', r'\toprule',
     r' & & \multicolumn{2}{c}{Spot} & \multicolumn{3}{c}{Opt.} & '
     r'\multicolumn{5}{c}{Export} & & & CASAAL\\',
     r'\cmidrule(lr){3-4}\cmidrule(lr){5-7}\cmidrule(lr){8-12}',
     r'Id & $|X|$ & st & tr & loc & tr & clk & loc & tr & clk & inv & diff & Sym. '
     r'& Time & st/tr/clk\\', r'\midrule']
for fid, desc, _, _ in forms:
    d = R[fid]
    name = fid + (r'$^\ddagger$' if fid in DEGENERATE else '')
    if d['status'] != 'ok':
        L.append(f"{name} & \\multicolumn{{13}}{{c}}{{{d['status']} (limit 300~s)}} & "
                 f"{casaal_cell(d)}\\\\")
        continue
    L.append(f"{name} & {d['clocks_f']} & {d['spot_st']} & {d['spot_tr']} & {d['opt_st']} & "
             f"{d['opt_tr']} & {d['opt_clk']} & {d['exp_st']} & {d['exp_tr']} & "
             f"{d['exp_clk']} & {d['exp_inv']} & {d['exp_diff']} & {d['sym_tr']} & "
             f"{float(d['total_s']):.2f} & {casaal_cell(d)}\\\\")
L += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
open(os.path.join(HERE, 'results_table.tex'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ------------------------------------------------------------ scaling table
S = [r'\begin{table}[t]', r'\centering',
     r'\caption{Scalability on the families R$n$ and N$n$: median time of the Spot, '
     r'optimization, and export stages and of the whole chain, minimum and maximum of '
     r'the five runs, peak memory, and exported transitions with Spot options '
     r'\texttt{-B --small} (default) and \texttt{-B -D}.  Times in seconds, memory in MB.}',
     r'\label{tab:scaling}', r'\footnotesize', r'\setlength{\tabcolsep}{3pt}',
     r'\begin{tabular}{@{}lrrrrrrrr@{}}', r'\toprule',
     r'Id & Spot & Opt. & Exp. & Total & [min, max] & Mem. & tr & tr \texttt{-D}\\',
     r'\midrule']
for fid, desc, _, _ in forms:
    if fid[0] not in 'RN':
        continue
    d = R[fid]
    if d['status'] != 'ok':
        S.append(f"{fid} & \\multicolumn{{8}}{{c}}{{{d['status']} (limit 300~s)}}\\\\")
        continue
    sm = d['det_exp_tr'] or 'timeout'
    S.append(f"{fid} & {float(d['spot_s']):.2f} & {float(d['opt_s']):.2f} & "
             f"{float(d['exp_s']):.2f} & {float(d['total_s']):.2f} & "
             f"[{float(d['total_s_min']):.2f}, {float(d['total_s_max']):.2f}] & "
             f"{float(d['mem_mb']):.0f} & {d['exp_tr']} & {sm}\\\\")
S += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
open(os.path.join(HERE, 'scaling_table.tex'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')

# ------------------------------------------------------------ formulas table
Fm = [r'\begin{table*}[t]', r'\centering',
      r'\caption{Benchmark formulas, in the input syntax of \texttt{mtl2tba} '
      r'(\texttt{\^{}U}, \texttt{\^{}R}: hatted operators; \texttt{[]}, \texttt{<>}: '
      r'$\Box$, $\Diamond$; \texttt{!}: negation).  CASAAL receives the same formula, '
      r'with \texttt{/\textbackslash} and \texttt{\textbackslash/} for $\wedge$ and $\vee$, '
      r'conjoined with \texttt{[](!(a /\textbackslash{} b))} for every pair of distinct '
      r'propositions; for F3 and F13 it receives the closest encodings with a leading '
      r'$\bigcirc$, which are not equivalent.  R1 is F1 with renamed propositions; it is '
      r'the first instance of the family R$n$.}',
      r'\label{tab:formulas}', r'\small',
      r'\begin{tabular}{@{}llp{0.62\textwidth}@{}}', r'\toprule',
      r'Id & Property & Formula\\', r'\midrule']
for fid, desc, f, _ in forms:
    ff = esc(f).replace('^', r'\^{}').replace('<', r'\textless{}').replace('>', r'\textgreater{}')
    ff = ff.replace('|', r'\textbar{}')
    Fm.append(f'{fid} & {esc(desc)} & \\texttt{{{ff}}}\\\\')
Fm += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
open(os.path.join(HERE, 'formulas_table.tex'), 'w', encoding='utf-8').write('\n'.join(Fm) + '\n')
# ------------------------------------------------------------ primed configurations
weak = read('weak_results.tsv')
Wt = [r'\begin{table}[t]', r'\centering',
      r'\caption{Primed configurations: the Until of the clauses of upper-bounded '
      r'hatted Until is replaced by a weak until in the formula given to Spot, which '
      r'removes the degeneralization of the B\"uchi acceptance (configurations whose '
      r'formula changes and whose sizes differ).  Spot: states/transitions; Opt.: '
      r'locations/transitions; Sym.: symbolic transitions of the unprimed and primed '
      r'configurations; Time: median of five runs, in seconds; CASAAL: '
      r'states/transitions on the common domain.}',
      r'\label{tab:weak}', r'\footnotesize', r'\setlength{\tabcolsep}{3pt}',
      r'\begin{tabular}{@{}lrrrrrrrr@{}}', r'\toprule',
      r' & \multicolumn{2}{c}{Spot} & \multicolumn{2}{c}{Opt.} & \multicolumn{2}{c}{Sym.} & & \\',
      r'\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}',
      r'Id & st & tr & loc & tr & $\mathsf{U}$ & $\mathsf{W}$ & Time & CASAAL\\', r'\midrule']
for fid, desc, _, _ in forms:
    wd = weak.get(fid + "'")
    if not wd:
        continue
    d = R[fid]
    if wd.get('status') == 'ok' and d['status'] == 'ok' and wd['opt_locs'] == d['opt_st'] \
            and wd['opt_trans'] == d['opt_tr']:
        continue
    cx = casaal_cell(d).rsplit('/', 1)[0] if casaal_cell(d) != '--' else '--'
    cx = cx.replace(r'$^\dagger$', '')
    mark = r'$^\dagger$' if d['casaal_exact'] == 'no' else ''
    if wd.get('status') != 'ok':
        Wt.append(f"{fid}$'$ & \\multicolumn{{7}}{{c}}{{timeout (limit 300~s)}} & {cx}{mark}\\\\")
        continue
    su = d['sym_tr'] if d['status'] == 'ok' else 'timeout'
    Wt.append(f"{fid}$'$ & {wd['spot_states']} & {wd['spot_trans']} & {wd['opt_locs']} & "
              f"{wd['opt_trans']} & {su} & {wd['sym_trans']} & "
              f"{float(wd['total_s_med']):.2f} & {cx}{mark}\\\\")
Wt += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
open(os.path.join(HERE, 'weak_table.tex'), 'w', encoding='utf-8').write('\n'.join(Wt) + '\n')
print('tables written')
