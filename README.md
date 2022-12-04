# Security Observatory for Helm Charts

This project continuously analyzes the global security posture of Helm charts.

It's on its very early stages, expect some inaccuracies and fast evolution.

## Sources

It uses [Artifact Hub](https://artifacthub.io/) as a source for a list of available Helm charts. It doesn't stress that projects resources as a static list of charts is downloaded in a single query.

Other sources can be added when they are available in the future.

## Evaluation

For evaluation, it uses:

* [psa-checker](https://vicenteherrera.com/psa-checker): A cli tool for static analysis of Pod Security Standard on files. Create by the same author as this project.
* [badrobot](https://github.com/controlplaneio/badrobot): A cli tool to evaluation Kubernetes operators for essential security practices.

More tools and evaluations will be added very soon.

## Results

Visit this page to see the generated documentation for results on the evaluation of all charts:

* **[HELM CHARTS EVALUATION RESULTS](https://vicenteherrera.com/secobs-charts/docs/generated/charts_levels.md)**

A WIP Jupyter Notebook will provide results that you can interact with in the near future, check its state here:

* **[Helm charts Jupyter Notebook](https://github.com/vicenteherrera/secobs-charts/blob/main/jupyter/helm_charts.ipynb)**
