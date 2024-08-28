const puppeteer = require('puppeteer');

// Function to capture the screenshot
async function captureScreenshot() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.setViewport({
        width: 500, 
        height: 300, 
        deviceScaleFactor: 2 
    });
    
    await page.setContent(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vikram Samvat Date Finder</title>
            <style>
                .badge {
                    background: linear-gradient(145deg, #fffbe6, #f4f4f4); 
                    border: 1px solid #ff9800;
                    padding: 5px 10px; 
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), inset 0 -1px 3px rgba(255, 255, 255, 0.6); 
                    text-align: center;
                    width: 120px; 
                    font-size: 10px;
                }
                .badge-line {
                    font-size: 12px;
                    margin: 2px 0; 
                }
                #line1 {
                    font-size: 14px; /* Slightly larger and bold for prominence */
                    font-weight: bold;
                    color: #ff4800;
                }
            </style>
        </head>
        <body>
            <main>
                <div id="badge" class="badge">
                    <div id="line1" class="badge-line">१०, भाद्रपद</div>
                    <div id="line2" class="badge-line">कृष्ण पक्ष , दशमी</div>
                    <div id="line3" class="badge-line">२०८१ पिङ्गल, विक्रम सम्वत</div>
                </div>
            </main>
        </body>
        </html>
    `);
    
    // Wait for the element to be available
    await page.waitForSelector('#badge');
    
    // Select the element to capture
    const badgeElement = await page.$('#badge');
    
    // Take a screenshot of the selected element
    await badgeElement.screenshot({
        path: 'badge.png',
        fullPage: false,
        type: 'png'
    });
    
    await browser.close();
}

// Schedule the task to run every 6 hours (21600000 milliseconds)
const interval = 6 * 60 * 60 * 1000; // 6 hours

// Run immediately once at startup
captureScreenshot();

// Set up interval to run the function periodically
setInterval(captureScreenshot, interval);