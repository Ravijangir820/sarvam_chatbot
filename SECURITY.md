# 🔒 Security Alert & Key Rotation Guide

## ⚠️ Critical: API Key Exposure Risk

Your Sarvam AI API key may have been exposed if the `.env` file was pushed to GitHub before proper `.gitignore` setup.

## ✅ What I've Done

I've updated `.gitignore` to properly exclude:
- `.env` files
- `*.env` files
- Any environment variable files

## 🔧 Immediate Actions Required

### Step 1: Rotate Your API Key (URGENT)

If you've already pushed code to GitHub with the `.env` file:

1. Go to **Sarvam Dashboard**: https://dashboard.sarvam.ai/
2. Navigate to **API Keys** section
3. **Regenerate/Rotate** your API key
4. **Delete** the old exposed key
5. Copy the new API key

### Step 2: Update Local `.env` File

Paste the new API key into your `.env`:

```env
SARVAM_API_KEY=sk_your_new_key_here
SARVAM_API_BASE_URL=https://api.sarvam.ai
```

### Step 3: Clean Git History (if committed)

If the `.env` was already committed to Git:

```bash
# Remove .env from git history (one-time operation)
git rm --cached .env
git commit -m "Remove .env file from git history"
git push origin main
```

### Step 4: Verify .gitignore Works

```bash
# Check if .env is properly ignored now
git status
```

You should NOT see `.env` in the output.

## 🛡️ Best Practices Going Forward

### DO:
✅ Keep `.env` in `.gitignore`
✅ Use environment variables in production
✅ Rotate keys periodically
✅ Never hardcode sensitive data
✅ Review git history before pushing
✅ Use `.env.example` for configuration templates

### DON'T:
❌ Commit `.env` files
❌ Share API keys in messages/emails
❌ Hardcode keys in source code
❌ Push private keys to public repositories
❌ Reuse old exposed keys

## 📝 Create `.env.example` (Safe Template)

Create a template file for other developers:

```bash
# .env.example
SARVAM_API_KEY=your_api_key_here
SARVAM_API_BASE_URL=https://api.sarvam.ai
```

Then add to git:
```bash
git add .env.example
git commit -m "Add .env.example (no sensitive keys)"
git push
```

## 🔍 Verify Your Setup

```bash
# 1. Check if git would ignore .env
git check-ignore -v .env
# Expected output: ".env" is explicitly ignored

# 2. Verify .env has the new key
cat .env
# Should show: SARVAM_API_KEY=sk_your_new_key...

# 3. Test the API
python test_api.py
```

## 🚨 If Key Was Publicly Exposed

### Immediate Steps:
1. **Regenerate key immediately** ⚡
2. **Monitor usage**: Check API logs for unauthorized calls
3. **Notify Sarvam Support** (if enterprise account)
4. **Clean git history**: Use the commands above
5. **Update all deployments**: Dev, staging, production

### Check for Unauthorized Usage:
- Log into Sarvam Dashboard
- Review API usage statistics
- Look for unusual activity patterns
- Check billing for unexpected charges

## 📦 Deployment Security

### For Production:
```bash
# Use environment variables, NEVER push .env
export SARVAM_API_KEY="your_production_key"
python app.py
```

### For Docker:
```dockerfile
# Never copy .env
RUN echo "SARVAM_API_KEY=${SARVAM_API_KEY}" > app/.env
# Instead use --build-arg or secrets
```

### For CI/CD (GitHub Actions, etc):
```yaml
# Add secret in GitHub Settings > Secrets
- name: Run tests
  env:
    SARVAM_API_KEY: ${{ secrets.SARVAM_API_KEY }}
  run: python test_api.py
```

## ✅ Security Checklist

- [ ] API key rotated (new key generated)
- [ ] Old key deleted from Sarvam Dashboard
- [ ] `.env` updated with new key locally
- [ ] `.gitignore` updated to exclude `.env`
- [ ] `.env.example` created as template
- [ ] Git history cleaned (if needed)
- [ ] `.env` removed from git tracking
- [ ] Verified with `git check-ignore`
- [ ] Tested API with `python test_api.py`
- [ ] All deployments updated with new key

## 📞 Support

- **Sarvam Dashboard**: https://dashboard.sarvam.ai/
- **Docs**: https://docs.sarvam.ai/
- **Discord**: https://discord.com/invite/5rAsykttcs

---

**Remember: Security is everyone's responsibility! 🔐**

Once you've completed these steps, your repository will be secure.
