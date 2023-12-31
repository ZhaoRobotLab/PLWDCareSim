  // Function to simulate the text message exchange
  function simulateTextMessageExchange(messages) {
    const messageContainer = document.getElementById('message-container');

    function appendMessage(isInterventionist, content, nonverbalAction) {
      return new Promise(resolve => {
        const messageBox = document.createElement('div');
        messageBox.classList.add('box');
        messageBox.classList.add(isInterventionist ? 'sb1' : 'sb2');
        messageBox.classList.add(isInterventionist ? 'interventionist' : 'patient');
        const messageContent = document.createElement('div');
        messageContent.classList.add('typing-animation');
        messageBox.appendChild(messageContent);

        messageContainer.appendChild(messageBox);
        messageContainer.scrollTop = messageContainer.scrollHeight;
        animateText(messageContent, content, resolve);

        if (nonverbalAction) {
          const nonverbalActionDiv = document.createElement('div');
          nonverbalActionDiv.classList.add('nonverbal-action');
          nonverbalActionDiv.textContent = nonverbalAction;
          messageBox.appendChild(nonverbalActionDiv);
        }
      });
    }

    function animateText(element, text, resolve) {
      let index = 0;
      const typingInterval = setInterval(() => {
        element.textContent = text.slice(0, index);
        index++;

        if (index > text.length) {
          clearInterval(typingInterval);
          resolve();
          messageContainer.scrollTop = messageContainer.scrollHeight;
        }
      }, 50); // Adjust the typing speed as needed (in milliseconds)
    }

    async function displayMessagesSequentially() {
      for (let i = 0; i < messages.length; i++) {
        const [message, nonverbalAction] = messages[i];
        const isInterventionist = i % 2 === 0;

        await appendMessage(isInterventionist, message, nonverbalAction);
        
        // Scroll to the bottom to show the latest message
        messageContainer.scrollTop = messageContainer.scrollHeight;

        // Delay before the next message
        await new Promise(resolve => setTimeout(resolve, 1000)); // Adjust the delay as needed
      }
    }

    // Start the simulation
    displayMessagesSequentially();
  }

  // Example usage
//   const messageSequence = [
//     ["Hello there!"],
//     ["Hi! How can I help you today?", "Patient is typing..."],
//     ["I've been feeling a bit under the weather lately."],
//     ["I'm sorry to hear that. Let's talk about your symptoms.", "Interventionist is typing..."],
//     // Add more messages as needed
//   ];

  // Start the exchange when the page loads
  window.onload = function () {
    
    const filePath = 'your-messages.json';
    loadDataFromFile(filePath).then((messageSequence) => {
        if (messageSequence) {
        console.log(messageSequence);
        simulateTextMessageExchange(messageSequence);
        } else {
        console.log('Failed to load data.');
        }
    });

    simulateTextMessageExchange(messageSequence);
  };