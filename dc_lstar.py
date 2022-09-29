from magento_sul import DCSUL
from dc_observation_table import DCObservationTable
from dc_oracle import DCOracle
from utils import find_minimal_consistent_dfa
from aalpy.utils.HelperFunctions import extend_set, all_prefixes

def run_dc_lstar(alphabet: list, sul: DCSUL, oracle: DCOracle):

    observation_table = DCObservationTable(alphabet, sul)

    # Initial update of observation table, for empty row
    observation_table.update_obs_table()

    while True:

        # Close observation table
        rows_to_close = observation_table.get_rows_to_close('longest_first')  # consider different closing strategy
        while rows_to_close is not None:
            rows_to_query = []
            for row in rows_to_close:
                observation_table.S.append(row)
                rows_to_query.extend([row + (a,) for a in alphabet])
            observation_table.update_obs_table(s_set=rows_to_query)
            rows_to_close = observation_table.get_rows_to_close('longest_first')  # consider different closing strategy

        # check completeness
        c_hypothesis = observation_table.gen_hypothesis(check_for_duplicate_rows=False)  # TODO: maybe change to True
        # c_hypothesis.make_input_complete('self_loop')  # TODO: do we need complete machine?

        cex = oracle.check_completeness(c_hypothesis)

        if cex is None:
            hypothesis = find_minimal_consistent_dfa(observation_table)
            cex = sul.check_soundness(hypothesis, alphabet)
            if cex is None:
                return hypothesis
            else:
                s_to_update = []
                added_rows = extend_set(observation_table.S, all_prefixes(cex))
                s_to_update.extend(added_rows)
                for p in added_rows:
                    s_to_update.extend([p + (a,) for a in alphabet])
                observation_table.update_obs_table(s_set=s_to_update)
                continue
        else:
            s_to_update = []
            added_rows = extend_set(observation_table.S, all_prefixes(cex))
            s_to_update.extend(added_rows)
            for p in added_rows:
                s_to_update.extend([p + (a,) for a in alphabet])
            observation_table.update_obs_table(s_set=s_to_update)
            continue

