import React, { useState, type FormEvent } from "react";
import "./SubmitData.css"
import {Label, Textarea,TextInput,Button,Sidebar, SidebarItem, SidebarItemGroup, SidebarItems } from "flowbite-react";
const JsonUploadForm: React.FC = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [sidebarOpen,setSidebarOpen] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please write a request");
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    // formData.append("description", description);
    formData.append("file", file);

    try {
      const response = await fetch("/api/collections/add", {
      method: "POST",
      body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage("Error uploading file");
      console.error(error);
    }
  };

  return (
    <div className="flex min-h-screen">
      <div className={`menu-toggle ${sidebarOpen ? "is-active" : ""}`} onClick={() => setSidebarOpen(!sidebarOpen)}>
        <div className="hamburguer">
          <span></span>
        </div>
      </div>
      <aside className={`sidebar ${sidebarOpen ? "is-active" : ""}`}>
        <h3>Menu</h3>
        <nav className="menu">
          <a href="/" className="menu-item is-active">Inicio</a>
          <a href="#" className="menu-item">Generar plan de estudios</a>
          <a href="#" className="menu-item">Contacto</a>
        </nav>
      </aside>
      <main className="flex-1 flex justify-center items-start p-8">
        <div className="form-container p-4 max-w-md">
          <h2 className="text-xl font-bold mb-2">UdeLearn</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <TextInput
                id = "title"
                type="text"
                placeholder="Rol (Especifique su rol: Estudiante, Profesor, etc.)"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />  
              {/* <Textarea
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="form-container-description w-full p-2 border rounded"
                rows={8}
                required
              /> */}
              <TextInput
                type="file"
                accept=".json"
                onChange={handleFileChange}
                className="form-container-fileButton w-full"
                required
                color="gray"
              />
              <div className="flex items-center justify-center">
                <Button pill
                type="submit"
                className=""
              >
                Aceptar
              </Button>
              </div>
            </form>
            {message && <p className="mt-4">{message}</p>}
          </div>
        </main>
    </div>
    
  );
};

export default JsonUploadForm;
