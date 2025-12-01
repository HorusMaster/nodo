export const uploadInvoice = async (file, isTestMode = false) => {
  // Use the same backend endpoint for single file uploads
  return uploadMultipleFiles([file], isTestMode);
};

export const uploadMultipleFiles = async (files, isTestMode = false) => {
  const formData = new FormData();

  // Append all files with the same key 'files'
  files.forEach(file => {
    formData.append("files", file);
  });

  // Choose endpoint based on test mode
  const endpoint = isTestMode ? "upload_multiple_files_test" : "upload_multiple_files";

  // Use environment variable for backend URL, fallback to localhost for development
  const BACKEND_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
  const BACKEND_URL = `${BACKEND_BASE}/${endpoint}`;

  // Create an AbortController for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

  try {
    console.log(`Uploading ${files.length} files to ${BACKEND_URL}...`);

    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Server error (${response.status}):`, errorText);
      throw new Error(`Upload failed: ${response.status} - ${errorText || response.statusText}`);
    }

    const result = await response.json();
    console.log("Upload successful:", result);
    return result;

  } catch (error) {
    clearTimeout(timeoutId);

    // Provide more specific error messages
    if (error.name === 'AbortError') {
      console.error("Upload timeout after 30 seconds");
      throw new Error("Upload timeout - the server took too long to respond");
    } else if (error instanceof TypeError && error.message === 'Failed to fetch') {
      console.error("Network error - cannot connect to backend server");
      throw new Error("Cannot connect to server. Please ensure the backend is running on http://localhost:8000");
    } else {
      console.error("Error uploading multiple files:", error);
      throw error;
    }
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
