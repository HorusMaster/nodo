import { useState } from 'react';
import { Upload, FileText, Folder, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { uploadInvoice, getFiles, uploadMultipleFiles } from './services/api';

function App() {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [isTestMode, setIsTestMode] = useState(false); // Toggle between test and production

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) {
      await handleUploadFiles(droppedFiles);
    }
  };

  const handleFileSelect = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFiles = Array.from(e.target.files);
      await handleUploadFiles(selectedFiles);
    }
  };

  const handleUploadFiles = async (filesToUpload) => {
    const validFiles = filesToUpload.filter(file =>
      file.type === 'application/pdf' || file.type === 'text/xml' || file.type === 'application/xml'
    );

    if (validFiles.length === 0) {
      alert("Please upload PDF or XML files.");
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);
    setErrorMessage('');

    try {
      // Use the new bulk upload function (test or production)
      const result = await uploadMultipleFiles(validFiles, isTestMode);

      console.log("Upload result:", result);
      setUploadStatus('success');

      // Refresh file list (mocked for now)
      const updatedFiles = await getFiles();
      setFiles(updatedFiles);

    } catch (error) {
      console.error(error);
      setUploadStatus('error');
      setErrorMessage(error.message || 'Unknown error occurred');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans selection:bg-pink-500 selection:text-white">
      <div className="max-w-4xl mx-auto space-y-12">

        {/* Header */}
        <header className="text-center space-y-4">
          <h1 className="text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500">
            Invoice Processor
          </h1>
          <p className="text-gray-400 text-lg">
            Upload your invoices to automatically generate quotations.
          </p>

          {/* Test Mode Toggle */}
          <div className="flex items-center justify-center gap-5 mt-8">
            <span className={`text-lg font-bold ${!isTestMode ? 'text-green-400' : 'text-gray-500'}`}>
              PRODUCCIÓN
            </span>
            <button
              onClick={() => setIsTestMode(!isTestMode)}
              className={`
                relative w-24 h-12 rounded-full transition-all duration-300 shadow-xl
                ${isTestMode ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-green-500 hover:bg-green-600'}
              `}
            >
              <div className={`
                absolute top-1.5 w-9 h-9 bg-white rounded-full shadow-lg transition-all duration-300
                ${isTestMode ? 'left-[54px]' : 'left-1.5'}
              `} />
            </button>
            <span className={`text-lg font-bold ${isTestMode ? 'text-yellow-400' : 'text-gray-500'}`}>
              TEST
            </span>
          </div>
        </header>

        {/* Upload Zone */}
        <div
          className={`
            relative group cursor-pointer
            border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300
            ${isDragging
              ? 'border-pink-500 bg-pink-500/10 scale-[1.02]'
              : 'border-gray-700 hover:border-purple-500 hover:bg-gray-800/50'
            }
          `}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <input
            type="file"
            id="fileInput"
            className="hidden"
            accept=".pdf,.xml"
            multiple
            onChange={handleFileSelect}
          />

          <div className="flex flex-col items-center space-y-6 pointer-events-none">
            <div className={`
              p-6 rounded-full bg-gradient-to-br from-gray-800 to-gray-900 shadow-2xl
              group-hover:shadow-purple-500/20 transition-shadow duration-300
            `}>
              {isUploading ? (
                <Loader2 className="w-12 h-12 text-purple-500 animate-spin" />
              ) : (
                <Upload className="w-12 h-12 text-gray-400 group-hover:text-white transition-colors" />
              )}
            </div>
            <div className="space-y-2">
              <p className="text-xl font-semibold text-gray-200">
                {isUploading ? "Processing..." : "Subir Archivos Multiples"}
              </p>
              <p className="text-sm text-gray-500">or click to browse</p>
            </div>
          </div>

          {/* Status Messages */}
          {uploadStatus === 'success' && (
            <div className="absolute top-4 right-4 flex items-center space-x-2 text-green-400 bg-green-400/10 px-4 py-2 rounded-full animate-in fade-in slide-in-from-bottom-2">
              <CheckCircle className="w-4 h-4" />
              <span className="text-sm font-medium">Uploaded Successfully</span>
            </div>
          )}
          {uploadStatus === 'error' && (
            <div className="absolute top-4 right-4 flex flex-col space-y-1 text-red-400 bg-red-400/10 px-4 py-2 rounded-lg animate-in fade-in slide-in-from-bottom-2 max-w-md">
              <div className="flex items-center space-x-2">
                <AlertCircle className="w-4 h-4" />
                <span className="text-sm font-medium">Upload Failed</span>
              </div>
              {errorMessage && (
                <span className="text-xs text-red-300 pl-6">{errorMessage}</span>
              )}
            </div>
          )}
        </div>

        {/* File Explorer */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-200 flex items-center space-x-2">
            <Folder className="w-6 h-6 text-purple-500" />
            <span>Processed Files</span>
          </h2>

          <div className="grid gap-6">
            {files.length === 0 ? (
              <div className="text-center py-12 bg-gray-800/30 rounded-2xl border border-gray-800">
                <p className="text-gray-500">No files processed yet.</p>
              </div>
            ) : (
              files.map((client, idx) => (
                <div key={idx} className="bg-gray-800/40 backdrop-blur-xl border border-gray-700/50 rounded-2xl overflow-hidden">
                  <div className="bg-gray-800/60 px-6 py-4 border-b border-gray-700/50 flex items-center space-x-3">
                    <div className="w-3 h-3 rounded-full bg-pink-500"></div>
                    <h3 className="font-semibold text-gray-200">{client.client}</h3>
                  </div>

                  <div className="p-6 space-y-6">
                    {client.folios.map((folio, fIdx) => (
                      <div key={fIdx} className="space-y-3">
                        <div className="flex items-center space-x-2 text-sm text-gray-400 uppercase tracking-wider font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                          <span>Folio: {folio.id}</span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pl-4">
                          {folio.files.map((file, fileIdx) => (
                            <div key={fileIdx} className="group flex items-center p-4 bg-gray-900/50 hover:bg-gray-700/50 rounded-xl border border-gray-800 hover:border-gray-600 transition-all cursor-pointer">
                              <div className="p-3 bg-gray-800 rounded-lg mr-4 group-hover:bg-gray-700 transition-colors">
                                <FileText className="w-6 h-6 text-indigo-400" />
                              </div>
                              <div>
                                <p className="font-medium text-gray-200 group-hover:text-white transition-colors">{file.name}</p>
                                <p className="text-xs text-gray-500 capitalize">{file.type}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
