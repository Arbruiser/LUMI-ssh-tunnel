# LUMI-ssh-tunnel

*Step 1*: 
We will just tell the LUMI login node to forward your local port 8000 to port 8000 on the compute node's IP address.
```
ssh -N -L 8000:<NODELIST>:8000 <your username>@lumi.csc.fi
```
*Note*: Leave this running in your terminal. It will quietly sit there, forwarding requests from your laptop into LUMI.

*Step 2*: Bridge the Network to the Socket on the Compute Node
Right now, your vLLM server is only listening to a local file (/tmp/vllm-17139911.sock). We need a bridge to catch the TCP traffic coming from your laptop and pipe it into that socket file.

Jump into the compute node:
```
srun --overlap --jobid <slurm-job-id> --pty bash
```

Once you are at the shell inside your compute node, change the .sock file path (`SOCKET_PATH = "/tmp/vllm-*.sock"`) to your JOBID and run `bridge.py` from inside the container:
```
singularity run -B /pfs,/scratch,/projappl /appl/local/laifs/containers/lumi-multitorch-latest.sif python bridge.py
```
*Note*: Leave this running in your terminal. It will quietly sit there, translating network requests from your laptop into socket requests for vLLM.

*Step 3*: Run the Local Python Script
```
python ssh_chat_with_LLM.py "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
```

...or your own Python script where client is:
```
client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key="token-ignored",
)
```
