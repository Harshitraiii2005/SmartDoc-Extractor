import React, { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import { saveAs } from "file-saver";

export default function App() {
  const [file, setFile] = useState(null);
  const [entities, setEntities] = useState([]);
  const [textInput, setTextInput] = useState("");
  const [extractedText, setExtractedText] = useState("");

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    setFile(uploadedFile);

    const formData = new FormData();
    formData.append("file", uploadedFile);

    const response = await axios.post("/extract", formData);
    setExtractedText(response.data.extracted_text);
    setEntities(response.data.entities);
  };

  const handleDownloadPDF = async () => {
    const res = await axios.get("/download_pdf", {
      responseType: "blob",
    });
    saveAs(res.data, "SmartDoc_Extracted.pdf");
  };

  return (
    <main className="relative min-h-screen bg-[#0b0c10] text-white p-6">
      <div className="absolute top-0 left-0 z-0 w-full h-full opacity-30">
        <lottie-player
          src="https://assets2.lottiefiles.com/packages/lf20_Xw0Y4v.json"
          background="transparent"
          speed="1"
          loop
          autoplay
        ></lottie-player>
      </div>

      <motion.div
        initial={{ opacity: 0, y: -60 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 text-center mb-12"
      >
        <h1 className="text-4xl font-bold text-purple-400">SmartDoc Extractor</h1>
        <p className="text-gray-400 mt-2">Upload a document to extract structured text and entities</p>
      </motion.div>

      <div className="relative z-10 grid md:grid-cols-2 gap-8">
        <div className="bg-black bg-opacity-40 p-6 rounded-lg shadow-md">
          <label className="block mb-2 text-purple-300 font-semibold">Upload File</label>
          <input
            type="file"
            onChange={handleFileUpload}
            className="bg-gray-900 p-2 rounded border border-purple-500 w-full"
          />
        </div>

        <div className="bg-black bg-opacity-40 p-6 rounded-lg shadow-md">
          <label className="block mb-2 text-purple-300 font-semibold">Or Paste Text</label>
          <textarea
            rows="6"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            className="bg-gray-900 p-3 rounded w-full border border-purple-500"
            placeholder="Paste your text here..."
          ></textarea>
          <button
            onClick={async () => {
              const res = await axios.post("/extract-text", { text: textInput });
              setExtractedText(res.data.extracted_text);
              setEntities(res.data.entities);
            }}
            className="mt-4 bg-purple-600 hover:bg-purple-800 text-white px-4 py-2 rounded"
          >
            Extract
          </button>
        </div>
      </div>

      {extractedText && (
        <div className="relative z-10 mt-12">
          <h2 className="text-2xl font-semibold text-purple-400 mb-4">📄 Extracted Text</h2>
          <div className="bg-[#1a1a2e] p-4 rounded-lg text-gray-300 whitespace-pre-wrap overflow-auto max-h-[300px]">
            {extractedText}
          </div>

          <h2 className="text-2xl font-semibold text-purple-400 mt-8 mb-4">🔍 Entities</h2>
          <div className="flex flex-wrap gap-4">
            {entities.map((ent, i) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.05, rotate: 2 }}
                className="bg-purple-800 p-3 rounded shadow-md w-64"
              >
                <strong className="text-sm text-white">{ent.label}</strong>
                <p className="text-gray-200 text-sm mt-1">{ent.text}</p>
              </motion.div>
            ))}
          </div>

          {entities.length > 0 && (
            <button
              onClick={handleDownloadPDF}
              className="mt-6 bg-purple-700 hover:bg-purple-900 text-white px-6 py-3 rounded"
            >
              ⬇ Download PDF
            </button>
          )}
        </div>
      )}
    </main>
  );
}
