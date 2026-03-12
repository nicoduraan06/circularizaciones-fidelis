import { handleUpload } from "@vercel/blob/client";

export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {

    const body = req.body;

    const jsonResponse = await handleUpload({
      body,
      request: req,
      token: process.env.BLOB_READ_WRITE_TOKEN,
    });

    return res.status(200).json(jsonResponse);

  } catch (error) {

    console.error("Blob upload error:", error);

    return res.status(500).json({
      error: "Error generating upload token",
    });

  }
}