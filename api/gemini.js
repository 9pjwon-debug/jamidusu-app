const MODEL = 'gemini-3.6-flash';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { prompt, maxTokens } = req.body || {};
  if (!prompt || typeof prompt !== 'string') {
    res.status(400).json({ error: 'prompt is required' });
    return;
  }

  const safeMaxTokens = Math.min(Math.max(parseInt(maxTokens, 10) || 1024, 1), 16000);

  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': process.env.GEMINI_API_KEY,
        },
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: safeMaxTokens },
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      console.error('gemini api error', data);
      res.status(502).json({ error: data.error?.message || 'gemini api request failed' });
      return;
    }

    const text = (data.candidates?.[0]?.content?.parts || [])
      .map((p) => p.text || '')
      .join('')
      .trim();

    if (!text) {
      res.status(502).json({ error: 'empty response from model' });
      return;
    }

    res.status(200).json({ text });
  } catch (error) {
    console.error('gemini request failed', error);
    res.status(502).json({ error: 'gemini api request failed' });
  }
}
