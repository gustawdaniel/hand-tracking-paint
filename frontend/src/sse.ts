export function setupSSEReceiver(element: HTMLElement) {
  const eventSource = new EventSource('http://127.0.0.1:5000/hand-position')
  eventSource.onmessage = (event) => {
    console.log('event', event);
    element.innerHTML = event.data
  }
}

