const { spawn } = require('child_process');

const TIMEOUT_MS = 120000; // 2 min — soul distillation can be slow

/**
 * Generate a response using the local `claude` CLI (Claude Code).
 * No API key required — uses the authenticated Claude Code session.
 *
 * @param {string} systemPrompt
 * @param {string} userMessage
 * @param {object} [opts]
 * @param {number} [opts.timeoutMs]
 * @returns {Promise<string>}
 */
async function generate(systemPrompt, userMessage, opts = {}) {
  const timeoutMs = opts.timeoutMs || TIMEOUT_MS;

  // Combine system + user into one prompt.
  // Claude CLI (-p mode) doesn't expose a separate --system-prompt flag,
  // so we use XML tags that the model understands as system context.
  const fullPrompt = systemPrompt
    ? `<system>\n${systemPrompt}\n</system>\n\n${userMessage}`
    : userMessage;

  return new Promise((resolve, reject) => {
    const proc = spawn('claude', ['-p', fullPrompt], {
      env: { ...process.env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';

    const timer = setTimeout(() => {
      proc.kill('SIGTERM');
      reject(new Error(`claude CLI timed out after ${timeoutMs / 1000}s`));
    }, timeoutMs);

    proc.stdout.on('data', d => { stdout += d; });
    proc.stderr.on('data', d => { stderr += d; });

    proc.on('close', code => {
      clearTimeout(timer);
      if (code !== 0) {
        reject(new Error(`claude exited ${code}: ${stderr.slice(0, 300)}`));
      } else {
        resolve(stdout.trim());
      }
    });

    proc.on('error', err => {
      clearTimeout(timer);
      reject(new Error(`claude CLI not found or not executable: ${err.message}`));
    });
  });
}

module.exports = { generate };
