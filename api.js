import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

export const analyzeSentiment = async (text) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze/`, { text });
    return response.data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    throw error;
  }
};

export const convertVoiceToText = async (audioFile) => {
  try {
    const formData = new FormData();
    formData.append('file', audioFile);
    const response = await axios.post(`${API_BASE_URL}/voice/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error converting voice to text:', error);
    throw error;
  }
};

export const convertTextToSpeech = async (text) => {
  // Validate input
  if (typeof text !== "string" || !text.trim()) {
    throw new Error("Text must be a non-empty string");
  }

  try {
    const response = await axios.post(
      `${API_BASE_URL}/voice/tts`,
      { text: text.trim() },  // Explicit key-value format
      {
        responseType: "blob",
        headers: {
          "Content-Type": "application/json",
          "Accept": "audio/wav"
        },
        transformRequest: [data => JSON.stringify(data)],  // Ensures proper JSON
        timeout: 10000
      }
    );

    // Handle JSON error responses
    if (response.data.type === "application/json") {
      const errorData = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(JSON.parse(reader.result));
        reader.readAsText(response.data);
      });
      throw new Error(errorData.detail || "TTS conversion failed");
    }

    return URL.createObjectURL(
      new Blob([response.data], { type: "audio/wav" })
    );
  } catch (error) {
    console.error("Full error context:", {
      request: error.config?.data,
      status: error.response?.status,
      headers: error.response?.headers,
      response: error.response?.data
    });
    throw new Error(`TTS failed: ${error.message}`);
  }
};

const speak = async (text) => {
  if (!text || typeof text !== 'string') {
    console.error('Invalid text input');
    return;
  }

  try {
    console.log("Requesting TTS for:", text.substring(0, 50) + (text.length > 50 ? "..." : ""));
    
    const audioUrl = await convertTextToSpeech(text);
    console.log("Audio generated successfully");
    
    const audio = new Audio(audioUrl);
    
    audio.onerror = (e) => {
      console.error('Audio playback error:', e);
    };
    
    await audio.play();
    
    // Clean up object URL after playback completes
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
      console.log("Playback completed");
    };
    
  } catch (err) {
    console.error('Speak function error:', err);
    
    // Handle specific error cases
    if (err.response) {
      if (err.response.status === 422) {
        console.error("Validation error - check your input text");
      } else if (err.response.status === 400) {
        console.error("Bad request:", err.response.data);
      }
    }
  }
};

export const getCompanionResponse = async (userInput) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/companion`,
      { user_input: userInput }  // Match the expected request body format
    );
    return response.data;
  } catch (error) {
    console.error('Error getting companion response:', error);
    throw error;
  }
};