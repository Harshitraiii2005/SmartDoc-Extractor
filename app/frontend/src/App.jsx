import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { saveAs } from "file-saver";
import { Download } from "lucide-react";
import axios from "axios";

export default function App() {
  const [textInput, setTextInput] = useState("");
  const [file, setFile] = useState(null);
  const [entities, setEntities] = useState([]);
  const [extractedText, setExtractedText] = useState("");

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    setFile(uploadedFile);
    const formData = new FormData();
    formData.append("document", uploadedFile);
    const response = await axios.post("/", formData);
    setExtractedText(response.data.extracted_text);
    setEntities(response.data.entities);
  };

  const handlePasteText = async () => {
    const response = await axios.post("/extract-text", { text: textInput });
    setExtractedText(response.data.extracted_text);
    setEntities(response.data.entities);
  };

  const handleDownloadPDF = () => {
    const blob = new Blob([JSON.stringify({ extractedText, entities }, null, 2)], {
      type: "application/pdf",
    });
    saveAs(blob, "extracted_data.pdf");
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-100 to-blue-200 p-8">
      <motion.h1
        className="text-4xl font-bold text-center text-indigo-800 mb-10"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        📄 SmartDoc Extractor
      </motion.h1>

      <div className="flex justify-center mb-10">
        <lottie-player
          src="https://assets10.lottiefiles.com/packages/lf20_hzgq1iov.json"
          background="transparent"
          speed="1"
          style={{ width: "300px", height: "300px" }}
          loop
          autoplay
        ></lottie-player>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-4 shadow-xl">
          <CardContent>
            <label className="block text-md font-medium mb-2">Upload Document</label>
            <Input type="file" onChange={handleFileUpload} />
          </CardContent>
        </Card>

        <Card className="p-4 shadow-xl">
          <CardContent>
            <label className="block text-md font-medium mb-2">Paste Text</label>
            <Textarea
              rows={6}
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Paste your text here..."
            />
            <Button className="mt-4" onClick={handlePasteText}>
              Extract Entities
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-10 p-4 shadow-xl">
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Extracted Text</h2>
          <p className="whitespace-pre-wrap text-gray-800 bg-white p-3 rounded-lg">
            {extractedText || "No content extracted yet."}
          </p>

          <h3 className="text-lg font-semibold mt-6">Entities</h3>
          <ul className="list-disc pl-5">
            {entities.map((ent, i) => (
              <li key={i} className="text-indigo-600">
                <strong>{ent.label}:</strong> {ent.text}
              </li>
            ))}
          </ul>

          {entities.length > 0 && (
            <Button className="mt-6" onClick={handleDownloadPDF}>
              <Download className="mr-2 h-5 w-5" /> Download as PDF
            </Button>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
