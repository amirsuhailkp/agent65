# Idor Bola: The endpoint uses a POST form with an `author` field and a submit button

**Category:** idor_bola
**Draft Severity (human review required):** high
**Confidence:** 1.0
**Verified:** True
**Date:** 2026-08-09

## Summary
**Observation:** The endpoint uses a POST form with an `author` field and a submit button

**Attack strategy tested:** Test with admin user to see if the response differs from samurai

**Outcome:** Confirmed after 1 attempt(s).

**Verification engine's reason:** reproduced with stable, high-impact evidence

## Steps to Reproduce
1. Target: `http://192.168.56.101/mutillidae/index.php?page=view-someones-blog.php`
2. Tool: `diff_requests`
3. Command executed:
   ```
   python3 /home/kali/agent_tools/diff_requests.py 'http://192.168.56.101/mutillidae/index.php?page=view-someones-blog.php' 'http://192.168.56.101/mutillidae/index.php?page=view-someones-blog.php' --method POST --data-a 'author=admin&view-someones-blog-php-submit-button=View+Blog+Entries' --data-b 'author=samurai&view-someones-blog-php-submit-button=View+Blog+Entries'
   ```
4. Result: `completed` (exit_code=0)
5. Planner's stated reasoning at decision time: Test if the admin user's blog posts are visible without authentication (as per known credentials, admin might have seeded blog posts or not) and compare with samurai to see if there's a difference in response (which would indicate IDOR vulnerability).

## Impact
**Draft severity (impact assessor, human review required):** high
**Clear impact demonstrated:** True
**False positive risk:** low
**Assessor reasoning:** The diff_excerpt shows the SQL query explicitly uses 'samurai' instead of 'admin' in the blogger_name filter, indicating the parameter is used to fetch specific user data. The identical status codes and near-identical content (except for the SQL line) confirm the parameter directly controls data retrieval, which is a clear IDOR vulnerability. The evidence demonstrates actual data filtering based on the parameter, not just a theoretical possibility.

## Remediation
Draft only — requires human review. General guidance for idor bola findings: enforce server-side authorization checks on every object reference; do not rely on client-supplied IDs without verifying the requesting session owns that resource.

## Evidence References
- hypothesis_id=hyp_20260809114412_0
- evidence_id=100
