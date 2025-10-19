# Test Pushover Integration
# This script tests the Pushover notification system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Pushover Integration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
Write-Host "Checking backend status..." -ForegroundColor Yellow
try {
    $status = Invoke-RestMethod -Uri "http://localhost:8000/status" -Method Get
    Write-Host "✓ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend is not responding" -ForegroundColor Red
    Write-Host "Please ensure Docker containers are running: docker-compose ps" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test 1: Configuration Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

try {
    $testResult = Invoke-RestMethod -Uri "http://localhost:8000/test-pushover" -Method Post
    
    if ($testResult.configured) {
        Write-Host "✓ Pushover is configured" -ForegroundColor Green
        if ($testResult.success) {
            Write-Host "✓ Test notification sent successfully!" -ForegroundColor Green
            Write-Host "  Check your Pushover app for the test notification" -ForegroundColor Cyan
        } else {
            Write-Host "✗ Failed to send test notification" -ForegroundColor Red
            Write-Host "  Check your Pushover credentials in .env file" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠ Pushover is not configured" -ForegroundColor Yellow
        Write-Host "  To enable Pushover:" -ForegroundColor White
        Write-Host "  1. Create account at https://pushover.net/" -ForegroundColor White
        Write-Host "  2. Get your User Key from dashboard" -ForegroundColor White
        Write-Host "  3. Create app at https://pushover.net/apps/build" -ForegroundColor White
        Write-Host "  4. Add keys to .env file:" -ForegroundColor White
        Write-Host "     PUSHOVER_USER_KEY=your_user_key" -ForegroundColor Gray
        Write-Host "     PUSHOVER_API_TOKEN=your_api_token" -ForegroundColor Gray
        Write-Host "  5. Restart: docker-compose restart backend" -ForegroundColor White
        Write-Host ""
        Write-Host "  See PUSHOVER_INTEGRATION_GUIDE.md for detailed instructions" -ForegroundColor Cyan
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test 2: Insufficient Information Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Asking a question the bot can't answer..." -ForegroundColor Yellow
Write-Host "Query: 'What's the weather in Atlantis?'" -ForegroundColor Gray
Write-Host ""

try {
    $body = @{
        message = "What's the weather in Atlantis?"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Bot Response:" -ForegroundColor White
    Write-Host $response.reply -ForegroundColor Gray
    Write-Host ""
    
    if ($response.reply -match "not available|error|don't have") {
        Write-Host "✓ Insufficient information detected" -ForegroundColor Green
        Write-Host "  If Pushover is configured, you should receive a notification now!" -ForegroundColor Cyan
    } else {
        Write-Host "ℹ Response doesn't indicate insufficient information" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Chat test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test 3: Normal Query (No Notification)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Asking a question the bot CAN answer..." -ForegroundColor Yellow
Write-Host "Query: 'What's the weather in Tokyo?'" -ForegroundColor Gray
Write-Host ""

try {
    $body = @{
        message = "What's the weather in Tokyo?"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Bot Response:" -ForegroundColor White
    Write-Host $response.reply -ForegroundColor Gray
    Write-Host ""
    Write-Host "✓ Normal response - No notification should be sent" -ForegroundColor Green
} catch {
    Write-Host "✗ Chat test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Additional Test Queries" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Try these queries to trigger notifications:" -ForegroundColor Yellow
Write-Host "  1. 'What's the weather in Narnia?'" -ForegroundColor White
Write-Host "  2. 'What's the weather in Middle Earth?'" -ForegroundColor White
Write-Host "  3. 'What's the weather in Hogwarts?'" -ForegroundColor White
Write-Host "  4. 'What's the weather in Gotham City?'" -ForegroundColor White
Write-Host ""
Write-Host "These should NOT trigger notifications:" -ForegroundColor Yellow
Write-Host "  1. 'What's the weather in San Francisco?'" -ForegroundColor White
Write-Host "  2. 'Calculate 50 * 20'" -ForegroundColor White
Write-Host "  3. 'What time is it?'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pushover Integration Features:" -ForegroundColor White
Write-Host "  ✓ Detects insufficient information responses" -ForegroundColor Green
Write-Host "  ✓ Sends real-time notifications to your device" -ForegroundColor Green
Write-Host "  ✓ Includes query and response in notification" -ForegroundColor Green
Write-Host "  ✓ Helps identify knowledge gaps" -ForegroundColor Green
Write-Host ""
Write-Host "For more information:" -ForegroundColor White
Write-Host "  - Read PUSHOVER_INTEGRATION_GUIDE.md" -ForegroundColor Cyan
Write-Host "  - Visit https://pushover.net/" -ForegroundColor Cyan
Write-Host "  - Check backend logs: docker logs chatbot-backend" -ForegroundColor Cyan
Write-Host ""
