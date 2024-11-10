export function setupSSEReceiver(element: HTMLElement) {
  const eventSource = new EventSource('http://127.0.0.1:5000/numbers')
  eventSource.onmessage = (event) => {
    element.innerHTML = event.data
  }
}