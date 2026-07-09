# Security Specification

## 1. Data Invariants
- Users can only read and write their own ST-5 and Behavior records.
- User profiles can only be updated by the owner.
- `username` must be unique and match the document ID.

## 2. The Dirty Dozen Payloads
1. Create user with shadow fields.
2. Update user profile as another user.
3. Read another user's ST-5 record.
4. Create ST-5 record for another user.
5. Create ST-5 record with invalid score type.
6. Delete another user's Behavior record.
7. Update user profile with different role.
8. Create Behavior record missing required fields.
9. Inject malicious ID for user profile.
10. Excessive array size (if applicable).
11. Update immutable fields like `createdAt`.
12. Read all users list without admin privileges.

## 3. Test Runner
We will use `@firebase/rules-unit-testing` to verify these invariants.
