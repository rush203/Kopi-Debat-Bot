# Test script for Kopi Debate Bot API

Write-Host "Testing Kopi Debate Bot API..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
$healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method Get
Write-Host "Response: $($healthResponse | ConvertTo-Json)" -ForegroundColor Green
Write-Host ""

# Test 2: Start New Conversation
Write-Host "Test 2: Start New Debate Conversation" -ForegroundColor Yellow
$body = @{
    conversation_id = $null
    message = "I believe the Earth is flat and I can prove it with simple observations"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/debate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 60
    Write-Host "Success! Conversation ID: $($response.conversation_id)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bot's Response:" -ForegroundColor Cyan
    Write-Host $response.message[$response.message.Count - 1].message -ForegroundColor White
    Write-Host ""
    
    # Save conversation ID for next test
    $conversationId = $response.conversation_id
    
    # Test 3: Continue Conversation
    Write-Host "Test 3: Continue Conversation" -ForegroundColor Yellow
    $body2 = @{
        conversation_id = $conversationId
        message = "But what about satellite images showing Earth as a sphere?"
    } | ConvertTo-Json
    
    $response2 = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/debate" -Method Post -Body $body2 -ContentType "application/json" -TimeoutSec 60
    Write-Host "Success!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bot's Response:" -ForegroundColor Cyan
    Write-Host $response2.message[$response2.message.Count - 1].message -ForegroundColor White
    Write-Host ""
    
    Write-Host "All tests passed! ✓" -ForegroundColor Green
} catch {
    Write-Host "Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

