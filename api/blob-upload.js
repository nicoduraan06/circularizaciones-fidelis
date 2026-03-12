import { put } from '@vercel/blob';

export default async function handler(req, res) {

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {

    const filename = req.headers['x-vercel-filename'];
    const contentType = req.headers['content-type'];

    const blob = await put(
      filename,
      req,
      {
        access: 'private',
        contentType,
        token: process.env.BLOB_READ_WRITE_TOKEN
      }
    );

    return res.status(200).json(blob);

  } catch (error) {

    console.error("Error subiendo a Blob:", error);

    return res.status(500).json({
      error: "Error subiendo archivo a Blob"
    });

  }

}