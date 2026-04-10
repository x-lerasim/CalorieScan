const axios = require("axios");

const HF_MODEL = process.env.HF_MODEL || "nateraw/food";
const HF_API_URL =
  process.env.HF_API_URL ||
  `https://router.huggingface.co/hf-inference/models/${HF_MODEL}`;

async function classifyImage(imageBuffer) {
  const token = process.env.HF_TOKEN;
  if (!token) {
    const err = new Error("HF_TOKEN is not configured on the server");
    err.status = 503;
    throw err;
  }
  try {
    const response = await axios.post(HF_API_URL, imageBuffer, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/octet-stream"
      },
      timeout: 30000,
      maxBodyLength: Infinity,
      maxContentLength: Infinity
    });
    const data = response.data;
    if (!Array.isArray(data) || data.length === 0) {
      const err = new Error("Unexpected response from classification model");
      err.status = 502;
      throw err;
    }
    const top = data[0];
    return { label: String(top.label || "").toLowerCase(), confidence: Number(top.score || 0) };
  } catch (error) {
    if (error.response) {
      const err = new Error(
        `HuggingFace API error: ${error.response.status} ${JSON.stringify(error.response.data)}`
      );
      err.status = 502;
      throw err;
    }
    throw error;
  }
}

module.exports = { classifyImage };
