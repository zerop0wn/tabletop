# Fixing Git Ownership Issues on EC2

If you get "dubious ownership" errors when using Git on EC2, use one of these solutions:

## Option 1: Add Safe Directory (Recommended)
```bash
git config --global --add safe.directory /opt/tabletop
```

## Option 2: Fix File Ownership
```bash
sudo chown -R ec2-user:ec2-user /opt/tabletop
```

## Option 3: Use Sudo for Git Operations
```bash
sudo git pull origin main
```

## After Fixing, Pull Latest Code:
```bash
git pull origin main
```

## If You Still Have Local Changes:
```bash
# Stash local changes
git stash

# Pull latest
git pull origin main

# If needed, reapply stashed changes
git stash pop
```

