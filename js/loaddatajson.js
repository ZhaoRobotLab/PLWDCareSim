async function loadDataFromFile(filePath) {
    try {
      const response = await fetch(filePath);
      const jsonData = await response.json();
  
      const messageSequence = [];
  
      jsonData.forEach((item) => {
        const message = [item.verbal_utterance];
        if (item.nonverbal_behavior) {
          //console.log("How many nonverbal behaviors? " + item.nonverbal_behavior.length);
          combined_nonverbal_behavior = "";
          for (let i = 0; i < item.nonverbal_behavior.length; i++) {
            combined_nonverbal_behavior += item.nonverbal_behavior[i];
            //if this isn't the last nonverbal behavior, add a comma
            if (i < item.nonverbal_behavior.length - 1) {
              combined_nonverbal_behavior += ", ";
            }
          }
          message.push(combined_nonverbal_behavior);
        }
  
        messageSequence.push(message);
      });
  
      return messageSequence;
    } catch (error) {
      console.error('Error loading data:', error);
      return null;
    }
  }
  
