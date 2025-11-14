#!/bin/bash
# Script to deploy federated learning code to Hackathon cluster
# Usage: ./deploy_to_cluster.sh

CLUSTER_USER="team15"
CLUSTER_HOST1="129.212.178.168"
CLUSTER_HOST2="134.199.193.89"
CLUSTER_PORT="32605"

echo "=========================================="
echo "Deploying to Hackathon Cluster"
echo "=========================================="

# Create deployment package
echo "Creating deployment package..."
tar -czf federated_learning.tar.gz \
    flower_server/ \
    flower_client/ \
    output/ \
    scripts/run_federated_learning.py \
    scripts/test_model.py \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude="*.pt" \
    --exclude="models/"

echo "Package created: federated_learning.tar.gz"
echo ""
echo "To upload and run on cluster:"
echo "1. Upload package:"
echo "   scp -P $CLUSTER_PORT federated_learning.tar.gz $CLUSTER_USER@$CLUSTER_HOST1:~/"
echo ""
echo "2. SSH to cluster:"
echo "   ssh $CLUSTER_USER@$CLUSTER_HOST1 -p $CLUSTER_PORT"
echo ""
echo "3. Extract and run:"
echo "   tar -xzf federated_learning.tar.gz"
echo "   cd ~"
echo "   ./submit-job.sh 'python scripts/run_federated_learning.py' --name federated-learning"


