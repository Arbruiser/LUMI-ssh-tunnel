# LUMI-ssh-tunnel
**Step 0**:
Start a vLLM server instance on a compute node. You can follow the instructions on the [ai-inference page]. 

**Step 1**:
We will tell the LUMI login node to forward your local port 8000 to port 8000 on the compute node's IP address.
```bash
ssh -N -L 8000:<NODELIST>:8000 <your username>@lumi.csc.fi
```
*Note*: Leave this running in your terminal. It will quietly sit there, forwarding requests from your laptop into LUMI's compute node.
`-N` stands for 'No execute', so that we don't open a new terminal.
`-L` - 'Local port forwarding', makes a "pipe" from your machine to LUMI. 
`8000:` is the "entrance pipe" on your machine, if any program *on your machine* taks to port 8000, it's forwarded to LUMI.
`:8000` is the exit of the pipe on the compute node. 


**Step 2**: 
The vLLM server is only listening to a local file (`/tmp/vllm-<JOBID>.sock`), so we need to build a bridge between port 8000 on the compute node and the socket file. 

Open a new terminal, connect to LUMI, jump into the compute node:
```bash
srun --overlap --jobid <slurm-job-id> --pty bash
```

Once you are at the shell inside your compute node, run `bridge.py` from inside the container (change `<JOBID>` to your actual JOBID):
```bash
singularity run -B /pfs,/scratch,/projappl /appl/local/laifs/containers/lumi-multitorch-latest.sif python bridge.py "<JOBID>"
```
*Note*: Leave this running in your terminal. It will quietly sit there, translating network requests from your laptop into socket requests for vLLM.

**Step 3**: 
Run the Local Python Script
```bash
python ssh_chat_with_LLM.py "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
```

...or your own Python script where client is:
```bash
client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key="token-ignored",
)
```


[ai-inference page]: https://github.com/CSCfi/ai-inference-examples
