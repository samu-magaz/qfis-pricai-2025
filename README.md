# Implementing Quantum Fuzzy Inference Systems for the Detection of Apneic Events - Code

Repository for the paper "Implementing Quantum Fuzzy Inference Systems for the Detection of Apneic Events" presented in PRICAI 2025 - Workshop on Quantum Computing for Search and Optimization Problems

In this repository, you will find the implementation of the experiments presented in Section 3 of the paper.

## Classical FIS

To test the classical implementation, MATLAB's Fuzzy Logic Designer is required. Once the software is ready, simply import the file ```fis-sao2.fis``` and test as desired.

## Quantum FIS

To test the quantum implementation, a Jupyter notebook ```qifs-sao2.ipynb``` illustrating the use of the software is provided. To run the circuit via CLI, simply type the following command:

```python src/qfis.py -rqc [CRISP_INPUT_SAO2RED] [CRISP_INPUT_SAO2REDDUR]```

For example:

```python src/qfis.py -rqc 42 64```
