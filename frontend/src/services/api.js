const N8N_WEBHOOK_URL = import.meta.env.VITE_N8N_WEBHOOK_URL || "https://n8n.redinmex.com/webhook-test/86ce68b9-267c-4d46-b4c7-6651bffc116e";

export const uploadInvoice = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  // Determine file type based on MIME type or extension
  let fileType = "pdf";
  if (file.type === "text/xml" || file.type === "application/xml" || file.name.endsWith(".xml")) {
    fileType = "xml";
  }
  formData.append("fileType", fileType);

  try {
    const response = await fetch(N8N_WEBHOOK_URL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error uploading invoice:", error);
    throw error;
  }
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
