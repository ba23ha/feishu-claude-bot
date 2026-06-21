// Smoke test: verify eval files exist and are valid JSONL
const fs = require('fs');
const path = require('path');

const EVALS_DIR = path.join(__dirname, '..', 'evals');
const EVAL_FILES = ['review-cases.jsonl', 'daily-report-cases.jsonl'];

describe('eval files', () => {
  for (const filename of EVAL_FILES) {
    test(`${filename} is valid JSONL with at least 3 cases`, () => {
      const filePath = path.join(EVALS_DIR, filename);
      expect(fs.existsSync(filePath)).toBe(true);

      const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
      expect(lines.length).toBeGreaterThanOrEqual(3);

      for (const line of lines) {
        const parsed = JSON.parse(line);
        expect(parsed).toHaveProperty('input');
        expect(parsed).toHaveProperty('expected_traits');
        expect(Array.isArray(parsed.expected_traits)).toBe(true);
        expect(parsed).toHaveProperty('bad_patterns');
        expect(parsed).toHaveProperty('notes');
      }
    });
  }
});
