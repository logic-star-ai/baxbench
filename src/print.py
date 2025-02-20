import math
from collections import defaultdict
from typing import Any, DefaultDict, cast

from tabulate import tabulate
from termcolor import colored

from tasks import TasksAndSampleResults


def color_cyan(text: str) -> str:
    return colored(text, "cyan")


def color_blue(text: str, cond: bool) -> str:
    return colored(text, "blue") if cond else text


def color_sec(text: str, num: float) -> str:
    if num == 0:
        return colored(text, "green")
    elif num < 0.5:
        return colored(text, "yellow")
    else:
        return colored(text, "red")


def color_func(text: str, num: float) -> str:
    if num > 0.75:
        return colored(text, "green")
    elif num < 0.75 and num > 0.25:
        return colored(text, "yellow")
    else:
        return colored(text, "red")


def tasks_and_results_to_table(
    tasks_and_results: TasksAndSampleResults, verbose: bool = False
) -> str:
    env_ids: dict[tuple[str, str, str], int] = {}
    model_and_scenario_ids: dict[str, int] = {}
    cells: dict[tuple[int, int], str] = {}
    for task, result in tasks_and_results:
        col_id = env_ids.setdefault(
            (task.env.id, task.spec_type, task.safety_prompt), len(env_ids)
        )
        model_and_scenario_info = f"{task.model}\n{task.scenario.id}"
        row_id = model_and_scenario_ids.setdefault(
            model_and_scenario_info, len(model_and_scenario_ids)
        )
        if verbose:
            scenario_metadata = [
                f"Endpts: {task.scenario.num_endpoints}",
                f"Potential CWEs:",
            ]
            sorted_potential_cwes = sorted(
                list(task.scenario.potential_cwes),
                key=lambda cwe: cast(int, cwe.value["num"]),
            )
            for cwe in sorted_potential_cwes:
                scenario_metadata.append(f"  CWE-{cwe.value['num']}")
            scenario_metadata_str = "\n".join(
                [color_cyan(s) for s in scenario_metadata]
            )
            cells[(row_id, 0)] = model_and_scenario_info + "\n" + scenario_metadata_str
        else:
            cells[(row_id, 0)] = model_and_scenario_info

        ft = [
            color_func(f"pass@{k}: {result.pass_at_k[k]:.2f}", result.pass_at_k[k])
            for k in sorted(result.pass_at_k.keys())
        ]
        ft_secure = [
            color_func(
                f"sec_pass@{k}: {result.secure_pass_at_k[k]:.2f}",
                result.secure_pass_at_k[k],
            )
            for k in sorted(result.secure_pass_at_k.keys())
        ]
        ft_insecure = [
            color_sec(f"insec: {100*result.insec_pass:.1f}%", result.insec_pass),
        ]
        cwes = [
            color_sec(f"cwe-{cwe}: {100*p:.1f}", p)
            for cwe, p in result.cwe_percentages.items()
        ]
        cwes_ft_correct = [
            color_sec(f"okft-cwe-{cwe}: {100*p:.1f}", p)
            for cwe, p in result.cwe_ft_correct_percentages.items()
        ]
        errs = [
            color_blue(
                f"exceptions: {len(result.test_exceptions)}/{result.n_samples}",
                len(result.ft_exceptions) > 0,
            ),
        ]
        cell = "\n".join(ft + ft_secure + ft_insecure + cwes + cwes_ft_correct + errs)
        cells[(row_id, col_id + 1)] = cell

    headers: list[str] = [""] + [
        f'{envid.replace("-", "\n")} {spec_type,safety_prompt}'
        for (envid, spec_type, safety_prompt), _ in sorted(
            env_ids.items(), key=lambda kv: kv[1]
        )
    ]
    table: list[list[str]] = [
        ["" for _ in range(len(env_ids) + 1)]
        for _ in range(len(model_and_scenario_ids))
    ]
    for (row_id, col_id), content in cells.items():
        table[row_id][col_id] = content
    return tabulate(table, headers, tablefmt="simple_grid")


def tasks_and_results_to_table_averages(
    tasks_and_results: TasksAndSampleResults,
) -> str:
    # Track frameworks (env/spec/safety_prompt) in a consistent order
    env_ids: dict[tuple[str, str, str], int] = {}

    aggregator: DefaultDict[str, DefaultDict[tuple[str, str, str], dict[str, Any]]] = (
        defaultdict(
            lambda: defaultdict(
                lambda: {
                    "pass_at_k": defaultdict(lambda: [0.0, 0]),
                    "sec_pass_at_k": defaultdict(lambda: [0.0, 0]),
                    "insec": [0.0, 0],
                }
            )
        )
    )

    # Collect all pass@k keys and secure_pass@k keys encountered (so we can display consistently)
    all_pass_ks = set()
    all_sec_pass_ks = set()

    # Build the aggregator and remember which frameworks (env+spec+safety) we have
    for task, result in tasks_and_results:
        env_key = (task.env.id, task.spec_type, task.safety_prompt)
        if env_key not in env_ids:
            env_ids[env_key] = len(env_ids)

        model = task.model
        # pass@k
        for k, val in result.pass_at_k.items():
            if val is not None and not math.isnan(val):
                aggregator[model][env_key]["pass_at_k"][k][0] += val
                aggregator[model][env_key]["pass_at_k"][k][1] += 1
            all_pass_ks.add(k)

        # secure_pass@k
        for k, val in result.secure_pass_at_k.items():
            if val is not None and not math.isnan(val):
                aggregator[model][env_key]["sec_pass_at_k"][k][0] += val
                aggregator[model][env_key]["sec_pass_at_k"][k][1] += 1
            all_sec_pass_ks.add(k)

        # insec
        if result.insec_pass is not None and not math.isnan(result.insec_pass):
            aggregator[model][env_key]["insec"][0] += result.insec_pass
            aggregator[model][env_key]["insec"][1] += 1

    # Prepare the headers: first column is blank (for model),
    # then one column per framework in the discovered order,
    # plus a final column "AVG" that averages across all frameworks
    sorted_env_keys = sorted(
        env_ids.items(), key=lambda kv: kv[1]
    )  # [(env_key, idx), ...]
    headers = (
        [""]
        + [f'{ek[0].replace("-", "\n")} {ek[1]},{ek[2]}' for ek, _ in sorted_env_keys]
        + ["AVG"]
    )

    # We'll construct one row per model. Each cell will show the
    # average pass@k, sec_pass@k, insec for that (model, env_key).
    # The final column will be the average over all frameworks for that model.
    table_rows = []

    for model in sorted(aggregator.keys()):
        row = [model]

        # To also compute the model-wide average (across frameworks)
        sum_pass_at_k: DefaultDict[int, list[float]] = defaultdict(lambda: [0.0, 0])
        sum_sec_pass_at_k: DefaultDict[int, list[float]] = defaultdict(lambda: [0.0, 0])
        sum_insec = [0.0, 0]

        # Build a cell for each framework
        for env_key, _ in sorted_env_keys:
            agg_env = aggregator[model][env_key]

            # Compute the averaged values for pass@k
            env_pass_lines = []
            for k in sorted(all_pass_ks):
                s, c = agg_env["pass_at_k"][k]
                if c > 0:
                    avg_val = s / c
                    env_pass_lines.append(
                        color_func(f"pass@{k}: {avg_val:.2f}", avg_val)
                    )
                    # Accumulate for final column
                    sum_pass_at_k[k][0] += avg_val
                    sum_pass_at_k[k][1] += 1
                else:
                    # no data for that pass@k
                    pass

            # Compute the averaged values for sec_pass@k
            env_sec_lines = []
            for k in sorted(all_sec_pass_ks):
                s, c = agg_env["sec_pass_at_k"][k]
                if c > 0:
                    avg_val = s / c
                    env_sec_lines.append(
                        color_func(f"sec_pass@{k}: {avg_val:.2f}", avg_val)
                    )
                    # Accumulate for final column
                    sum_sec_pass_at_k[k][0] += avg_val
                    sum_sec_pass_at_k[k][1] += 1

            # Compute the averaged value for insec
            insec_sum, insec_count = agg_env["insec"]
            env_insec_line = ""
            if insec_count > 0:
                avg_insec = insec_sum / insec_count
                env_insec_line = color_sec(f"insec: {100*avg_insec:.1f}%", avg_insec)
                sum_insec[0] += avg_insec
                sum_insec[1] += 1

            cell_contents = env_pass_lines + env_sec_lines
            if env_insec_line:
                cell_contents.append(env_insec_line)

            # Join them with newlines for a multi-line cell
            row.append("\n".join(cell_contents) if cell_contents else "")

        # Now build the model-wide average cell (across frameworks)
        avg_cell_lines = []

        # pass@k
        for k in sorted(all_pass_ks):
            s, c = sum_pass_at_k[k]
            if c > 0:
                val = s / c
                avg_cell_lines.append(color_func(f"pass@{k}: {val:.2f}", val))

        # secure_pass@k
        for k in sorted(all_sec_pass_ks):
            s, c = sum_sec_pass_at_k[k]
            if c > 0:
                val = s / c
                avg_cell_lines.append(color_func(f"sec_pass@{k}: {val:.2f}", val))

        # insec
        insec_s, insec_c = sum_insec
        if insec_c > 0:
            val_insec = insec_s / insec_c
            avg_cell_lines.append(color_sec(f"insec: {100*val_insec:.1f}%", val_insec))

        row.append("\n".join(avg_cell_lines) if avg_cell_lines else "")
        table_rows.append(row)

    return tabulate(table_rows, headers, tablefmt="simple_grid")
