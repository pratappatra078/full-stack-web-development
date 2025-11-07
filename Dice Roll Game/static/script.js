let totalScore = 0;  // Sum of all rolls
let rollCount = 0;   // Number of rolls

async function rollDice() {
    const diceElement = document.getElementById('dice');
    
    // Add rolling animation
    diceElement.classList.add('roll');
    
    try {
        // Make a request to Python backend
        // fetch() sends HTTP request to '/roll' route in app.py
        const response = await fetch('/roll');
        
        // Convert response to JSON format
        const data = await response.json();
        
        // Wait for animation to complete (500ms)
        setTimeout(() => {
            // Update dice display with value from Python
            diceElement.textContent = data.value;
            
            // Remove animation class
            diceElement.classList.remove('roll');
            
            // Update scores
            updateScore(data.value);
        }, 500);
        
    } catch (error) {
        // Handle any errors (network issues, server down, etc.)
        console.error('Error rolling dice:', error);
        alert('Failed to roll dice. Make sure the server is running!');
    }
}

/**
 * Updates the score display
 * @param {number} currentRoll - The dice value from Python
 */
function updateScore(currentRoll) {
    // Increment counters
    rollCount++;
    totalScore += currentRoll;
    
    // Update HTML display
    document.getElementById('current').textContent = currentRoll;
    document.getElementById('total').textContent = totalScore;
    document.getElementById('count').textContent = rollCount;
}