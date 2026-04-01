# LUMI-ssh-tunnel
**Step 1**:
Start a vLLM server instance on a compute node by running: 
```bash
sbatch run-vllm-lumi4.sh
```
The vLLM is started with a randomly generated API key which you can view at the beginning of the slurm output file.

**Step 2**:
We will tell the LUMI login node to forward your local port 8000 to port 8000 on the compute node's IP address.
```bash
ssh -N -L 8000:<NODELIST>:8000 <your username>@lumi.csc.fi
```
*Note*: Leave this running in your terminal. It will quietly sit there, forwarding requests from your laptop into LUMI's compute node.
`-N` stands for 'No execute', so that we don't open a new terminal.
`-L` - 'Local port forwarding', makes a "pipe" from your machine to LUMI. 
`8000:` is the "entrance pipe" on your machine, if any program *on your machine* taks to port 8000, it's forwarded to LUMI.
`:8000` is the exit of the pipe on the compute node. 

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
