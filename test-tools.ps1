# Test Function Calling Feature
# This script tests the OpenAI function calling capabilities

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing OpenAI Function Calling" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
Write-Host "Checking backend status..." -ForegroundColor Yellow
try {
    $status = Invoke-RestMethod -Uri "http://localhost:8000/status" -Method Get
    if ($status.has_api_key) {
        Write-Host "✓ Backend is running with API key configured" -ForegroundColor Green
    } else {
        Write-Host "✗ Backend is running but API key is not configured" -ForegroundColor Red
        Write-Host "Please set OPENAI_API_KEY in your .env file" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "✗ Backend is not responding" -ForegroundColor Red
    Write-Host "Please ensure Docker containers are running: docker-compose ps" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Listing available tools..." -ForegroundColor Yellow
try {
    $tools = Invoke-RestMethod -Uri "http://localhost:8000/tools" -Method Get
    Write-Host "✓ Found $($tools.count) available tools:" -ForegroundColor Green
    foreach ($func in $tools.available_functions) {
        Write-Host "  - $func" -ForegroundColor Cyan
    }
} catch {
    Write-Host "✗ Failed to fetch tools" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Test Queries" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Weather Query
Write-Host ""
Write-Host "Test 1: Weather Query" -ForegroundColor Magenta
Write-Host "Query: 'What's the weather in San Francisco?'" -ForegroundColor Gray
try {
    $body = @{
        message = "What's the weather in San Francisco?"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.reply)" -ForegroundColor White
    if ($response.used_tools) {
        Write-Host "✓ Tools were used!" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

# Test 2: Time Query
Write-Host ""
Write-Host "Test 2: Time Query" -ForegroundColor Magenta
Write-Host "Query: 'What time is it right now?'" -ForegroundColor Gray
try {
    $body = @{
        message = "What time is it right now?"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.reply)" -ForegroundColor White
    if ($response.used_tools) {
        Write-Host "✓ Tools were used!" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

# Test 3: Calculation
Write-Host ""
Write-Host "Test 3: Calculation" -ForegroundColor Magenta
Write-Host "Query: 'Calculate 25 * 4 + 100'" -ForegroundColor Gray
try {
    $body = @{
        message = "Calculate 25 * 4 + 100"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.reply)" -ForegroundColor White
    if ($response.used_tools) {
        Write-Host "✓ Tools were used!" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

# Test 4: Regular Chat (no tools needed)
Write-Host ""
Write-Host "Test 4: Regular Chat (no tools)" -ForegroundColor Magenta
Write-Host "Query: 'Tell me a fun fact about space'" -ForegroundColor Gray
try {
    $body = @{
        message = "Tell me a fun fact about space"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.reply)" -ForegroundColor White
    if (-not $response.used_tools) {
        Write-Host "✓ No tools needed for this query" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

# Test 5: Multiple Tools
Write-Host ""
Write-Host "Test 5: Multiple Tools" -ForegroundColor Magenta
Write-Host "Query: 'What's the weather in Tokyo and what time is it there?'" -ForegroundColor Gray
try {
    $body = @{
        message = "What's the weather in Tokyo and what time is it there?"
        use_tools = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.reply)" -ForegroundColor White
    if ($response.used_tools) {
        Write-Host "✓ Tools were used!" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tests Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now:" -ForegroundColor Yellow
Write-Host "1. Open http://localhost:4200 to use the chat interface" -ForegroundColor White
Write-Host "2. View API docs at http://localhost:8000/docs" -ForegroundColor White
Write-Host "3. Check the TOOLS_GUIDE.md for more information" -ForegroundColor White
Write-Host ""
