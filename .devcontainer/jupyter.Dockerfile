FROM python:3.6

RUN set -x; \
    # pin specific versions of Jupyter and Tornado dependency
    pip install notebook==5.7.10 \
    pip install tornado==4.5.3 \
    # install the package
    pip install graph-notebook \
    # install and enable the visualization widget
    && jupyter nbextension install --py --sys-prefix graph_notebook.widgets \
    && jupyter nbextension enable  --py --sys-prefix graph_notebook.widgets \
    # copy static html resources
    && python -m graph_notebook.static_resources.install \
    && python -m graph_notebook.nbextensions.install \
    # copy premade starter notebooks
    && mkdir -p /notebooks \
    && python -m graph_notebook.notebooks.install --destination /notebooks

EXPOSE 8888

CMD jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root /notebooks


