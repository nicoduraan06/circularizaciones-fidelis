import { handleUpload } from "@vercel/blob/client";

export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {

    const jsonResponse = await handleUpload({
      body: req.body,
      request: req,

      onBeforeGenerateToken: async (pathname) => {
        return {
          allowedContentTypes: ["application/pdf"],
          tokenPayload: JSON.stringify({ pathname })
        };
      },

      onUploadCompleted: async ({ blob, tokenPayload }) => {
        console.log("Upload completado:", blob, tokenPayload);
      }

    });

    return res.status(200).json(jsonResponse);

  } catch (error) {

    console.error("Blob upload error:", error);

    return res.status(500).json({
      error: "Error generating upload token"
    });

  }

}