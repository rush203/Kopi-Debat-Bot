# 🧪 API Testing Guide - Kopi Debate Bot

## 📥 Quick Start with Postman

### Import the Collection
1. Open Postman
2. Click **Import** button (top left)
3. Select the file: `Kopi_Debate_Bot_Tests.postman_collection.json`
4. The collection will load with all tests ready to run

### Run Tests
- **Run single test**: Click on any request → Click "Send"
- **Run entire folder**: Right-click folder → "Run folder"
- **Run all tests**: Click collection → "Run collection"

---

## 🎯 Manual Testing Examples

### ✅ Test 1: Flat Earth Debate (RECOMMENDED FIRST TEST)

#### Request 1: Start Conversation
**POST** `http://localhost:8000/api/v1/debate`

**Body:**
```json
{
  "conversation_id": null,
  "message": "I believe the Earth is flat and I can prove it with simple observations"
}
```

**Expected Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": [
    {
      "role": "user",
      "message": "I believe the Earth is flat and I can prove it with simple observations"
    },
    {
      "role": "bot",
      "message": "Absolutely! The evidence for a flat Earth is compelling when you examine everyday observations..."
    }
  ]
}
```

**✏️ Save the `conversation_id` from the response!**

---

#### Request 2: Continue Conversation
**POST** `http://localhost:8000/api/v1/debate`

**Body:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "But what about satellite images showing Earth as a sphere?"
}
```

**What to Check:**
- ✅ Bot maintains flat earth position
- ✅ Provides counter-arguments (CGI, fish-eye lenses, etc.)
- ✅ Response is persuasive but not overly argumentative
- ✅ Stays on topic

---

#### Continue Testing (Requests 3-6+)

**Request 3:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "How do you explain ships disappearing over the horizon bottom-first?"
}
```

**Request 4:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "Thousands of scientists have measured Earth's curvature. Are they all lying?"
}
```

**Request 5:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "What about gravity? How does it work on a flat Earth?"
}
```

**Request 6:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "How do you explain different time zones if the Earth is flat?"
}
```

**Request 7:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "Pilots and sailors use spherical navigation. Why does it work?"
}
```

**Request 8:**
```json
{
  "conversation_id": "SAME_UUID",
  "message": "We have photos from space stations showing a round Earth"
}
```

---

### ✅ Test 2: Climate Change Debate

**Start:**
```json
{
  "conversation_id": null,
  "message": "Climate change is just a natural cycle, humans have nothing to do with it"
}
```

**Continue with:**
- "CO2 levels are at record highs according to ice core data"
- "97% of climate scientists agree humans are causing it"
- "Arctic ice is melting at unprecedented rates"
- "The correlation between industrial activity and warming is clear"
- "What about ocean acidification from CO2 absorption?"

---

### ✅ Test 3: Vaccines Debate

**Start:**
```json
{
  "conversation_id": null,
  "message": "Natural immunity is superior to vaccines in every way"
}
```

**Continue with:**
- "Vaccines have eradicated smallpox completely"
- "What about immunocompromised people who can't develop immunity?"
- "Herd immunity protects vulnerable populations"
- "Vaccine side effects are minimal compared to disease risks"

---

### ✅ Test 4: Fun Debate - Pineapple Pizza

**Start:**
```json
{
  "conversation_id": null,
  "message": "Pineapple on pizza is an abomination that ruins Italian cuisine"
}
```

**Continue with:**
- "Sweet and savory combinations work in many cuisines"
- "Hawaiian pizza is one of the most popular worldwide"
- "Italians put honey on cheese, so why not pineapple?"

---

## ❌ Error Testing

### Test: Invalid Conversation ID
**Expected: 404 NOT FOUND**
```json
{
  "conversation_id": "invalid-uuid-12345",
  "message": "This should fail"
}
```

### Test: Empty Message
**Expected: 422 UNPROCESSABLE ENTITY**
```json
{
  "conversation_id": null,
  "message": ""
}
```

### Test: Missing Message Field
**Expected: 422 UNPROCESSABLE ENTITY**
```json
{
  "conversation_id": null
}
```

---

## 📊 What to Evaluate

### ✅ Conversation Coherence
- [ ] Bot remembers previous arguments
- [ ] No contradictions across messages
- [ ] Topic stays consistent
- [ ] References earlier points made

### ✅ Persuasiveness
- [ ] Arguments are logical (within the stance)
- [ ] Uses evidence and examples
- [ ] Addresses counterarguments
- [ ] Not overly aggressive or dismissive

### ✅ Position Maintenance
- [ ] Never concedes or agrees with opponent
- [ ] Always defends original stance
- [ ] Finds creative counterarguments
- [ ] Stays on the defensive side

### ✅ Technical Requirements
- [ ] Response time < 30 seconds
- [ ] Handles 5+ message exchanges
- [ ] Proper JSON response format
- [ ] Correct status codes
- [ ] conversation_id maintained

---

## 🔍 Advanced Testing Scenarios

### Scenario 1: Very Long Conversation (10+ messages)
Test if bot maintains coherence over extended debate

### Scenario 2: Multiple Simultaneous Conversations
- Start Conversation A (Flat Earth)
- Start Conversation B (Climate Change)
- Alternate between A and B
- Verify no topic mixing

### Scenario 3: Contradictory Challenges
Present contradictory evidence in sequence to test consistency

### Scenario 4: Edge Cases
- Very short messages: "Why?"
- Very long messages: Full paragraphs
- Special characters in messages
- Different languages (if supported)

---

## 📈 Success Criteria

| Criterion | Target | Notes |
|-----------|--------|-------|
| Response Time | < 30s | Per API call |
| Min Conversation Length | 5+ messages | Should handle more |
| Position Consistency | 100% | Never concede |
| Coherence | High | No contradictions |
| Persuasiveness | Subjective | Judge quality |
| Error Handling | Proper codes | 404, 422, etc. |

---

## 🐛 Common Issues

### Issue: "Connection refused"
**Solution:** Ensure Docker container is running
```bash
docker-compose ps
docker-compose logs api
```

### Issue: Bot gives generic responses
**Solution:** Check OpenAI API key is set in `.env`

### Issue: 500 Internal Server Error
**Solution:** Check logs for API errors
```bash
docker-compose logs --tail 50 api
```

### Issue: Slow responses
**Solution:** 
- Check network connection
- Verify OpenRouter/OpenAI API status
- Consider reducing `OPENAI_MAX_TOKENS` in `.env`

---

## 📝 Testing Checklist

- [ ] Import Postman collection
- [ ] Test Health endpoint
- [ ] Start Flat Earth debate
- [ ] Complete 5+ message exchanges
- [ ] Verify bot maintains position
- [ ] Test multiple debate topics
- [ ] Test error scenarios
- [ ] Test concurrent conversations
- [ ] Verify response times
- [ ] Check conversation coherence
- [ ] Evaluate persuasiveness

---

## 🎓 Tips for Best Results

1. **Be Specific**: Give detailed arguments for better responses
2. **Use Facts**: Present real counterarguments
3. **Stay on Topic**: Don't jump between unrelated points
4. **Be Patient**: First response may take 5-10 seconds
5. **Save UUIDs**: Always copy conversation_id for continuation

---

## 📞 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/debate` | POST | Main debate endpoint |
| `/api/v1/health` | GET | Health check |
| `/docs` | GET | Interactive API documentation |
| `/redoc` | GET | Alternative API documentation |
| `/` | GET | Service info |

---

## 🚀 Quick Commands

```bash
# Check if server is running
curl http://localhost:8000/api/v1/health

# View logs
docker-compose logs -f api

# Restart server
docker-compose restart

# Stop server
docker-compose down

# Start server
docker-compose up -d
```

---

**Happy Testing! 🎉**


