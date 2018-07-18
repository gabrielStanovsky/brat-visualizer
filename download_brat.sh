#!/bin/bash
# Download and extract brat
set -e
pushd brat

# Download
wget http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz

# Extract
tar -xvzf brat-v1.3_Crunchy_Frog.tar.gz

popd
echo "Brat downloaded successfully"
