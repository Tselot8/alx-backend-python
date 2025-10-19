# kubctl-0x01
# PowerShell script to scale Django app and monitor performance

Write-Host "📈 Scaling Django app deployment to 3 replicas..." -ForegroundColor Cyan
kubectl scale deployment django-messaging-deployment --replicas=3

Start-Sleep -Seconds 10

Write-Host "🧩 Verifying running pods..." -ForegroundColor Yellow
kubectl get pods

Write-Host "🧠 Waiting a few seconds for pods to be ready..." -ForegroundColor DarkYellow
Start-Sleep -Seconds 15

Write-Host "🚀 Performing load testing using wrk..." -ForegroundColor Green
# Run load test against your Django app (adjust IP/port if needed)
wrk -t2 -c10 -d10s http://localhost:8000

Write-Host "📊 Monitoring resource usage..." -ForegroundColor Cyan
kubectl top pods

Write-Host "✅ Scaling, load testing, and monitoring complete!" -ForegroundColor Green
