# Analytic Model of Fidelity under Depolarizing Noise


This repository contains all the source code, data, and circuits used in our study on fidelity estimation for quantum circuits under depolarizing noise and coherence errors. The repository accompanies the research paper published at: [An Accurate Efficient Analytic Model of Fidelity under Depolarizing Noise oriented to Large Scale Quantum System Design](https://arxiv.org/abs/2503.06693).

## Repository Structure

- **`circuits/`**: Quantum circuits used in the main experiments.
- **`shor_bench/`**: Circuits specifically used for the Shor's algorithm experiment.
- **`estimation_algorithms/`**: Source code for the fidelity estimation methods, including:
  - Qiskit Simulation (with noise models derived from IBM Q processors) [[1]](https://arxiv.org/abs/2405.08810)
  - ESP (Estimated Success Probability) [[2]](https://dl.acm.org/doi/10.1145/3297858.3304007)
  - QVA (Quantum Vulnerability Analysis) [[3]](https://ieeexplore.ieee.org/document/10361567)
  - Our proposed approach
- **`data/data_*.csv`**: Experimental data from six separate executions on IBM Q processors:
  - `data_1.csv, data_2.csv, ..., data_6.csv` contain real hardware execution results.
  - `data_1.csv` was used to generate the figures in the paper.
  - `data_depol_simulation.csv` contains results from depolarizing noise simulations.
- **`figures/figure_*.py`**: Source code to generate all figures presented in the paper, ensuring full reproducibility of results.

## How to Replicate the Experiments

To reproduce the main experiment:
1. Run `generate_data_1.py` to submit the circuit execution to the designated IBM Q quantum processor.
2. Once execution completes, retrieve the experiment identifier (printed from step 1).
3. Use the retrieved identifier to run `generate_data_2.py` and collect the results.

To replicate additional experiments:
- **Technology feasibility studies (Figures 5 and 6 in the paper):**
  - Use `generate_link_feasibility_data.py` to evaluate computation bounds with different error rates.
  - Use `generate_shor_computation_data.py` to analyze the feasibility of Shor's algorithm for different quantum architectures.

All scripts allow users to modify simulation parameters as needed.

## Citation
If you use this repository in your work, please cite our paper:
> [An Accurate Efficient Analytic Model of Fidelity under Depolarizing Noise oriented to Large Scale Quantum System Design](https://arxiv.org/abs/2503.06693)

We hope this repository facilitates further research in quantum circuit fidelity estimation. If you have any questions or find issues, feel free to reach out! [pau.escofet@upc.edu](mailto:pau.escofet@upc.edu)

