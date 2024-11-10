export function setupSSEReceiver(element: HTMLElement, canvas: HTMLCanvasElement) {
  const eventSource = new EventSource('http://127.0.0.1:5000/stream')
  let lastPosition: { cx: number, cy: number } | null = null
  let drawLines = false

  // Get the canvas context
  const ctx = canvas.getContext('2d')!

  // Store previously drawn circles to avoid clearing the entire canvas
  let circles: { cx: number, cy: number }[] = []

  // Function to draw the thumb position
  function drawThumbPosition(cx: number, cy: number) {
    // Clear only the area of the last gray circle
    if (lastPosition) {
      ctx.clearRect(lastPosition.cx - 5, lastPosition.cy - 5, 10, 10) // Clear the old circle area
    }

    // Draw gray circle to represent thumb position
    ctx.fillStyle = drawLines ? 'black' : 'gray'
    ctx.beginPath()
    ctx.arc(cx, cy, 5, 0, Math.PI * 2)
    ctx.fill()

    // Save this circle's position
    circles.push({ cx, cy })

    // Draw persistent black lines if space is pressed
    if (lastPosition && drawLines) {
      ctx.beginPath()
      ctx.moveTo(lastPosition.cx, lastPosition.cy)
      ctx.lineTo(cx, cy)
      ctx.strokeStyle = 'black'
      ctx.lineWidth = 2
      ctx.stroke()
    }

    // Save the current position as the last position
    lastPosition = { cx, cy }
  }

  // Event listener for SSE
  eventSource.onmessage = (event) => {
    console.log('Received event:', event.data);
    element.innerHTML = event.data

    const thumbPosition = event.data.split(',')
    const cx = parseInt(thumbPosition[0])
    const cy = parseInt(thumbPosition[1])

    // Draw thumb position on canvas
    drawThumbPosition(cx, cy)
  }

  // Listen for space bar to toggle line drawing
  window.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
      drawLines = true
    }
  })

  window.addEventListener('keyup', (event) => {
    if (event.code === 'Space') {
      drawLines = false
    }
  })
}
