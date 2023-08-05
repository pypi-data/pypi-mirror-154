from meteor_reasoner.materialization.seminaive_join import *
from meteor_reasoner.materialization.naive_join import *
from collections import defaultdict
import time


def naive_immediate_consequence_operator(rules, D, D_index, recorder=None):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        # print("Rule application:", str(rule))
        # t_start = time.time()
        naive_join(rule, D, delta_new, D_index, recorder=recorder)
        # print("Run time:", time.time()-t_start)
    return delta_new


def seminaive_immediate_consequence_operator(rules, D, D_index, k=1, delta_old=None):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        # print("Rule application:", str(rule))
        # t_start = time.time()
        seminaive_join(rule, D, delta_old, delta_new, D_index=D_index)
        # print("Run time:", time.time() - t_start)

    return delta_new
