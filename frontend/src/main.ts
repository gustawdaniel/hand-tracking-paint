import './style.css'
import { setupSSEReceiver } from './sse.ts'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <p>Tracking Thumb Position</p>
    <p id="sse"></p>
    <canvas id="thumbCanvas" width="640" height="480" style="border: 1px solid black;"></canvas>
  </div>
`
const canvasElement = document.querySelector<HTMLCanvasElement>('#thumbCanvas')!
const debugElement = document.querySelector<HTMLElement>('#sse')!

setupSSEReceiver(debugElement, canvasElement)
