## Connecting OpenCode coding agent from a Docker container on your machine to a vLLM instance on a LUMI compute node booked by you
This demo is meant for running on Linux. Running on Mac or Windows requires small changes with Docker's IP address. 

###**Step 0**:
Clone this repository to your machine and to your project folder on LUMI.

###**Step 1**:
Connect to LUMI and start a vLLM server instance on a compute node. Change the `project` to your actual project number in `run-vllm-lumi4.sh` and run: 
```bash
sbatch run-vllm-lumi4.sh
```
1. Run `squeue --me` to find your NODELIST (e.g., `nid005500`).
2. Open your slurm output file (`slurm-XXXXXXXX.out`) and copy the API KEY.
3. Wait a few minutes for the weights to load. Check the end of `slurm-XXXXXXXX.out` for a line similar to `(APIServer pid=8379) INFO: Application startup complete.`.

**Step 2**:
Configure OpenCode Locally:
1. Open `opencode.json` on your machine.
2. Paste your API KEY into the `apiKey` field.

**Step 3**
We will tell the LUMI login node to forward requests from Docker's IP address on local port 8000 to port 8000 on the compute node's IP address. It is a "double jump": Container -> Host -> LUMI Login -> LUMI Compute. Run:
```bash
# Replace <NODELIST> and <your username>
ssh -N -L 172.17.0.1:8000:<NODELIST>:8000 <your username>@lumi.csc.fi
```
*Note*: Leave this running in your terminal. It will quietly sit there, forwarding requests from your laptop into LUMI's compute node.
- `-N` stands for 'No execute', so that we don't start a new shell on LUMI.
- `-L` - 'Local port forwarding', makes a "pipe" from your machine to LUMI. 
- `8000:` is the "entrance pipe" on your machine, if any program *on your machine* taks to port 8000, it's forwarded to LUMI.
- `172.17.0.1` is the IP address of Docker containers on your machine.
- `<NODELIST>` is the compute node where your vLLM instance is running.
- `:8000` is the exit of the pipe on the compute node. 

**Step 4**: 
Building and launch the container. **Open an new terminal** and navigate to this project's directory and run:
```bash
sudo docker build -t opencode-agent .

sudo docker run -d \
  --name opencode-sandbox \
  -e OPENAI_BASE_URL="http://172.17.0.1:8000/v1" \
  -v "$(pwd):/app" \
  opencode-agent
```

- `-d`: Detached mode. Runs the container in the background so your terminal remains free to run commands.
- `--name opencode-sandbox`: Gives the container a human readable name so you can find it easily with `docker ps`.
- `-e OPENAI_BASE_URL=...`: Environment Variable. This tells OpenCode exactly where to find your vLLM server (which is being piped through the tunnel at 172.17.0.1:8000).

`-v "$(pwd):/app"`: Volume Mount. This "binds" your current folder on your laptop to the /app folder inside the container. Anything the AI agent writes in /app appears instantly on your machine.

**Step 5**:
Open an interactive bash shell inside your running container:
```bash
sudo docker exec -it opencode-sandbox /bin/bash
```

From inside container, run opencode:
```bash
opencode
```

**Step 6**:
To stop the agent:
```bash
sudo docker stop opencode-sandbox && sudo docker rm opencode-sandbox
```
To stop the tunnel:
Go to the second terminal and press Ctrl+C

[ai-inference page]: https://github.com/CSCfi/ai-inference-examples
