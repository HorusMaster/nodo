const BACKEND_URL = "http://localhost:8000/upload_multiple_files";

export const uploadInvoice = async (file) => {
  // Use the same backend endpoint for single file uploads
  return uploadMultipleFiles([file]);
};

export const uploadMultipleFiles = async (files) => {
  const formData = new FormData();

  // Append all files with the same key 'files'
  files.forEach(file => {
    formData.append("files", file);
  });

  // Backend URL (assuming localhost:8000 based on context)
  const BACKEND_URL = "http://localhost:8000/upload_multiple_files";

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error uploading multiple files:", error);
    throw error;
  }
};

// Mock function to simulate fetching file structure
// In a real scenario, this would hit another endpoint or the webhook would return the updated list
export const getFiles = async () => {
  // Simulating a delay
  await new Promise((resolve) => setTimeout(resolve, 500));

  // Mock data structure: Client -> Folio -> Files
  return [
    {
      client: "MANTENIMIENTO INDUSTRIAL Y COMERCIAL XICO",
      folios: [
        {
          id: "A-355",
          files: [
            { name: "factura.pdf", type: "invoice" },
            { name: "cotizacion.pdf", type: "quotation" }
          ]
        }
      ]
    }
  ];
};
