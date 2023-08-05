# Run Jupyter Server in an LSF host

### Installation

```bash
pip install @papaemmelab/jupyterlab-lsf
```

### Usage:

Choose an unique port for your user:
```bash
jupyterlab-lsf --port 2345
```

### More:

```bash
$ jupyterlab-lsf --help

Usage: jupyterlab-lsf [OPTIONS]

  Submits jupyter server in an lsf host and map its port.

Options:
  -p, --port INTEGER      Port number, unique by server user  [default: 8888]
  -w, --walltime INTEGER  LSF job wall time (minutes)  [default: 240]
  -n, --nodes INTEGER     LSF job nodes  [default: 2]
  -m, --memory INTEGER    LSF job per node memory (Gb)  [default: 32]
  --watch INTEGER         Waiting seconds to watch for notebook job status
                          [default: 4]
  -s, --htslib-path TEXT  htslib path  [default: /work/isabl/ref/homo_sapiens/
                          GRCh37d5/htslib/htslib-1.9]
  --help                  Show this message and exit.
```

To map you localhost port with your server (where LSF runs):
```bash
ssh -X -N -f -L localhost:$PORT:localhost:$PORT $SERVER
```

To clear the port:
```bash
lsof -ti:$PORT | xargs kill -9
```

It might be useful to declare them as bash functions in your `.bash_profile`:
```bash
clearport () {
 lsof -ti:$1 | xargs kill -9
}

forward () {
 ssh -X -N -f -L localhost:"$1":localhost:"$1" "$2"
}

# Examples:
# forward 8888 juno
# clearport 8888

```

