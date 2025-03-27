document.addEventListener('DOMContentLoaded', async () => {
  const urlSpan = document.getElementById('url');
  const resultPara = document.getElementById('result');
  const checkBtn = document.getElementById('checkBtn');

  // Get active tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0].url;
    urlSpan.innerText = url || "Unable to retrieve URL";
    checkBtn.addEventListener('click', () => analyzeURL(url));
  });

  async function analyzeURL(url) {
    if (!url) {
      resultPara.innerText = "Error: No valid URL found!";
      return;
    }

    resultPara.innerText = "Checking...";

    try {
      const response = await fetch('http://127.0.0.1:5000/check_subscription', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
      });

      const data = await response.json();
      resultPara.innerText = data.result || "Error analyzing URL!";
    } catch (error) {
      resultPara.innerText = "Error connecting to the server.";
    }
  }
});
