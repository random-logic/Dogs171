import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import "@mantine/core/styles.css";
import { Loader } from "@mantine/core";

function MyComponent() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const jsonData = await response.json();
      console.log(jsonData);
      return jsonData;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const classifyImage = () => {
    setTimeout(async () => {
      const response = await fetchData();
      setAnswer(response);
      setLoading(false);
    }, 1000);
  };

  return (
    <Grid container justifyContent="center" spacing={2}>
      <Grid item xs={12}>
        <Box textAlign="center" p={2}>
          <div>
            <h2>
              Welcome to dog classifier! Upload a picture of a dog below and we
              will tell you what breed it is.
            </h2>
          </div>
        </Box>
      </Grid>

      <Grid item xs={12}>
        <Box maxWidth="100vw" display="flex" justifyContent="center" p={2}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={6}>
              <Box
                p={2}
                textAlign="center"
                style={{ backgroundColor: "lightblue", borderRadius: "10px" }}
              >
                <input
                  id="image-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{ display: "none" }}
                />
                {selectedImage === null ? (
                  <h3>No image uploaded yet.</h3>
                ) : null}
                {selectedImage && (
                  <img
                    src={selectedImage}
                    alt="Uploaded"
                    style={{
                      maxWidth: "100%",
                      maxHeight: "100%",
                      padding: "10px",
                    }}
                  />
                )}
                <br></br>
                <label htmlFor="image-upload" style={{ cursor: "pointer" }}>
                  <p
                    style={{
                      background: "linear-gradient(to right, teal, teal)",
                      width: "40%",
                      margin: "auto",
                      borderRadius: "10px",
                      color: "white",
                      border: "2px solid black",
                      padding: "10px",
                    }}
                  >
                    {selectedImage === null
                      ? "Upload image"
                      : "Upload a different image"}
                  </p>
                </label>
                <br></br>
                {selectedImage !== null ? (
                  <button
                    style={{
                      backgroundColor: "rgba(249, 255, 207, 1)",
                      width: "40%",
                      margin: "auto",
                      borderRadius: "10px",
                      color: "black",
                      border: "2px solid black",
                      padding: "10px",
                      cursor: "pointer",
                    }}
                    onClick={() => {
                      setLoading(true);
                      classifyImage();
                    }}
                  >
                    Classify Dog
                  </button>
                ) : null}
              </Box>
            </Grid>
            <Grid item xs={6}>
              <Box
                p={2}
                textAlign="center"
                style={{ backgroundColor: "lightgreen", borderRadius: "10px" }}
              >
                <h3>
                  {answer === null
                    ? "Click classify dog to find its breed"
                    : `The dog you uploaded is a ${answer}`}
                </h3>
                {loading === true ? <Loader color="blue" /> : null}
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Grid>
    </Grid>
  );
}

export default MyComponent;
