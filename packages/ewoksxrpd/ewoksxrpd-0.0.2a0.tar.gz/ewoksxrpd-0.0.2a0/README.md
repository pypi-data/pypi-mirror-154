# ewoksxrpd

Data processing workflows for High-Throughout X-ray Powder Diffraction

## Getting started

Run an example workflow

```bash
python examples/job.py
```

Run an example workflow with GUI

```bash
ewoks execute examples/xrpd_workflow.json --binding=orange --data-root-uri=/tmp --data-scheme nexus
```

Produce the example data

```bash
pytest --examples
```

## Documentation

https://workflow.gitlab-pages.esrf.fr/ewoksapps/ewoksxrpd/