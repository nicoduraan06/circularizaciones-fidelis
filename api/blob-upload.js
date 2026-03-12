import { handleUpload } from '@vercel/blob';

export default async function handler(req, res) {

  const body = req.body;

  try {

    const jsonResponse = await handleUpload({
      body,
      request: req,

      onBeforeGenerateToken: async (pathname) => {

        return {
          allowedContentTypes: ['application/pdf'],
          tokenPayload: JSON.stringify({
            pathname
          })
        };

      },

      onUploadCompleted: async ({ blob, tokenPayload }) => {
        console.log("Upload completado:", blob, tokenPayload);
      }

    });

    return res.status(200).json(jsonResponse);

  } catch (error) {

    console.error(error);

    return res.status(400).json({
      error: 'Error en subida a Blob'
    });

  }

}