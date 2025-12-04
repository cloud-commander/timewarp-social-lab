#!/bin/bash
# This script is intended to be run inside the container, but we can also run it from outside if we have privileges.
# However, the Dockerfile already includes this in /start.sh.
# This file is just for reference or manual execution if needed.

echo "Applying GPRS Traffic Control..."
tc qdisc add dev eth0 root tbf rate 40kbit burst 10kb latency 800ms
echo "Done. Bandwidth: 40kbps, Latency: 800ms."
