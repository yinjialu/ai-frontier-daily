#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'wechat-frontmatter-'));
const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const script = path.join(skillDir, 'scripts/push_draft.mjs');
const article = path.join(testDir, 'article.md');
const preview = path.join(testDir, 'preview.html');

fs.writeFileSync(article, `---
title: Hidden title
date: 2026-06-29
status: draft
cover: assets/cover.png
sources:
  - type: local_firsthand
    path: data/firsthand/example.md
---

# Visible title

Visible body.
`);

execFileSync(process.execPath, [
  script,
  '--file',
  article,
  '--title',
  'Visible title',
  '--preview-out',
  preview,
  '--dry-run',
], { stdio: 'pipe' });

const html = fs.readFileSync(preview, 'utf8');
assert.match(html, /Visible title/);
assert.match(html, /Visible body/);
assert.doesNotMatch(html, /Hidden title/);
assert.doesNotMatch(html, /sources:/);
assert.doesNotMatch(html, /local_firsthand/);
assert.doesNotMatch(html, /status: draft/);
