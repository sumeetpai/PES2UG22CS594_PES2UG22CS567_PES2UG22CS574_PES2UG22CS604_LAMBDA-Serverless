const fs = require('fs');

try {
    // Read input from file
    const inputData = JSON.parse(fs.readFileSync('/app/input.json', 'utf8'));

    // Import and execute function
    const { handler } = require('./function.js');
    const result = handler(inputData);

    // Ensure result is JSON serializable
    const output = typeof result === 'object' ? result : { output: result };

    // Write output
    fs.writeFileSync('/app/output.json', JSON.stringify(output));
} catch (error) {
    fs.writeFileSync('/app/output.json', JSON.stringify({ error: error.message }));
} 