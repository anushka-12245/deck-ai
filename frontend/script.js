// point to your backend server
const API_BASE = "http://127.0.0.1:8000";

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  const feedbackDiv = document.getElementById("feedback");

  if (!file) {
    feedbackDiv.innerText = "Please select a file.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  feedbackDiv.innerText = "Processing file... Please wait.";

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.feedback) {
      feedbackDiv.innerText = data.feedback;
      addToChatLog("AI", data.feedback);
    } else {
      feedbackDiv.innerText = "Error: " + (data.error || "Unknown error");
    }
  } catch (err) {
    feedbackDiv.innerText = "Upload failed. Please try again.";
    console.error(err);
  }
}

async function askFollowUp() {
  const input = document.getElementById("userQuery");
  const query = input.value.trim();
  if (!query) return;

  addToChatLog("User", query);
  input.value = "";

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.response) {
      addToChatLog("AI", data.response);
    } else {
      addToChatLog("AI", "Something went wrong. Try again.");
    }
  } catch (err) {
    console.error(err);
    addToChatLog("AI", "Server error. Try again later.");
  }
}

function addToChatLog(sender, message) {
  const chatLog = document.getElementById("chatLog");
  const msgDiv = document.createElement("div");
  msgDiv.className = sender.toLowerCase() === "ai" ? "bot" : "user";
  msgDiv.innerText = `${sender}: ${message}`;
  chatLog.appendChild(msgDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}
