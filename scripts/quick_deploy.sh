#!/bin/bash
# Quick deployment script for Hackathon cluster
# This script prepares everything for deployment

CLUSTER_USER="team15"
CLUSTER_HOST="129.212.178.168"
CLUSTER_PORT="32605"

echo "=========================================="
echo "Quick Deployment to Hackathon Cluster"
echo "=========================================="
echo ""
echo "Step 1: Creating deployment package..."

# Create tar archive excluding unnecessary files
tar -czf federated_learning.tar.gz \
    flower_server/ \
    flower_client/ \
    output/ \
    scripts/run_federated_learning.py \
    scripts/test_model.py \
    scripts/run_server_cluster.sh \
    scripts/run_client_cluster.sh \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude="*.pt" \
    --exclude="models/" \
    --exclude=".git"

echo "✓ Package created: federated_learning.tar.gz"
echo ""
echo "Step 2: Upload instructions"
echo "============================"
echo ""
echo "Run these commands to upload and deploy:"
echo ""
echo "1. Upload package:"
echo "   scp -P $CLUSTER_PORT federated_learning.tar.gz $CLUSTER_USER@$CLUSTER_HOST:~/"
echo ""
echo "2. SSH to cluster:"
echo "   ssh $CLUSTER_USER@$CLUSTER_HOST -p $CLUSTER_PORT"
echo ""
echo "3. On cluster, extract and run:"
echo "   cd ~"
echo "   tar -xzf federated_learning.tar.gz"
echo "   chmod +x scripts/*.sh"
echo "   ./submit-job.sh 'python scripts/run_federated_learning.py' --name federated-learning --gpu"
echo ""
echo "Or use the all-in-one script:"
echo "   ./submit-job.sh 'bash scripts/run_all_cluster.sh' --name federated-learning --gpu"
echo ""


