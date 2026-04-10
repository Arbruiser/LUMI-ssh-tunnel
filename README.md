## Connecting OpenCode to vLLM on LUMI via SSH Tunnel
This setup runs the OpenCode coding agent in a local Docker container and connects it to a Qwen3-Coder-Next instance running on a LUMI compute node.

This guide is written for Linux. Mac/Windows users will need to adjust the Docker gateway IP (usually host.docker.internal).
Scripts for starting a vLLM server were adapted from [ai-inference].

---

### **Step 1: Start vLLM on LUMI**
Connect to LUMI and start a vLLM server instance on a compute node. Change the `project` to your actual project number in `run-vllm-lumi4.sh` and run: 
1. Log into LUMI and clone this repository;
2. Edit `run-vllm-lumi4.sh` with your project number;
3. Submit the job:
```bash
sbatch run-vllm-lumi4.sh
```
4. Get your connection details:
- Run `squeue --me` to find your NODELIST (e.g., `nid005500`);
- Open your slurm output file (`slurm-XXXXXXXX.out`) and copy the API KEY;
- Wait a few minutes for the weights to load. Check the end of `slurm-XXXXXXXX.out` for a line similar to `(APIServer pid=8379) INFO: Application startup complete.`.

---

### **Step 2: make the SSH tunnel**
We will tell the LUMI login node to forward requests from Docker's IP address on local port 8042 to port 8042 on the compute node's IP address. It is a "double jump": Container -> Host -> LUMI Login -> LUMI Compute. 
Log out of LUMI, run this in your **local terminal** and leave it open:
```bash
# Replace <NODELIST> and <your username>
ssh -N -L 172.17.0.1:8042:<NODELIST>:8042 <your username>@lumi.csc.fi
```
*Note*: Leave this running in your terminal. It will quietly sit there, forwarding requests from your machine into LUMI's compute node.

**Command breakdown:**
- `-N` stands for 'No execute', so that we don't start a new shell on LUMI.
- `-L` - 'Local port forwarding', makes a "pipe" from your machine to LUMI. 
- `8042:` is the "entrance pipe" on your machine, if any program *on your machine* taks to port 8042, it's forwarded to LUMI.
- `172.17.0.1` is the IP address of Docker containers on your machine.
- `<NODELIST>` is the compute node where your vLLM instance is running.
- `:8042` is the exit of the pipe on the compute node. 

---

### **Step 3: configure and launch Docker**
Open a second terminal, clone this repository and edit `opencode.json` with your `apiKey` from Step 1.
Then, build and run the container:
```bash
sudo docker build -t opencode-agent .

sudo docker run -d \
  --name opencode-sandbox \
  -e OPENAI_BASE_URL="http://172.17.0.1:8042/v1" \
  -v "$(pwd):/app" \
  opencode-agent
```

- `-d`: Detached mode. Runs the container in the background so your terminal remains free to run commands.
- `--name opencode-sandbox`: Gives the container a human readable name so you can find it easily with `docker ps`.
- `-e OPENAI_BASE_URL=...`: Environment Variable. This tells OpenCode exactly where to find your vLLM server (which is being piped through the tunnel at 172.17.0.1:8042).
`-v "$(pwd):/app"`: Volume Mount. This "binds" your current folder on your laptop to the /app folder inside the container. Anything the AI agent writes in /app appears instantly on your machine.

---

### **Step 4: start the coding agent**
Open an interactive bash shell inside your running container:
```bash
sudo docker exec -it opencode-sandbox /bin/bash
```

And run OpenCode from inside the container:
```bash
opencode
```

---

### **Step 5**:
To stop the agent:
```bash
sudo docker stop opencode-sandbox && sudo docker rm opencode-sandbox
```
To stop the tunnel:
Go to the second terminal and press Ctrl+C

---
**Troubleshooting:**
If you're getting the error that the port is already occupied when spinning up vLLM, you can:
1) Try again, possibly get a different node where the port isn't occupied by another user;
2) Change the port in `run-vllm-process.sh`, in your SSH tunnel, and in `opencode.json`. 

If you're getting "error 429: too many requests...", add your HF access token to the `run-vll-lumi4.sh` script:
```bash
export HF_TOKEN="<your read HF token>"
```
**Changing the model**
To change the model, you need to: 
1) edit the `vllm serve` command at the end of `run-vllm-lumi4.sh`;
2) edit `opencode.json` with the right model name.

[ai-inference page]: https://github.com/CSCfi/ai-inference-examples
