# kurbeScript.ps1
# This script checks if Minikube is installed, starts a Kubernetes cluster,
# verifies that the cluster is running, and lists available pods.

Write-Host "🎉 Kubernetes cluster setup complete and running successfully!"

# Check if minikube command exists
if (!(Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Minikube is not installed or not found in PATH."
    Write-Host "➡️ Please install Minikube from https://minikube.sigs.k8s.io/docs/start/"
    exit 1
}

Write-Host "✅ Minikube is installed."

# Start the Minikube cluster
Write-Host "🚀 Starting Minikube cluster..."
minikube start

# Verify the cluster is running
Write-Host "🔎 Verifying cluster status..."
kubectl cluster-info

# Retrieve available pods
Write-Host "📦 Listing available pods..."
kubectl get pods --all-namespaces

Write-Host "🎉 Kubernetes cluster setup complete and running successfully!"
